import datetime
import dotenv
import os
from pytoyoda import *
from database.models.trip import Trip

async def synctrips(startDate: datetime, endDate: datetime=datetime.datetime.now()):
    dotenv.load_dotenv()
    username = os.getenv("TOYOTA_USERNAME")
    password = os.getenv("TOYOTA_PASSWORD")
    client = MyT(username=username, password=password, use_metric=True)
    await client.login()
    vehicles = await client.get_vehicles()
    trips= await vehicles[0].get_trips(startDate, endDate, full_route=False)
    parsed_trips = [parse_trip(trip) for trip in trips]
    return parsed_trips

def parse_trip(trip) -> Trip:
    return Trip(
        start_lat=trip.locations.start.lat if trip.locations else 0.0,
        start_lon=trip.locations.start.lon if trip.locations else 0.0,
        end_lat=trip.locations.end.lat if trip.locations else 0.0,
        end_lon=trip.locations.end.lon if trip.locations else 0.0,
        start_time=trip.start_time,
        end_time=trip.end_time,
        duration=int(trip.duration.total_seconds()) if trip.duration else 0,
        distance=trip.distance or 0.0,
        ev_duration=int(trip.ev_duration.total_seconds()) if trip.ev_duration else None,
        ev_distance=trip.ev_distance,
        fuel_consumed=trip.fuel_consumed or 0.0,
        average_fuel_consumed=trip.average_fuel_consumed or 0.0,
        user=None  # jeśli chcesz przypisać użytkownika później
    )