"""
Program 3
-----------------------------------------------------------------------------------------------
Weather details displaying for a particular place given longitude & latitude in the globe.
Read longitude & latitude values from the user and store weather details to a dictionary.
"""

import requests
from datetime import datetime


def get_weather(latitude: float, longitude: float) -> dict:
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid=3118cd38ee3c8d85bea678b7100a9d31&units=metric"
    response = requests.get(url)
    data = response.json()

    return data


def display_weather(data: dict) -> None:
    if int(data["cod"]) == 400:
        print(f"ERROR!\t{data['message']}\n")

    elif int(data["cod"]) == 200:
        print("-" * 100)
        print(f"\nPlace:\t{data['name']}, {data['sys']['country']}")
        print(
            f"Weather report:\t{data['weather'][0]['main']} with {data['weather'][0]['description']} near {data['base']}"
        )
        print(
            f"Temperature:\t{data['main']['temp']} but feels like {data['main']['feels_like']}"
        )
        # print(f"Min temperature:\t{data['main']['temp_min']}")
        # print(f"Max temperature:\t{data['main']['temp_max']}")
        print(f"Pressure:\t{data['main']['pressure']}")
        print(f"Humidity:\t{data['main']['humidity']}")
        print(f"Visibility:\t{data['visibility']}")
        print(
            f"Wind speed:\t{data['wind']['speed']} at an angle of {data['wind']['deg']}"
        )
        print(f"\n-> {datetime.fromtimestamp(data['dt'])}\n")
        print("-" * 100)


while True:
    try:
        print("-" * 100)
        print("Weather Manager")
        print("-" * 100)
        latitude = float(input("Enter latitude value:\t"))
        longitude = float(input("Enter longitudinal value:\t"))

        weather_data = get_weather(latitude, longitude)

        # error message
        # weather_data = {'cod': '400', 'message': 'wrong latitude'}

        # success
        # weather_data = {'coord': {'lon': -122.4194, 'lat': 37.7749}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 10.33, 'feels_like': 9.64, 'temp_min': 6.27, 'temp_max': 12.44, 'pressure': 1021, 'humidity': 85}, 'visibility': 10000, 'wind': {'speed': 5.66, 'deg': 280}, 'clouds': {'all': 20}, 'dt': 1707632260, 'sys': {'type': 2, 'id': 2017837, 'country': 'US', 'sunrise': 1707577532, 'sunset': 1707615745}, 'timezone': -28800, 'id': 5391959, 'name': 'San Francisco', 'cod': 200}

        display_weather(weather_data)

    except KeyboardInterrupt:
        print("\nExiting....!")
        exit()


"""
Output

Enter latitude value:   13.031781
Enter longitudinal value:       77.569854
-----------------------------------------------------------------------------------------------

Place:  Kanija Bhavan, IN
Weather report: Clouds with scattered clouds near stations
Temperature:    27.97 but feels like 27.78
Pressure:       1023
Humidity:       42
Visibility:     8000
Wind speed:     5.14 at an angle of 100

-> 2024-02-11 12:10:46

-----------------------------------------------------------------------------------------------

Enter latitude value: 37.7749 (San Francisco)
Enter longitudinal value: -122.4194 (San Francisco)
-----------------------------------------------------------------------------------------------

Place:   San Francisco, US
Weather report: Clouds with few clouds near stations
Temperature:    10.33 but feels like 9.64
Pressure:       1021
Humidity:       85
Visibility:     10000
Wind speed:     5.66 at an angle of 280

-> 2024-02-11 11:47:40

"""