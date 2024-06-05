import requests
import streamlit as st

my_api = '47d8441287d3c3d5fe39e3668e7e78c3'
city = input("Please write a city name: ")
weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={my_api}").json()

while weather_data['cod'] != 200:
  print(weather_data['message'])
  city = input("Please write a city name: ")
  weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={my_api}").json()


weather_string = f'''
The weather in {city} is: {weather_data['weather'][0]['description']}
Temprature: {weather_data['main']['temp']} degrees
Humidity: {weather_data['main']['humidity']} %
'''

st.write(weather_string)