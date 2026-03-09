import asyncio



from frontend.Widgets.SortingHeader import SortingHeader
from frontend.Widgets.TripEditDialog import TripEditDialog
from frontend.Widgets.TripCard import TripCard
from frontend.const import header_names, header_mapping

from frontend.subpages.TripPage.TripsViewModel import TripViewModel

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QHBoxLayout
from typing import Dict
from PyQt6.QtCore import QTimer


class TripsView(QWidget):
    def __init__(self, trip_service, user_service):
        super().__init__()

        self.vm = TripViewModel(trip_service, user_service)

        self.loaded_cards: Dict[int, TripCard] = {}
        self.header_widgets = []

        self.chunk_size = 10
        self.current_offset = 0
        self.is_loading = False
        self.all_loaded = False
        self.headers_enabled = True

        self.setup_ui()

        self.vm.trip_updated.connect(self.on_trip_updated)
        self.vm.content_changed.connect(self.on_data_reload)
        self.vm.trips_added.connect(self.on_data_reload)

        self.load_more_trips()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.headers_container= QWidget()
        self.headers_layout = QHBoxLayout()
        self.headers_container.setLayout(self.headers_layout)



        for display_text, field_name in header_mapping.items():
            header = SortingHeader(display_text, callback=None)
            callback = lambda f=field_name, h=header: self.on_header_clicked(f, h)

            header.callback = callback

            self.header_widgets.append(header)
            self.headers_layout.addWidget(header)

        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout()
        self.cards_container.setLayout(self.cards_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.cards_container)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.verticalScrollBar().valueChanged.connect(self.on_scroll)
        layout.addWidget(self.headers_container)
        layout.addWidget(self.scroll_area)

    def load_more_trips(self):
        if self.all_loaded or self.is_loading:
            return

        self.is_loading = True

        start = self.current_offset
        end = start + self.chunk_size

        new_trips_data = self.vm.get_trips_slice(start, end)

        if not new_trips_data:
            self.all_loaded = True
            self.is_loading = False
            return

        for trip_data in new_trips_data:
            if trip_data.id in self.loaded_cards:
                card = self.loaded_cards[trip_data.id]
                card.setParent(self.cards_container)
                self.cards_layout.addWidget(card)
                card.setVisible(True)
            else:
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
    def on_header_clicked(self, field_name: str, clicked_header):
        if not self.headers_enabled:
            return
        direction = clicked_header.get_state()
        self.vm.header_changed(field_name, direction)


    def open_edit_dialog(self, trip_id):
        trip_data = self.vm.get_trip_by_id(trip_id)
        users = self.vm.get_all_users()

        dialog = TripEditDialog(trip_data, users, parent=self)
        if dialog.exec():
            schema = dialog.get_data()
            self.vm.save_trip_edit(schema)
        dialog.deleteLater()

    def on_trip_updated(self, updated_ids: list[int]):
        print("Aktualizuje widgety",updated_ids)
        count=0
        for trip_id in updated_ids:
            if trip_id in self.loaded_cards:
                fresh_data = self.vm.get_trip_by_id(trip_id)

                if fresh_data:
                    card_widget = self.loaded_cards[trip_id]
                    card_widget.update_data(fresh_data)
                    count+=1
        print(f"Zaktualizowałem {count}")


    def on_data_reload(self):
        QTimer.singleShot(0, self._perform_reload_logic)

    def _perform_reload_logic(self):
        """Właściwa logika przeładowania (to co miałeś w on_data_reload)"""
        if self.is_loading:
            return

        self.is_loading = True

        self.headers_enabled = False

        layout = self.cards_layout

        for card in self.loaded_cards.values():
            layout.removeWidget(card)
            card.setParent(None)

        self.current_offset = 0
        self.all_loaded = False

        sb = self.scroll_area.verticalScrollBar()
        sb.blockSignals(True)
        sb.setValue(0)
        sb.blockSignals(False)
        self.is_loading = False
        self.load_more_trips()
        self.headers_enabled = True

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
