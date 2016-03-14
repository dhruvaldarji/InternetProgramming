# !/usr/bin/python

"""
Get and Display Weather Data for a ZipCode via REST API
"""

# Imports
import requests
import json
from datetime import datetime

# Variables
user_id = ""  # Unnecessary
# DELETE this API ID before submission!!!
user_apiid = "15eb7ea63ba50c8cd3b335824763ec97"  # REQUIRED
zip_code = "30055"  # REQUIRED


def get_weather(appid, zipcode):
    response = requests.get(
        "http://api.openweathermap.org/data/2.5/weather?appid=" + appid + "&units=imperial&zip=" + zipcode + ",us")
    response_data = json.loads(response.text)

    return response_data


def print_weather_data(data):
    name = '{0:<25} {1} {2}'.format("Name: ", data['name'], '')
    current_temperature = '{0:<25} {1} {2}'.format("Current Temperature: ", data['main']['temp'], 'Fahrenheit')
    atmospheric_pressure = '{0:<25} {1} {2}'.format("Atmospheric Pressure: ", data['main']['pressure'], 'hPa')
    wind_speed = '{0:<25} {1} {2}'.format("Wind Speed: ", data['wind']['speed'], 'mph')
    wind_direction = '{0:<25} {1} {2}'.format("Wind Direction: ", data['wind']['deg'], 'degrees')
    time = '{0:<25} {1} {2}'.format("Time of Report: ",
                                    datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S'), '')

    print(name)
    print(current_temperature)
    print(atmospheric_pressure)
    print(wind_speed)
    print(wind_direction)
    print(time)


# Get the Weather and print the data
print_weather_data(get_weather(user_apiid, zip_code))
