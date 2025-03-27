# handler.py
# Written by Gray (@eskaliert680)
# Here you can find the handlers for the POST calls, i.e., updating location data by device, creating new devices, etc.
#
#
#

from logging import warn
import os
from dotenv import load_dotenv
load_dotenv()

import numbers
import datetime

from flask import Flask, jsonify, request
from flask_restful import Resource, Api

from supabase import create_client, Client

app = Flask("Tracker")
api = Api(app)

SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY: str = os.environ.get("SUPABASE_ANON_KEY")
GROUP_NAME: str = os.environ.get("GROUP_NAME")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Insert new device into table.
class CreateNewDevice(Resource):
    def post(self):
        data = request.get_json()
        print("Received data:\n",data)

        if not data["longitude"] or not data["latitude"] or not data["device_name"] or not data["device_type"]:
            return jsonify({"data":[],"code":401,"message":"Malformed data"})

        # Check type of data
        if not isinstance(data["longitude"],numbers.Number) or not isinstance(data["latitude"],numbers.Number):
            return jsonify({"data":[],"code":401,"message":"Bad type on latitude and/or longitude, expected numeric"})

        if not isinstance(data["device_name"],str) or not isinstance(data["device_type"],str):
            return jsonify({"data":[],"code":401,"message":"Bad type on device type and/or name, expected string"})

        # Check if device already exists in the database
        get_response = (
            supabase.table("devices")
            .select("*")
            .eq("device_name", data["device_name"])
            .execute()
        )

        if len(get_response.data) > 0:
            return jsonify({"data":[],"code":401,"message":"Device with name " + data["device_name"] + " already exists in the database"})

        device_prototype = {
            "device_name": data["device_name"],
            "device_type": data["device_type"],
            "latitude": data["latitude"],
            "longitude": data["longitude"],
            "updated_at": datetime.datetime.now()
        }

        create_response = (
            supabase.table("devices")
            .insert(device_prototype)
            .execute()
        )

        return jsonify({
            "data":[],
            "code":200,
            "message":"Device with name " + data["device_name"] + " has been added to the database"
        })

# Update geolocation.

class GeolocationUpdate(Resource):
    def post(self):
        data = request.get_json()
        print("Received data:\n",data)

        # Validate received data.
        if not data["id"] or not data["longitude"] or not data["latitude"]:
            return jsonify({"data":[],"code":401,"message":"Malformed data"})

        # Check if device exists in database
        get_response = (
            supabase.table("devices")
            .select("*")
            .eq("id", data["id"])
            .execute()
        )

        if len(get_response.data) == 0:
            warn("Device doesn't exist! Returning null!")
            return jsonify({'data':[],'code':404,"message":"Device doesn't exist in database"})

        update_prototype = {
            "latitude": data["latitude"],
            "longitude": data["longitude"],
            "updated_at": datetime.datetime.now()
        }

        # If it does exist, update the entry in the database
        update_response = (
            supabase.table("devices")
            .update(update_prototype)
            .eq("id", data["id"])
            .execute()
        )
        return jsonify({"data":[],"code":200,"message":"Geolocation update was successful"})

api.add_resource(GeolocationUpdate,"/tracker/update")
api.add_resource(CreateNewDevice,"/tracker/new-device")
