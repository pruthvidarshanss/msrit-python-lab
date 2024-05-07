"""
Program 3
--------------------------------------------------------------------------------------------------------------
Write a Python program to do the following.
a. Create Synthesis Weather details in a csv file. 
b. Load the csv file data into dictionary
b. Read a place name and display weather details
d. Read longitude & latitude values from the user and display weather details 
"""

from faker import Faker
import csv, random
from tqdm import tqdm
from geopy.geocoders import Nominatim


def save_to_csv(filename:str, data: dict) -> None:
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Place",  "Latitude", "Longitude", "Temperature", "Humidity", "Wind", "Weather"])
        for k, v in data.items():
            writer.writerow([v["place"], v["latitude"], v["longitude"], v["temperature"], v["humidity"], v["wind"], v["weather"]])


def generate_weather_details(filename: str, num_records: int) -> dict:
    fake = Faker()
    geolocator = Nominatim(user_agent="my_geocoder")

    data = {}
    weather_category = ["Rainy", "Cloudy", "Sunny"]

    for i in tqdm(range(num_records)):
        try:
            city = fake.city()
            loc = geolocator.geocode(city)
                    
            lat = loc.latitude
            long = loc.longitude

            temp = random.randint(-20, 40)  
            humidity = random.randint(10, 100)
            wind = random.randint(3, 25)
            weather = random.choice(weather_category)

            data[i+1] = {
                "place" : city,
                "longitude": lat,
                "latitude": long,
                "temperature": temp,
                "humidity": humidity,
                "wind": wind,
                "weather": weather,
            }

        except:
            pass

    save_to_csv(filename, data)

    return data


dataset = "weather.csv"

wdata = generate_weather_details(dataset, 100)

while True:
    try:
        print("Weather forecast:")
        print("-"*100)
        print("Choose any one option to continue:\n")

        choice = input("1. Weather details on a particular place\n2. Weather details from latitude and longitude\n\n")

        if choice == "1":
            place = input("Enter a place name:\n")

            f = False
            for k, val in wdata.items():
                if place in val["place"]:
                    print(f"Place:\t{val['place']}")
                    print(f"Latitude:\t{val['latitude']}")
                    print(f"Longitude:\t{val['longitude']}")
                    print(f"Temperature:\t{val['temperature']}")
                    print(f"Humidity:\t{val['humidity']}")
                    print(f"Wind Speed:\t{val['wind']}")
                    print(f"Weather:\t{val['weather']}\n\n")
                    f = True

            if not f:
                print("We cannot provide weather details on this place...!")

        elif choice == "2":
            lat = float(input("Enter latitude:\t"))
            long = float(input("Enter longitude:\t"))

            f = False
            for k, val in wdata.items():
                if lat == float(val["latitude"]) and long == float(val["longitude"]):
                    print(f"Latitude:\t{val['latitude']}")
                    print(f"Longitude:\t{val['longitude']}")
                    print(f"Place:\t{val['place']}")
                    print(f"Temperature:\t{val['temperature']}")
                    print(f"Humidity:\t{val['humidity']}")
                    print(f"Wind Speed:\t{val['wind']}")
                    print(f"Weather:\t{val['weather']}\n\n")
                    f = True

            if not f:
                print("We cannot provide weather details on this place...!")

        else:
            print("Invalid choice...!")


    except Exception as e:
        print(f"Error: {e}\n\n")

    except KeyboardInterrupt:
        print("Exiting...!")
        exit()