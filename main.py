import requests as rs
import streamlit as st
import datetime as dt
import json

st.title('Welcome to the weather app!')
my_api = '47d8441287d3c3d5fe39e3668e7e78c3'

st.write(dt.datetime.now().strftime('''
%A, %d %B %Y\n
%I:%M %p
'''))

# read settings:
location = {}
with open('settings.json', 'r') as f:
  settings = (json.load(f))
  location["default"] = settings.setdefault("default", [])
  location["favorites"] = settings.setdefault("favorites", [])

# set default locations:
default_loc_input = st.text_input("Would you like to set a default location?")
if default_loc_input != '' and st.button("Set default"):
  location["default"] = default_loc_input.capitalize()
  with open('settings.json','w') as f:
    json.dump(location,f)

# set favorites:
favorites_loc_input = st.text_input("Add favorite locations:")
if favorites_loc_input != '' and st.button("Add"):
  if favorites_loc_input.capitalize() not in location["favorites"]:
    location["favorites"].append(favorites_loc_input.capitalize())
    with open('settings.json','w') as f:
      json.dump(location,f)


def get_weather(weather_data, city=location["default"]):
  st.header(city.capitalize())
  st.subheader('Weather description')
  st.write((f'''
        {weather_data['weather'][0]['description']}\n
        Temperature: {weather_data['main']['temp']} degrees\n
        Humidity: {weather_data['main']['humidity']} %
        '''))


def get_timezone(offset):
  offset = weather_data['timezone'] / (60 * 60)
  st.subheader('Date and Time')
  st.write(dt.datetime.now(dt.timezone(dt.timedelta(hours=offset))).strftime('''
        %A, %d %B %Y\n
        %I:%M %p
        '''))

check_favorites = st.checkbox("Choose from favorite")
if check_favorites:
  city = st.selectbox("Choose from favorites", location["favorites"], index=None, placeholder="Select location...")
else:
  city = st.text_input("Where would you like to know the weather in?")

weather_data = rs.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={my_api}").json()

show_time = st.toggle("Local time")

if (city != '' and not check_favorites) or (city is not None and check_favorites):
  if weather_data['cod'] == 200:
    get_weather(weather_data, city)
    if show_time:
      get_timezone(weather_data['timezone'] / (60 * 60))
  else:
    st.write(weather_data['message'])
else:
  default_loc = location["default"]
  weather_data = rs.get(f"https://api.openweathermap.org/data/2.5/weather?q={default_loc}&units=metric&appid={my_api}").json()
  get_weather(weather_data)