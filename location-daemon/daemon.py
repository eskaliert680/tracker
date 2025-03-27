import time, json, geocoder, requests
from logging import warn
starttime = time.monotonic()

CONFIG_JSON_PATH = "config.json"

with open(CONFIG_JSON_PATH, 'r') as file:
    data = json.load(file)

DELAY = data["delay"]
URL = data["url"]

def get_current_gps_coordinates():
    g = geocoder.ip('me')
    if g.latlng is not None:
        return g.latlng
    else:
        return None

print(get_current_gps_coordinates())

def run():
    while True:
        coords = get_current_gps_coordinates() # 0 is latitude, 1 is longitude
        if coords is not None:
            requests.post(URL,{"latitude":coords[0],"longitude":coords[1]})
        else:
            warn("Could not get coordinates from IP address. Check your internet connection")
        time.sleep(float(DELAY) - ((time.monotonic() - starttime) % float(DELAY)))
