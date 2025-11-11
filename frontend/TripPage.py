from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt6.QtCore import Qt
from frontend.stylesheets import trip_page_stylesheet
from frontend.Widgets.TripCard import TripCard
from database.schemas.trip_schema import TripSchema
from datetime import datetime


class TripsListPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_page()
        self.load_mock_data()  # Ładujemy mockowane dane

    def setup_page(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel("🗂️ Lista Tripów")
        title.setObjectName("page_title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.cards_container = QWidget()
        self.cards_container.setObjectName("cards_container")
        self.cards_layout = QVBoxLayout()
        self.cards_container.setLayout(self.cards_layout)

        scroll = QScrollArea()
        scroll.setWidget(self.cards_container)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        self.setStyleSheet(trip_page_stylesheet)

    def load_mock_data(self):
        from database.schemas.user_schema import UserSchema

        # Mockowany user
        mock_user = UserSchema(
            id=1,
            name ="Jan",
            surname="Kowalski",
        )

        # Mockowany trip
        mock_trip = TripSchema(
            id=52,
            start_lat=52.2297,
            start_lon=21.0122,
            end_lat=52.4064,
            end_lon=16.9252,
            start_time=datetime(2024, 11, 8, 9, 30),
            end_time=datetime(2024, 11, 8, 12, 45),
            duration=11700,  # 3h15m w sekundach
            distance=310.5,
            fuel_consumed=18.5,
            average_fuel_consumed=5.96,
            ev_distance=None,
            ev_duration=None,
            refuel=True,
            period=1,
            driver=mock_user,
            vehicle=None,
            payers=[]
        )

        trip_card = TripCard(mock_trip)
        self.cards_layout.addWidget(trip_card)