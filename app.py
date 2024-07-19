from flask import Flask, render_template, jsonify
import pandas as pd
import requests
import config
from aqi_calculator import calculate_aqi

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_aqi_data')
def get_aqi_data():
    cities_data = pd.read_csv('us_cities_100k_plus.csv')

    # Hides API key
    api_key = config.api_key 

    data = []

    for _, row in cities_data.iterrows():
        lat = row['lat']
        lng = row['lng']
        city_name = row['city']
        response = requests.get(f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lng}&appid={api_key}')
        app.logger.debug(f"API Response: {response.status_code}, Content: {response.content}")
        
        if response.status_code == 200:
            pollutant_data = response.json()
            app.logger.debug(f"Pollutant Data: {pollutant_data}")
            
            city_data = {
                'city': city_name,
                'lat': lat,
                'lng': lng,
                'pm2_5': pollutant_data['list'][0]['components'].get('pm2_5', 0),
                'pm10': pollutant_data['list'][0]['components'].get('pm10', 0),
                'o3': pollutant_data['list'][0]['components'].get('o3', 0),
                'no2': pollutant_data['list'][0]['components'].get('no2', 0),
                'so2': pollutant_data['list'][0]['components'].get('so2', 0),
                'co': pollutant_data['list'][0]['components'].get('co', 0)
            }
            
            aqi = calculate_aqi(city_data)
            city_data['aqi'] = aqi
            data.append(city_data)
            app.logger.debug(f"City Data with AQI: {city_data}")
        else:
            app.logger.error(f"Failed to get data from API for {city_name}. Status code: {response.status_code}")

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
