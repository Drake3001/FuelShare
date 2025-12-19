import asyncio

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer
from typing import Dict, List

from database.schemas.trip_schema import TripUpdateSchema
from frontend.Widgets.TripEditDialog import TripEditDialog
from frontend.Widgets.TripCard import TripCard

from frontend.subpages.TripPage.TripsViewModel import TripViewModel

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel
from typing import Dict


class TripsView(QWidget):
    def __init__(self, trip_service, user_service):
        super().__init__()

        self.vm = TripViewModel(trip_service, user_service)

        self.loaded_cards: Dict[int, TripCard] = {}

        self.chunk_size = 10
        self.current_offset = 0
        self.is_loading = False
        self.all_loaded = False

        self.setup_ui()

        self.vm.trip_updated.connect(self.on_trip_updated)
        self.vm.data_changed.connect(self.on_data_reload)

        self.load_more_trips()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout()
        self.cards_container.setLayout(self.cards_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.cards_container)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.verticalScrollBar().valueChanged.connect(self.on_scroll)

        layout.addWidget(self.scroll_area)

    def load_more_trips(self):
        """Pobiera kolejną paczkę danych z ViewModelu i tworzy karty"""
        if self.all_loaded:
            return
        self.is_loading = True  # Blokujemy kolejne wywołania

        start = self.current_offset
        end = start + self.chunk_size

        new_trips_data = self.vm.get_trips_slice(start, end)

        if not new_trips_data:
            self.all_loaded = True
            self.is_loading = False
            print("Osiągnięto koniec listy.")
            return


        for trip_data in new_trips_data:
            if trip_data.id not in self.loaded_cards:
                self.create_card(trip_data)

        self.current_offset += len(new_trips_data)

        if len(new_trips_data) < self.chunk_size:
            self.all_loaded = True

        self.is_loading = False

    def create_card(self, trip_data):
        card = TripCard(trip_data)

        card.edit_requested.connect(self.open_edit_dialog)

        self.loaded_cards[trip_data.id] = card
        self.cards_layout.addWidget(card)

    # --- OBSŁUGA ZDARZEŃ ---

    def open_edit_dialog(self, trip_id):
        trip_data = self.vm.get_trip_by_id(trip_id)
        users = self.vm.get_all_users()

        dialog = TripEditDialog(trip_data, users, parent=self)
        if dialog.exec():
            schema = dialog.get_data()
            self.vm.save_trip_edit(schema)
        dialog.deleteLater()

    def on_trip_updated(self, updated_ids: list[int]):
        count = 0
        for trip_id in updated_ids:
            if trip_id in self.loaded_cards:
                fresh_data = self.vm.get_trip_by_id(trip_id)

                if fresh_data:
                    card_widget = self.loaded_cards[trip_id]
                    card_widget.update_data(fresh_data)
                    count += 1

        print(f"Zaktualizowano {count} widgetów w miejscu (ID: {updated_ids}).")

    def on_data_reload(self):
        print("Pełny reload listy...")

        # Usuwanie starych widgetów
        for card in self.loaded_cards.values():
            card.deleteLater()
        self.loaded_cards.clear()

        # Resetowanie offsetu i ładowanie od nowa
        self.current_offset = 0
        self.load_more_trips()

    def on_scroll(self, value):
        if self.is_loading or self.all_loaded:
            return

        scroll_bar = self.scroll_area.verticalScrollBar()
        maximum = scroll_bar.maximum()

        if maximum == 0:
            return


        threshold = maximum * 0.85

        if value >= threshold:
            self.load_more_trips()