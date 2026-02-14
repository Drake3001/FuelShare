import time
import random
from typing import List, Tuple

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from geopy import Location

from database.schemas.trip_schema import TripUpdateSchema


def geocoder(trip_list: List[Tuple[int, Tuple[float, float], Tuple[float, float]]]) -> List[TripUpdateSchema]:
    processed = 0
    to_process = len(trip_list)
    results = []

    geolocator = Nominatim(user_agent="FuelShareApp/1.0", timeout=10)

    for entry in trip_list:
        print(f"Wykonano {processed}/{to_process}")
        processed += 1
        trip_id, start, end = entry

        print("starting location")
        geo1 = _safe_reverse(geolocator, start)
        time.sleep(2.0 + random.uniform(0.1, 1.0))

        print("ending location")
        geo2 = _safe_reverse(geolocator, end)
        time.sleep(2.0 + random.uniform(0.1, 1.0))

        str1 = format_address(geo1)
        str2 = format_address(geo2)

        results.append(TripUpdateSchema(id=trip_id, start_address=str1, end_address=str2))

    return results


def _safe_reverse(geolocator, coords, retries=2):
    """Reverse geocode with timeout handling and retries."""
    for attempt in range(retries + 1):
        try:
            return geolocator.reverse(f"{coords[0]}, {coords[1]}", language="pl")
        except GeocoderTimedOut:
            print(f"  Timeout (próba {attempt + 1}/{retries + 1})")
            if attempt < retries:
                time.sleep(3.0 + random.uniform(1.0, 2.0))
        except GeocoderServiceError as e:
            print(f"  Błąd serwisu geocoding: {e}")
            if attempt < retries:
                time.sleep(5.0 + random.uniform(1.0, 3.0))
    return None


def format_address(geo: Location):
    if geo is None:
        return "Nie znaleziono adresu"
    address = geo.raw.get('address', {})
    city = (address.get('city') or
            address.get('town') or
            address.get('village') or
            address.get('suburb') or
            "Nieznana miejscowość")

    road = address.get('road', '')
    house_num = address.get('house_number', '')

    parts = [city]
    if road != '':
        parts.append(road)
    if house_num != '':
        parts.append(house_num)
    return ", ".join(parts)
