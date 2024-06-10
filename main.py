import requests as rs
import streamlit as st
import datetime as dt
import json

st.title('Welcome to the weather app!')
my_api = '47d8441287d3c3d5fe39e3668e7e78c3'

st.write(dt.datetime.now(dt.timezone(dt.timedelta(hours=+3))).strftime('''
%A, %d %B %Y\n
%I:%M %p
'''))

location = {}
city = ''
try:
  with open('settings.json', 'r+') as f:
    try:
      settings = (json.load(f))
      location["default"] = settings.setdefault("default", [])
      location["favorites"] = settings.setdefault("favorites", [])
      location["units"] = settings.setdefault("units", [])
    except:
      location["default"] = []
      location["favorites"] = []
      location["units"] = []
except FileNotFoundError:
  with open('settings.json', 'w+') as f:
    location["default"] = []
    location["favorites"] = []
    location["units"] = []

# set default locations:
default_loc_input = st.text_input("Would you like to set a default location?")
if default_loc_input != '' and st.button("Set default"):
  location["default"] = default_loc_input.title()
  with open('settings.json','w') as f:
    json.dump(location,f)

# set favorites:
favorites_loc_input = st.text_input("Add favorite locations:")
if favorites_loc_input != '' and st.button("Add"):
  if favorites_loc_input.title() not in location["favorites"]:
    location["favorites"].append(favorites_loc_input.title())
    with open('settings.json','w') as f:
      json.dump(location,f)

# set default units:
units_input = st.radio("Temperature units", ["metric", "imperial"], captions=["°C","°F"], index=None)
if units_input is not None:
  def_units = units_input
elif len(location["units"]) > 0:
  def_units = location["units"]
else:
  def_units = "metric"

if st.button("Set default units"):
  location["units"] = def_units
  with open('settings.json', 'w') as f:
    json.dump(location, f)

def get_weather(weather_data, units, city=location["default"]):
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

if len(location["favorites"]) > 0:
  check_favorites = st.checkbox("Choose from favorite")
  if check_favorites:
    city = st.selectbox("Choose from favorites", location["favorites"], index=None, placeholder="Select location...")
  else:
    city = st.text_input("Where would you like to know the weather in?")
else:
  city = st.text_input("Where would you like to know the weather in?")
  check_favorites = False

weather_data = rs.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units={def_units}&appid={my_api}").json()


show_time = st.toggle("Local time")

if (city != '' and not check_favorites) or (city is not None and check_favorites):
  if weather_data['cod'] == 200:
    get_weather(weather_data, def_units, city)
    if show_time:
      get_timezone(weather_data['timezone'] / (60 * 60))
  else:
    st.write(weather_data['message'])
elif len(location["default"]) >= 1:
  default_loc = location["default"]
  weather_data = rs.get(f"https://api.openweathermap.org/data/2.5/weather?q={default_loc}&units={def_units}&appid={my_api}").json()
  get_weather(weather_data, def_units)
