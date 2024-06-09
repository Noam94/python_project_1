import requests as rs
import streamlit as st
import datetime as dt
import pytz as tz

st.title('Welcome to the weather app!')

st.write(dt.datetime.now().strftime('''
%A, %d %B %Y\n
%I:%M %p
'''))

my_api = '47d8441287d3c3d5fe39e3668e7e78c3'
city = st.text_input("Where would you like to know the weather in?")
weather_data = rs.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={my_api}").json()

show_time = st.checkbox("Local time")

if city != '':
  if weather_data['cod'] == 200:
    st.header(city.capitalize())
    st.subheader('Weather description')
    st.write((f'''
      {weather_data['weather'][0]['description']}\n
      Temperature: {weather_data['main']['temp']} degrees\n
      Humidity: {weather_data['main']['humidity']} %
      '''))
    if show_time:
      offset = weather_data['timezone'] / (60 * 60)
      st.subheader('Date and Time')
      st.write(dt.datetime.now(dt.timezone(dt.timedelta(hours=offset))).strftime('''
      %A, %d %B %Y\n
      %I:%M %p
      '''))
  else:
    st.write(weather_data['message'])