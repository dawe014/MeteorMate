import requests
from flask import Blueprint, render_template, request, jsonify
from flask import *
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/forecast')
def forecast():
    return render_template('forecast.html')

@bp.route('/history')
def history():
    return render_template('history.html')

@bp.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        units = request.form['units']
        session['units'] = units
        return redirect(url_for('main.settings'))
    units = session.get('units', 'metric')
    return render_template('settings.html', units=units)

API_KEY = 'fe370947b3844fefae1180925242005'
BASE_URL = 'http://api.weatherapi.com/v1'

@bp.route('/api/weather', methods=['GET'])
def get_weather():
    location = request.args.get('location')
    if not location:
        return jsonify({'error': 'Location is required'}), 400

    response = requests.get(f"{BASE_URL}/current.json", params={'key': API_KEY, 'q': location})
    data = response.json()

    if response.status_code != 200:
        return jsonify({'error': data.get('error', {}).get('message', 'Error fetching data')}), 400

    weather_data = {
        'location': data['location']['name'],
        'temperature': data['current']['temp_c'],
        'description': data['current']['condition']['text'],
        'humidity': data['current']['humidity'],
        'wind_speed': data['current']['wind_kph']
    }

    return jsonify(weather_data)

@bp.route('/api/forecast', methods=['GET'])
def get_forecast():
    location = request.args.get('location')
    if not location:
        return jsonify({'error': 'Location is required'}), 400

    response = requests.get(f"{BASE_URL}/forecast.json", params={'key': API_KEY, 'q': location, 'days': 3})
    data = response.json()

    if response.status_code != 200:
        return jsonify({'error': data.get('error', {}).get('message', 'Error fetching data')}), 400

    forecast_data = {
        'location': data['location']['name'],
        'forecast': [
            {
                'date': day['date'],
                'temp': day['day']['avgtemp_c'],
                'condition': day['day']['condition']['text']
            }
            for day in data['forecast']['forecastday']
        ]
    }

    return jsonify(forecast_data)
