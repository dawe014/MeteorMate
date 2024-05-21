import requests
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session

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

API_KEY = 'fYA06PNSbAbW15Kf6TmXro7nxgQAh1dG'
BASE_URL = 'https://api.tomorrow.io/v4/timelines'

@bp.route('/api/weather', methods=['GET'])
def get_weather():
    location = request.args.get('location')
    if not location:
        return jsonify({'error': 'Location is required'}), 400

    params = {
        'location': location,
        'fields': ['temperature', 'weatherCode'],
        'timesteps': '1h',
        'units': 'metric',
        'apikey': API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if response.status_code != 200:
        return jsonify({'error': data.get('message', 'Error fetching data')}), response.status_code

    weather_data = {
        'location': location,
        'temperature': data['data']['timelines'][0]['intervals'][0]['values']['temperature'],
        'description': data['data']['timelines'][0]['intervals'][0]['values']['weatherCode']
    }

    return jsonify(weather_data)

@bp.route('/api/forecast', methods=['GET'])
def get_forecast():
    location = request.args.get('location')
    if not location:
        return jsonify({'error': 'Location is required'}), 400

    params = {
        'location': location,
        'fields': ['temperature', 'weatherCode'],
        'timesteps': '1d',
        'units': 'metric',
        'apikey': API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if response.status_code != 200:
        return jsonify({'error': data.get('message', 'Error fetching data')}), response.status_code

    forecast_data = {
        'location': location,
        'forecast': [
            {
                'date': interval['startTime'],
                'temp': interval['values']['temperature'],
                'condition': interval['values']['weatherCode']
            }
            for interval in data['data']['timelines'][0]['intervals']
        ]
    }

    return jsonify(forecast_data)
