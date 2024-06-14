# python_project_1: Weather App

Welcome to the Weather App! This application allows users to get the current weather information for various locations. The app can save favorite locations and set default units for temperature. It also shows the local date and time for the selected city.

## Features

- Display current weather information (general description, temperature, and humidity).
- Set and save a default location.
- Set and save favorite locations.
- Choose between metric and imperial units for temperature.
- Display the local date and time for the selected city.

## Installation

- Main file to run: main.py
- All the requirements are in the pyproject.toml file.
- The script is run through streamlit: can be directly from the terminal (with the command: streamlit run main.py) or through the public link to the application.
- settings.json file is not mandatory: if the file does not exist, it will automatically create one. This file stores the default location, favorite locations, and preferred temperature units.

## Usage:

- Set default location: the app will show the weather in this location if no other location is provided.
- Set favorite locations: The user can set as many locations as they want.
- Choose a location: you can either type a city name or click on the "Choose from favorites" button, and the list of favorite locations will appear.
- Choose default measurement units for temperature: if default units are not chosen, the default will be metric (Celcios). The user can change to imperial (Fahrenheit) and save this setting.
- Show local time: by choosing this option, the local time at the chosen location will be shown.

## Streamlit application link:
[Whether app](https://pythonproject1-9farhdpv6jsegiwhx3wcu4.streamlit.app/)
