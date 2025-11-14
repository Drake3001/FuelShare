import datetime
import dotenv
import os

from pydantic import ValidationError
from pytoyoda import *
from database.schemas.trip_schema import TripCreateSchema


async def synctrips(startDate: datetime, endDate: datetime=datetime.datetime.now()):
    dotenv.load_dotenv()
    username = os.getenv("TOYOTA_USERNAME")
    password = os.getenv("TOYOTA_PASSWORD")
    client = MyT(username=username, password=password, use_metric=True)
    await client.login()
    vehicles = await client.get_vehicles()
    ###pobieranie wszystkich samochodów i wpisywanie ich do bazy danych na bieżąco
    vehicle=vehicles[0]
    trips= await vehicle.get_trips(startDate, endDate, full_route=False)
    validated_dtos= []
    for trip in trips:
        dto = parse_trips(trip)
        if dto:
            validated_dtos.append(dto)
    return validated_dtos




def parse_trips(trip_response):
    response_data = {
        "start_lat": trip_response.locations.start.lat if trip_response.locations else 0.0,
        "start_lon": trip_response.locations.start.lon if trip_response.locations else 0.0,
        "end_lat": trip_response.locations.end.lat if trip_response.locations else 0.0,
        "end_lon": trip_response.locations.end.lon if trip_response.locations else 0.0,
        "start_time": trip_response.start_time,
        "end_time": trip_response.end_time,
        "duration": int(trip_response.duration.total_seconds()) if trip_response.duration else 0,
        "distance": trip_response.distance,
        "ev_duration": int(trip_response.ev_duration.total_seconds()) if trip_response.ev_duration else None,
        "ev_distance": trip_response.ev_distance,
        "fuel_consumed": trip_response.fuel_consumed,
        "average_fuel_consumed": trip_response.average_fuel_consumed,
    }
    try:
        validated_dto= TripCreateSchema(**response_data)
        return validated_dto
    except ValidationError as e:
        print(f"Validation Error for started at {trip_response.start_time}: {e}")
        return None