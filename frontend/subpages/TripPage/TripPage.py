import asyncio

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer
from typing import Dict, List
from database.cruds.crud_trip import TripService
from frontend.Widgets.SortingHeader import SortingHeader
from frontend.stylesheets import trip_page_stylesheet
from frontend.Widgets.TripCard import TripCard
from database.schemas.trip_schema import TripSchema
from datetime import datetime
from frontend.const import header_names
from frontend.subpages.TripPage.TripLoader import TripLoader


class TripsListPage(QWidget):
    def __init__(self, trip_service):
        super().__init__()
        self.loader = TripLoader(trip_service)
        self.update_current_trips()
        self.buffer_size = 10
        self.last_loaded_ind=0
        self.all_loaded=False
        self.setup_page()
        self.load_first_widget()
        self.fetch_widgets_and_show()

    def load_first_widget(self):
        if not self.current_trips:
            return

        first_id = self.current_trips[0]
        first_trip = self.loader.all_trips[first_id]

        temp_card = TripCard(first_trip, self.loader.trip_callback)
        self.card_height = temp_card.sizeHint().height()

        viewport_height = self.scroll_area.viewport().height()
        self.chunk_size = max(1, viewport_height // self.card_height) + self.buffer_size

        temp_card.deleteLater()


        print("Wysokość pojedynczej karty:", self.card_height)

    def setup_page(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel("🗂️ Lista Tripów")
        title.setObjectName("page_title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        headers_container = QWidget()
        headers_layout = QHBoxLayout()
        headers_container.setLayout(headers_layout)

        self.headers=[]
        for name in header_names:
            new_header=SortingHeader(name, self.header_callback)
            self.headers.append(new_header)
            headers_layout.addWidget(new_header)
        layout.addWidget(headers_container)

        # Kontener dla kart - NIE scroll area bezpośrednio
        self.cards_container = QWidget()
        self.cards_container.setObjectName("cards_container")
        self.cards_layout = QVBoxLayout()
        self.cards_container.setLayout(self.cards_layout)

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.cards_container)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.verticalScrollBar().valueChanged.connect(self.on_scroll)
        layout.addWidget(self.scroll_area)

        self.setStyleSheet(trip_page_stylesheet)

    def update_current_trips(self, **kwargs):
        self.current_trips=self.loader.filter_trips(**kwargs)

    def on_scroll(self, value):
        if self.all_loaded:
            return
        scroll_bar = self.scroll_area.verticalScrollBar()
        max_value = scroll_bar.maximum()

        if value > max_value * 0.85:
            self.fetch_widgets_and_show()

    def fetch_widgets_and_show(self):
        if self.last_loaded_ind >= len(self.current_trips):
            self.all_loaded = True
            return
        start = self.last_loaded_ind
        end = start + self.chunk_size
        end = min(end, len(self.current_trips))
        to_load = self.current_trips[start:end]
        self.last_loaded_ind = end
        trip_cards = self.loader.get_trip_cards(to_load)
        for trip_card in trip_cards:
            self.cards_layout.addWidget(trip_card)
            trip_card.show()
    def header_callback(self):
        sorting_values: Dict[str, int ]= {}
        for header in self.headers:
            sorting_values[header.get_txt()]= header.get_state()
        print(sorting_values)
