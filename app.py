import os
import requests

from pprint import PrettyPrinter
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file
# from geopy.geocoders import Nominatim


################################################################################
## SETUP
################################################################################

app = Flask(__name__)

# Get the API key from the '.env' file
load_dotenv()

pp = PrettyPrinter(indent=4)

API_KEY = os.getenv('API_KEY')
API_URL = 'http://api.openweathermap.org/data/2.5/weather'
ICON_URL = 'http://openweathermap.org/img/wn/'


################################################################################
## ROUTES
################################################################################

@app.route('/')
def home():
    """Displays the homepage with forms for current or historical data."""
    context = {
        'min_date': (datetime.now() - timedelta(days=5)),
        'max_date': datetime.now()
    }
    return render_template('home.html', **context)

def get_letter_for_units(units):
    """Returns a shorthand letter for the given units."""
    return 'F' if units == 'imperial' else 'C' if units == 'metric' else 'K'

def get_weather_data(city, units):
    """Function to get weather data"""

    params = {
    'appid': API_KEY,
    'q': city,
    'units': units,
    }

    result_json = requests.get(API_URL, params=params).json()
    return result_json



@app.route('/results', methods=['GET','POST'])
def results():
    """Displays results for current weather conditions."""
    city = request.args.get('city')
    units = request.args.get('units')

    result_json = get_weather_data(city, units)
    
    context = {
        'date': datetime.now().strftime('%A, %B %d %Y'),
        'city': result_json["name"],
        'description': result_json["weather"][0]["description"],
        'temp': result_json["main"]["temp"],
        'humidity': result_json["main"]["humidity"],
        'wind_speed': result_json["wind"]["speed"],
        'sunrise': datetime.fromtimestamp(result_json["sys"]["sunrise"]),
        'sunset': datetime.fromtimestamp(result_json["sys"]["sunset"]),
        'units_letter': get_letter_for_units(units),
        'icon': ICON_URL + result_json["weather"][0]["icon"] + '@2x.png'
    }

    return render_template('results.html', **context)





@app.route('/comparison_results', methods=['GET', 'POST'])
def comparison_results():
    """Displays the relative weather for 2 different cities."""

    city1 = request.args.get('city1')
    city2 = request.args.get('city2')
    units = request.args.get('units')

    city1_results = get_weather_data(city1, units)
    city2_results = get_weather_data(city2, units)

    temp_diff = ''
    humid_diff = ''
    wind_diff = ''
    sun_diff = ''



    context = {
        'date': datetime.now().strftime('%A, %B %d %Y'),
        'city1_info': {
            'city': city1_results["name"],
            'description': city1_results["weather"][0]["description"],
            'temp': city1_results["main"]["temp"],
            'humidity': city1_results["main"]["humidity"],
            'wind_speed': city1_results["wind"]["speed"],
            'sunrise': datetime.fromtimestamp(city1_results["sys"]["sunrise"]),
            'sunset': datetime.fromtimestamp(city1_results["sys"]["sunset"]),
            'units_letter': get_letter_for_units(units),
            'icon': ICON_URL + city1_results["weather"][0]["icon"] + '@2x.png',
        },
        'city2_info': {
            'city': city2_results["name"],
            'description': city2_results["weather"][0]["description"],
            'temp': city2_results["main"]["temp"],
            'humidity': city2_results["main"]["humidity"],
            'wind_speed': city2_results["wind"]["speed"],
            'sunrise': datetime.fromtimestamp(city2_results["sys"]["sunrise"]),
            'sunset': datetime.fromtimestamp(city2_results["sys"]["sunset"]),
            'units_letter': get_letter_for_units(units),
            'icon': ICON_URL + city2_results["weather"][0]["icon"] + '@2x.png',

        }

    }

    return render_template('comparison_results.html', **context)


if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)
