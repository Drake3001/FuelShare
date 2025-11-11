from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from database.schemas.trip_schema import TripSchema
from frontend.const import trip_record_start, trip_record_end, map_true, map_false
from frontend.stylesheets import trip_card_stylesheet


class TripCard(QWidget):
    def __init__(self, trip_data: TripSchema):
        super().__init__()
        self.trip_data = trip_data
        self.setup_card()
        self.setStyleSheet(trip_card_stylesheet)

    def setup_card(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        id_label = QLabel(f"{self.trip_data.id}")

        time_widget = QWidget()
        time_layout = QVBoxLayout()
        time_widget.setLayout(time_layout)
        start_label = QLabel(trip_record_start)
        end_label = QLabel(trip_record_end)

        # Formatowanie daty - możesz dostosować
        start_time = QLabel(f"{self.trip_data.start_time.strftime('%d.%m.%Y, %H:%M')}")
        end_time = QLabel(f"{self.trip_data.end_time.strftime('%d.%m.%Y, %H:%M')}")

        time_layout.addWidget(start_label)
        time_layout.addWidget(start_time)
        time_layout.addWidget(end_label)
        time_layout.addWidget(end_time)

        if self.trip_data.driver:
            driver_name = f"{self.trip_data.driver.name or ''} {self.trip_data.driver.surname or ''}".strip()
        else:
            driver_name = "Brak kierowcy"

        driver_val = QLabel(driver_name)

        distance_val = QLabel(f"{self.trip_data.distance:.2f} km")

        time_sec = self.trip_data.duration
        time_hour = time_sec // 3600
        time_minute = (time_sec % 3600) // 60
        duration_val = QLabel(f"{time_hour}h {time_minute}m")

        ev_duration=self.trip_data.ev_duration or 0.0
        ev_duration_val=QLabel(f"{ev_duration:.2f} h")

        ev_distance=self.trip_data.ev_distance or 0.0
        ev_distance_val=QLabel(f"{ev_distance:.2f} h")

        consumption_val = QLabel(f"{self.trip_data.fuel_consumed:.2f} L")

        avg_fuel_val = QLabel(f"{self.trip_data.average_fuel_consumed:.2f} L/100km")

        refuel_text = map_true if self.trip_data.refuel else map_false
        refuel_val = QLabel(refuel_text)

        period_val = QLabel(f"{self.trip_data.period}")

        edit_button = QPushButton("Edit")

        layout.addWidget(id_label)
        layout.addWidget(time_widget)
        layout.addWidget(driver_val)
        layout.addWidget(distance_val)
        layout.addWidget(duration_val)
        layout.addWidget(ev_duration_val)
        layout.addWidget(ev_distance_val)
        layout.addWidget(consumption_val)
        layout.addWidget(avg_fuel_val)
        layout.addWidget(refuel_val)
        layout.addWidget(period_val)
        layout.addWidget(edit_button)