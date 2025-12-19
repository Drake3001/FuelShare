
from PyQt6.QtCore import QObject, pyqtSignal
from typing import Dict, List
from database.schemas.trip_schema import TripSchema


class TripViewModel(QObject):
    data_changed = pyqtSignal()
    trip_updated = pyqtSignal(list)

    def __init__(self, trip_service, user_service):
        super().__init__()
        self.trip_service = trip_service
        self.user_service = user_service

        self.all_trips: Dict[int, TripSchema] = {}

        self.load_initial_data()

    def load_initial_data(self):
        raw_trips = self.trip_service.get_all_trips()
        self.all_trips = {t.id: t for t in raw_trips}
        # self.filtered_trips_ids = list(self.all_trips.keys()) # uproszczenie

    def get_trips_slice(self, start_idx: int, end_idx: int) -> List[TripSchema]:
        """Zwraca listę obiektów Schema dla zadanego zakresu (scroll)"""
        all_values = list(self.all_trips.values())
        return all_values[start_idx:end_idx]

    def get_trip_by_id(self, trip_id: int) -> TripSchema:
        return self.all_trips.get(trip_id)

    def get_all_users(self):
        return self.user_service.get_all_users()

    def save_trip_edit(self, update_schema):
        updated_trip, modified_trips = self.trip_service.update_trip(update_schema)
        if not updated_trip:
            return
        self.all_trips[updated_trip.id] = updated_trip
        notify_ids=[]
        for t_id, new_period in modified_trips:
            if t_id in self.all_trips:
                current_trip = self.all_trips[t_id]
                new_trip_obj = current_trip.model_copy(update={"period": new_period})
                self.all_trips[t_id] = new_trip_obj
                notify_ids.append(t_id)
        self.trip_updated.emit(notify_ids)
