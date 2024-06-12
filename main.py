import requests as rs
import streamlit as st
import datetime as dt
import json

st.title('Welcome to the weather app!')
my_api = '47d8441287d3c3d5fe39e3668e7e78c3'

# display current date and time
st.write(dt.datetime.now(dt.timezone(dt.timedelta(hours=+3))).strftime('''
%A, %d %B %Y\n
%I:%M %p
'''))

def save_settings(settings, file='settings.json'):
  with open(file, 'w') as f:
    json.dump(settings, f)

settings = {}
city = ''
try:
  with open('settings.json', 'r+') as f:
    try:
      settings_file = (json.load(f))
      settings["default"] = settings_file.setdefault("default", [])
      settings["favorites"] = settings_file.setdefault("favorites", [])
      settings["units"] = settings_file.setdefault("units", [])
    except:
      settings = {"default": "", "favorites": [], "units": ""}
except FileNotFoundError:
  with open('settings.json', 'w+') as f:
    settings = {"default": "", "favorites": [], "units": ""}

# set default locations:
default_loc_input = st.text_input("Set a default location:")
if default_loc_input and st.button("Set default"):
  settings["default"] = default_loc_input.title()
  save_settings(settings)

# set favorites:
favorites_loc_input = st.text_input("Add favorite locations:")
if favorites_loc_input and st.button("Add"):
  if favorites_loc_input.title() not in settings["favorites"]:
    settings["favorites"].append(favorites_loc_input.title())
    save_settings(settings)

# set default units:
units_input = st.radio("Temperature units", ["metric", "imperial"], captions=["°C","°F"], index=1 if settings["units"] == "imperial" else 0)

if st.button("Set default units"):
  settings["units"] = units_input
  save_settings(settings)


def get_weather(weather_data, units, city=settings["default"]):
  st.header(city.title())
  st.subheader('Weather description')
  if units == "imperial":
    units_toprint = "°F"
  else:
    units_toprint = "°C"
  st.write((f'''
        {weather_data['weather'][0]['description']}\n
        Temperature: {weather_data['main']['temp']} {units_toprint}\n
        Humidity: {weather_data['main']['humidity']} %
        '''))


def get_timezone(offset):
  offset = weather_data['timezone'] / (60 * 60)
  st.subheader('Date and Time')
  st.write(dt.datetime.now(dt.timezone(dt.timedelta(hours=offset))).strftime('''
        %A, %d %B %Y\n
        %I:%M %p
        '''))


if settings["favorites"]:
  check_favorites = st.checkbox("Choose from favorite")
  if check_favorites:
    city = st.selectbox("Choose from favorites", settings["favorites"], index=None, placeholder="Select location...")
  else:
    city = st.text_input("Enter city name:")
else:
  city = st.text_input("Enter city name:")

weather_data = rs.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units={units_input}&appid={my_api}").json()

show_time = st.toggle("Local time")

if (city):
  if weather_data['cod'] == 200:
    get_weather(weather_data, units_input, city)
    if show_time:
      get_timezone(weather_data['timezone'] / (60 * 60))
  else:
    st.write(weather_data['message'])
elif settings["default"]:
  default_loc = settings["default"]
  weather_data = rs.get(f"https://api.openweathermap.org/data/2.5/weather?q={default_loc}&units={units_input}&appid={my_api}").json()
  get_weather(weather_data, units_input)