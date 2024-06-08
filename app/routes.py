from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from . import db, bcrypt
from .models import User
import requests
from flask_login import login_user, logout_user, login_required, current_user

from .decorators import login_required

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    return render_template('index.html')

@bp.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        try:
            full_name = request.form['fname']
            email = request.form['email']
            password = request.form['pass']
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            # Create a new user instance
            new_user = User(full_name=full_name, email=email, password=hashed_password)

            # Add the user to the database
            db.session.add(new_user)
            db.session.commit()

            flash('You have successfully registered! Please login.', 'success')
            return redirect(url_for('main.login'))
        except Exception as e:
            flash(f'Error during registration: {str(e)}', 'danger')

    return render_template('registration.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['pass']

            # Query the database for the user
            user = User.query.filter_by(email=email).first()

            if user and bcrypt.check_password_hash(user.password, password):
                session['loggedin'] = True
                session['id'] = user.id
                session['email'] = user.email
                flash('Login successful!', 'success')
                return redirect(url_for('main.index'))
            else:
                flash('Invalid email or password!', 'danger')

        except Exception as e:
            flash(f'Login failed: {str(e)}', 'danger')

    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    flash('You have successfully logged out.', 'success')
    return redirect(url_for('main.login'))

@bp.route('/forecast')
@login_required
def forecast():
    return render_template('forecast.html')

@bp.route('/api/weather', methods=['GET'])
@login_required
def get_weather():
    location = request.args.get('location')
    if not location:
        return jsonify({'error': 'Location is required'}), 400

    API_KEY = '5eee08f17e6a60e743f9ecd7a57f6a86'
    BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
    units = session.get('units', 'metric')  # Default to 'metric' if not set

    params = {
        'q': location,
        'appid': API_KEY,
        'units': units
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        weather_data = {
            'location': location,
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description']
        }

        return jsonify(weather_data)

    except Exception as e:
        return jsonify({'error': f'Error fetching data: {str(e)}'}), 500

@bp.route('/api/forecast', methods=['GET'])
@login_required
def get_forecast():
    location = request.args.get('location')
    if not location:
        return jsonify({'error': 'Location is required'}), 400

    API_KEY = '5eee08f17e6a60e743f9ecd7a57f6a86'
    BASE_URL = 'https://api.openweathermap.org/data/2.5/forecast'
    units = session.get('units', 'metric')  # Default to 'metric' if not set

    params = {
        'q': location,
        'appid': API_KEY,
        'units': units
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        forecast_data = {
            'location': location,
            'unit': units,
            'forecast': [
                {
                    'date': interval['dt_txt'],
                    'temp': interval['main']['temp'],
                    'pressure': interval['main']['pressure'],
                    'humidity': interval['main']['humidity'],
                    'condition': interval['weather'][0]['description'],
                    'icon': interval['weather'][0]['icon']
                }
                for interval in data['list']
            ]
        }

        return jsonify(forecast_data)

    except Exception as e:
        return jsonify({'error': f'Error fetching data: {str(e)}'}), 500

@bp.route('/settings', methods=['POST'])
@login_required
def save_settings():
    data = request.get_json()
    units = data.get('units')
    if units in ['metric', 'imperial', 'standard']:
        session['units'] = units
        return jsonify({'success': True, 'message': 'Settings saved!'})
    else:
        return jsonify({'success': False, 'message': 'Invalid units!'})
