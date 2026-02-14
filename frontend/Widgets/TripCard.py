# frontend/Widgets/TripCard.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal
from database.schemas.trip_schema import TripSchema
from frontend.const import trip_record_start, trip_record_end, trip_record_start_address, trip_record_end_address, map_true, map_false
from frontend.stylesheets import trip_card_stylesheet


class TripCard(QWidget):
    edit_requested = pyqtSignal(int)

    def __init__(self, trip_data: TripSchema):
        super().__init__()
        self.trip_data = trip_data

        self.setup_ui()

        self.refresh_ui_content()

        self.setStyleSheet(trip_card_stylesheet)

    def setup_ui(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.id_label = QLabel()

        time_widget = QWidget()
        time_layout = QVBoxLayout()
        time_widget.setLayout(time_layout)

        time_layout.addWidget(QLabel(trip_record_start))
        self.start_time_label = QLabel()
        time_layout.addWidget(self.start_time_label)

        time_layout.addWidget(QLabel(trip_record_end))
        self.end_time_label = QLabel()  # Dynamiczny
        time_layout.addWidget(self.end_time_label)

        address_widget = QWidget()
        address_layout = QVBoxLayout()
        address_widget.setLayout(address_layout)

        address_layout.addWidget(QLabel(trip_record_start_address))
        self.start_address_label = QLabel()
        address_layout.addWidget(self.start_address_label)

        address_layout.addWidget(QLabel(trip_record_end_address))
        self.end_address_label = QLabel()
        address_layout.addWidget(self.end_address_label)

        self.driver_label = QLabel()
        self.distance_label = QLabel()
        self.duration_label = QLabel()
        self.ev_duration_label = QLabel()
        self.ev_distance_label = QLabel()
        self.consumption_label = QLabel()
        self.avg_fuel_label = QLabel()
        self.refuel_label = QLabel()
        self.period_label = QLabel()

        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self._on_edit_click)

        # Dodawanie do layoutu
        layout.addWidget(self.id_label)
        layout.addWidget(time_widget)
        layout.addWidget(address_widget)
        layout.addWidget(self.driver_label)
        layout.addWidget(self.distance_label)
        layout.addWidget(self.duration_label)
        layout.addWidget(self.ev_distance_label)
        layout.addWidget(self.ev_duration_label)
        layout.addWidget(self.consumption_label)
        layout.addWidget(self.avg_fuel_label)
        layout.addWidget(self.refuel_label)
        layout.addWidget(self.period_label)
        layout.addWidget(self.edit_button)

    def _on_edit_click(self):

        self.edit_requested.emit(self.trip_data.id)

    def update_data(self, new_data: TripSchema):
        self.trip_data = new_data
        self.refresh_ui_content()

    def refresh_ui_content(self):
        data = self.trip_data

        self.id_label.setText(str(data.id))
        self.start_time_label.setText(data.start_time.strftime('%d.%m.%Y, %H:%M'))
        self.end_time_label.setText(data.end_time.strftime('%d.%m.%Y, %H:%M'))

        if data.driver:
            driver_name = f"{data.driver.name or ''} {data.driver.surname or ''}".strip()
        else:
            driver_name = "Brak kierowcy"
        self.driver_label.setText(driver_name)

        self.distance_label.setText(f"{data.distance:.2f} km")

        time_sec = data.duration
        time_hour = time_sec // 3600
        time_minute = (time_sec % 3600) // 60
        self.duration_label.setText(f"{time_hour}h {time_minute}m")

        ev_dur = data.ev_duration or 0.0
        self.ev_duration_label.setText(f"{ev_dur:.2f} h")

        ev_dist = data.ev_distance or 0.0
        self.ev_distance_label.setText(f"{ev_dist:.2f} h")

        self.consumption_label.setText(f"{data.fuel_consumed:.2f} L")
        self.avg_fuel_label.setText(f"{data.average_fuel_consumed:.2f} L/100km")

        self.refuel_label.setText(map_true if data.refuel else map_false)
        self.period_label.setText(str(data.period))

        self.start_address_label.setText(data.start_address or "\u2014")
        self.end_address_label.setText(data.end_address or "\u2014")