# frontend/Widgets/TripEditDialog.py

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QComboBox,
                             QDialogButtonBox, QGroupBox, QFormLayout,
                             QWidget, QCheckBox, QListWidget, QListWidgetItem)
from PyQt6.QtCore import Qt
from typing import List

from database.schemas.trip_schema import TripUpdateSchema
from database.schemas.user_schema import UserSchema


class TripEditDialog(QDialog):
    def __init__(self, trip_data, all_users: List[UserSchema], parent=None):
        super().__init__(parent)
        self.trip = trip_data
        self.all_users = all_users

        self.setWindowTitle(f"Edycja Przejazdu #{trip_data.id}")
        self.resize(500, 700)
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # --- SEKCJA INFO (READ-ONLY) ---
        info_group = QGroupBox("Read-only Ifno")
        info_group.setStyleSheet("""
            QGroupBox { font-weight: bold; border: 1px solid #ddd; border-radius: 6px; margin-top: 10px; padding-top: 10px; }
            QLabel { color: #555; }
        """)
        info_layout = QFormLayout()
        info_layout.addRow("Start:", QLabel(f"{self.trip.start_time.strftime('%d.%m.%Y, %H:%M')}"))
        info_layout.addRow("Koniec:", QLabel(f"{self.trip.end_time.strftime('%d.%m.%Y, %H:%M')}"))
        info_layout.addRow("Dystans:", QLabel(f"{self.trip.distance:.2f} km"))
        info_layout.addRow("Zużycie:", QLabel(f"{self.trip.fuel_consumed:.2f} L"))
        info_group.setLayout(info_layout)
        self.layout.addWidget(info_group)

        self.layout.addSpacing(10)

        # --- SEKCJA EDYCJI ---
        edit_label = QLabel("Pola do edycji")
        edit_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        self.layout.addWidget(edit_label)

        driver_label = QLabel("👤 Kierowca")
        driver_label.setStyleSheet("font-weight: bold; margin-top: 5px;")
        self.layout.addWidget(driver_label)

        self.driver_combo = QComboBox()
        self.driver_combo.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 4px;")
        self.layout.addWidget(self.driver_combo)

        payers_label = QLabel("💳 Płatnicy")
        payers_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        self.layout.addWidget(payers_label)

        self.payers_list = QListWidget()
        self.payers_list.setFixedHeight(120)  # Ograniczamy wysokość, żeby nie zajęło całego okna
        self.payers_list.setStyleSheet("border: 1px solid #ccc; border-radius: 4px;")
        self.layout.addWidget(self.payers_list)

        self.refuel_check = QCheckBox("Tankowanie przed przejazdem?")
        self.refuel_check.setStyleSheet("margin-top: 10px; font-weight: bold;")
        self.layout.addWidget(self.refuel_check)

        self.layout.addStretch()

        # --- PRZYCISKI ---
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)

    def load_data(self):
        # --- Ładowanie Kierowców ---
        self.driver_combo.addItem("Nie przypisano", None)
        current_driver_index = 0

        for i, user in enumerate(self.all_users):
            display_name = f"{user.name} {user.surname}"
            # Dodajemy ID usera jako `userdata` itemu
            self.driver_combo.addItem(display_name, user.id)

            if self.trip.driver and user.id == self.trip.driver.id:
                current_driver_index = i + 1

        self.driver_combo.setCurrentIndex(current_driver_index)

        # --- Ładowanie Payers ---
        current_payer_ids = [p for p in self.trip.payer_ids] if self.trip.payer_ids else []

        for user in self.all_users:
            display_name = f"{user.name} {user.surname}"
            item = QListWidgetItem(display_name)
            item.setData(Qt.ItemDataRole.UserRole, user.id)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)

            if user.id in current_payer_ids:
                item.setCheckState(Qt.CheckState.Checked)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)

            self.payers_list.addItem(item)

        self.refuel_check.setChecked(bool(self.trip.refuel))

    def get_data(self):

        selected_driver_id = self.driver_combo.currentData()
        selected_payer_ids = []
        for i in range(self.payers_list.count()):
            item = self.payers_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                user_id = item.data(Qt.ItemDataRole.UserRole)
                selected_payer_ids.append(user_id)
        res = TripUpdateSchema(
            id=self.trip.id,
            driver_id=selected_driver_id,
            refuel=self.refuel_check.isChecked(),
            payer_ids=selected_payer_ids
        )
        return res
