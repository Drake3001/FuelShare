
from PyQt6.QtCore import QObject, pyqtSignal
from typing import Dict, List, Tuple
from database.schemas.trip_schema import TripSchema


class TripViewModel(QObject):
    content_changed = pyqtSignal()
    trip_updated = pyqtSignal(list)
    trips_added = pyqtSignal()

    def __init__(self, trip_service, user_service):
        super().__init__()
        self.trip_service = trip_service
        self.user_service = user_service

        self.user_service.user_data_changed.connect(self.handle_user_updated_or_deleted)
        self.trip_service.trips_updated.connect(self.handle_trips_updated)

        self.all_trips: Dict[int, TripSchema] = {}
        self.filtered_trips: List[int] = []
        self.sorting_stack: List[Tuple[str, int]] = []

        self.load_initial_data()

    def load_initial_data(self):
        raw_trips = self.trip_service.get_all_trips()
        self.all_trips = {t.id: t for t in raw_trips}
        self.filtered_trips = list(self.all_trips.keys())
        self.filtered_trips.sort()

    def get_trips_slice(self, start_idx: int, end_idx: int) -> List[TripSchema]:
        """Zwraca listę obiektów Schema dla zadanego zakresu (scroll)"""
        ids=self.filtered_trips[start_idx:end_idx]
        return [self.all_trips[key] for key in ids]

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

    def header_changed(self, field_name: str , direction: int ):
        self.sorting_stack = [elem for elem in self.sorting_stack if elem[0] != field_name]
        if direction != 0:
            self.sorting_stack.append((field_name, direction))
        self.sorting()


    def sorting(self):
        if not self.sorting_stack:
            self.filtered_trips.sort()
        else:
            for i in range(len(self.sorting_stack)-1, -1, -1):
                field_name, direction = self.sorting_stack[i]
                print(field_name, direction)
                if direction == 0:
                    pass
                reverse = (direction == -1)
                def key_selector(t_id):
                    val = getattr(self.all_trips[t_id], field_name)
                    if field_name == 'driver':
                        if val is None:
                            return ""
                        name = val.name or ""
                        surname = val.surname or ""
                        return f"{name} {surname}".strip().lower()
                    if val is None:
                        return float('-inf') if reverse else float('inf')
                    return val
                self.filtered_trips.sort(key=key_selector, reverse=reverse)
        self.content_changed.emit()

    def handle_user_updated_or_deleted(self, user_id: int):
        print("handle_user_updated_or_deleted", user_id)
        user = self.user_service.get_user(user_id)

        ids_to_refresh = []
        for trip_id, trip in self.all_trips.items():
            is_modified = False
            updates = {}

            if trip.driver and trip.driver.id == user_id:
                if user:
                    updates["driver"] = user
                else:
                    updates["driver"] = None
                    updates["driver_id"] = None
                is_modified = True
            if trip.payer_ids and user_id in trip.payer_ids:
                if user:
                    is_modified = True
                else:
                    new_payer_ids = [pid for pid in trip.payer_ids if pid != user_id]
                    updates["payer_ids"] = new_payer_ids
                    is_modified = True
            if is_modified:
                if updates:
                    new_trip = trip.model_copy(update=updates)
                    self.all_trips[trip_id] = new_trip

                ids_to_refresh.append(trip_id)
        if ids_to_refresh:
            print(f"User {user_id} zmieniony/usunięty. Odświeżam {len(ids_to_refresh)} tripów.")
            self.trip_updated.emit(ids_to_refresh)

    def handle_trips_updated(self, trips_ids : List[int]):
        updated_trips = self.trip_service.get_trips_listed(trips_ids)
        new_ids = []
        existing_ids = []
        for trip in updated_trips:
            self.all_trips[trip.id] = trip
            if trip.id in self.filtered_trips:
                existing_ids.append(trip.id)
            else:
                new_ids.append(trip.id)

        if existing_ids:
            self.trip_updated.emit(existing_ids)

        if new_ids:
            self.filtered_trips.extend(new_ids)
            self.filtered_trips.sort()
            self.trips_added.emit()