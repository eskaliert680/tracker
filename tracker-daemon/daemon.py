import time, json, geocoder, datetime, socket
from getmac import get_mac_address
from logging import warn
from supabase import create_client, Client
starttime = time.monotonic()

mac_address = get_mac_address()
hostname = socket.gethostname()

# Pulling configs
CONFIG_JSON_PATH = "config.json"
with open(CONFIG_JSON_PATH, 'r') as file:
    data = json.load(file)
DELAY = data["delay"]
DELAY_SECONDS = float(DELAY) * 60.0
SUPABASE_URL  = data["supabase_url"]
SUPABASE_ANON_KEY = data["supabase_anon_key"]

print(SUPABASE_URL)
print(SUPABASE_ANON_KEY)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def get_current_gps_coordinates():
    g = geocoder.ip('me')
    if g.latlng is not None:
        return g.latlng
    else:
        return None

def getCurrentDateTime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def updateLocation(location_data):
    update_prototype = {
        "latitude": location_data["latitude"],
        "longitude": location_data["longitude"],
        "last_update": getCurrentDateTime()
    }

    # If it does exist, update the entry in the database
    update_response = (
        supabase.table("devices")
        .update(update_prototype)
        .eq("mac_address", location_data["mac_address"])
        .execute()
    )

def createNewDevice(device_data):
    get_response = (
        supabase.table("devices")
        .select("*")
        .eq("device_name", device_data["device_name"])
        .execute()
    )

    device_prototype = {
        "device_name": device_data["device_name"],
        "device_type": device_data["device_type"],
        "latitude": device_data["latitude"],
        "longitude": device_data["longitude"],
        "mac_address": device_data["mac_address"],
        "updated_at": getCurrentDateTime()
    }

    create_response = (
        supabase.table("devices")
        .insert(device_prototype)
        .execute()
    )

def run():
    while True:
        coords = get_current_gps_coordinates() # 0 is latitude, 1 is longitude
        if coords is not None:
            location_update_data = {
                "latitude":float(coords[0]),
                "longitude":float(coords[1]),
                "mac_address":str(get_mac_address())
            }
            print(coords[0])
            print(coords[1])
            updateLocation(location_update_data)
        else:
            warn("Could not get coordinates from IP address. Check your internet connection")
        time.sleep(DELAY_SECONDS - ((time.monotonic() - starttime) % DELAY_SECONDS))
