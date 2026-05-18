import requests
import sys
import json
import pprint
import subprocess
import datetime

def help():
    print("usage: uyr 'location' 'number'")
    print("         'location' = location, duh")
    print("         'number' = hours from now (0 = from now). 'all' displays all available hourly forecasts")
    print("         example: uyr oslo 0 (displays the weather in Oslo right now)")
    print("         example: uyr bergen all (displays the weather in Bergen for the foreseeable future)")

def weather_print(entry):
            location = sys.argv[1]
            current = entry["data"]["instant"]["details"]
            time = entry["time"]
            entry_time = datetime.datetime.fromisoformat(entry["time"])
            local_time = entry_time.astimezone()
            date = local_time.strftime("%d-%m-%Y")
            clock = local_time.strftime("%H:%M")
            if "next_1_hours" in entry["data"]:
                symbol = entry["data"]["next_1_hours"]["summary"]["symbol_code"]
            elif "next_6_hours" in entry["data"]:
                symbol = entry["data"]["next_6_hours"]["summary"]["symbol_code"]
            else:
                symbol = "null"

            # subprocess.run(["kitty", "+kitten", "icat", "--align", "left", "assets/" + symbol + ".png"])
            subprocess.run(["kitty", "+kitten", "icat", "--align", "left", "/usr/local/share/uyr/assets/" + symbol + ".png"])
            sys.stdout.write("\033[8A")
            sys.stdout.write("\033[20C")
            print("Location:", location)
            sys.stdout.write("\033[20C")
            print("Date:", date)
            sys.stdout.write("\033[20C")
            print("Time:", clock)
            sys.stdout.write("\033[20C")

            if current["air_temperature"] < 5:
                color = "\033[34m"
            elif current["air_temperature"] > 20:
                color = "\033[31m"
            else:
                color = "\033[0m"

            print(f"Temp: {color}{current['air_temperature']} °C\033[0m")
            sys.stdout.write("\033[20C")
            print("Wind:", current["wind_speed"], "m/s")
            sys.stdout.write("\033[20C")
            print("Wet:", current["relative_humidity"], "%\033[0m")
            sys.stdout.write("\033[20C")
            if "next_1_hours" in entry["data"]:
                print("Precipitation:", entry["data"]["next_1_hours"]["details"]["precipitation_amount"])

            subprocess.run(["paplay", "--volume=35768", "/usr/local/share/uyr/assets/kavaer.mp3"])


if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help"]:
    help()
elif len(sys.argv) != 3:
    print(" -h, or --help for help")
else:
    headers = {"User-Agent": "uyr-weather-app/0.1"}
    location = sys.argv[1]
    url_geo = f"https://nominatim.openstreetmap.org/search?q={location}&format=json"
    response = requests.get(url_geo, headers=headers)
    data = response.json()
    if len(data) == 0:
        print(f"{sys.argv[1]} is not a location.")
        exit()
    lat = data[0]["lat"]
    lon = data[0]["lon"]

    url_met = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}"
    response = requests.get(url_met, headers=headers)
    data = response.json()

    now = datetime.datetime.now(datetime.UTC)

    for entry in data["properties"]["timeseries"]:
        if sys.argv[2] != "all":
            nowapi = int(entry["time"].split("T")[1].split(":")[0])
            if nowapi == now.hour + int(sys.argv[2]):
                weather_print(entry)
                break

        elif sys.argv[2] == "all":
            symbol = 0
            weather_print(entry)
            print(" ")
            if symbol == "null":
                print("hehe.")
                break


