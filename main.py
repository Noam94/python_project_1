import requests as rs
import streamlit as st
import datetime as dt
import pytz as tz

st.title('Welcome to the weather app!')

st.text(dt.datetime.now().strftime('''
%A, %d %B %Y
%I:%M %p
'''))

my_api = '47d8441287d3c3d5fe39e3668e7e78c3'
city = st.text_input("Where would you like to know the weather in?")
weather_data = rs.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={my_api}").json()

show_time = st.checkbox("Local time")

if city != '':
  if weather_data['cod'] == 200:
    weather_string = f'''
    {weather_data['weather'][0]['description']}
    Temperature: {weather_data['main']['temp']} degrees
    Humidity: {weather_data['main']['humidity']} %
    '''
    st.header(city.capitalize())
    st.subheader('Weather description')
    st.text(weather_string)
    if show_time:
      city_tz = [s for s in tz.all_timezones if city.title().replace(' ', '_') in s]
      tz_obj = tz.timezone(city_tz[0])
      st.subheader('Date and Time')
      st.text(dt.datetime.now(tz_obj).strftime('''
      %A, %d %B %Y 
      %I:%M %p}
      '''))
  else:
    st.write(weather_data['message'])