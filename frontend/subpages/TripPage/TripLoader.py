
from database.cruds.crud_trip import TripService
from database.schemas.trip_schema import TripSchema
from frontend.Widgets.TripCard import TripCard
from typing import Dict

class TripLoader():
    def __init__(self, trip_service: TripService):
        self.trip_service = trip_service
        self.loaded_widget: Dict[int, TripCard]= {}
        self.all_trips: Dict[int, TripSchema]={}
        self.fetch_trip_data()

    def fetch_trip_data(self):
        all_trips = self.trip_service.get_all_trips()
        for trip in all_trips:
            self.all_trips[trip.id] = trip
        print(f"Pobrałem tripow {len(self.all_trips)}")

    def trip_callback(self):
        pass

    def get_trip_cards(self, trip_ids):
        widgets=[]
        print(trip_ids)
        for trip_id in trip_ids:
            if trip_id not in self.loaded_widget:
                self.loaded_widget[trip_id] = TripCard(self.all_trips[trip_id], self.trip_callback)
            widgets.append(self.loaded_widget[trip_id])
        return widgets


    def filter_trips(self, **kwargs):
        #tu dodanie implementacji filtrowania
        return list(self.all_trips.keys())



