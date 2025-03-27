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

from flask import Flask, jsonify, request
from flask_restful import Resource, Api

from supabase import create_client, Client

app = Flask("Tracker")
api = Api(app)

SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY: str = os.environ.get("SUPABASE_ANON_KEY")
GROUP_NAME: str = os.environ.get("GROUP_NAME")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Manager for device geodata.

class GeolocationManager(Resource):
    def post(self):
        data = request.get_json()
        print("Received data:\n",data)

        # Validate received data.
        if not data["id"] or not data["longitude"] or not data["latitude"]:
            return jsonify({"data":[],"code":400})

        # Check if device exists in database
        get_response = (
            supabase.table("devices")
            .select("*")
            .eq("id", data["id"])
            .execute()
        )
        print(get_response.data)

        if len(get_response.data) == 0:
            warn("Device doesn't exist! Returning null!")
            return jsonify({'data':[],'code':404})

        # If it does exist, update the entry in the database
        update_response = (
            supabase.table("devices")
            .update({"latitude": data["latitude"],"longitude":data["longitude"]})
            .eq("id", data["id"])
            .execute()
        )
        return jsonify({"data":[],"code":200})

api.add_resource(GeolocationManager,"/tracker/update")
