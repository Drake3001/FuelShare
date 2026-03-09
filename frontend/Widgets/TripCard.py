# frontend/Widgets/TripCard.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout,
    QSizePolicy, QStyleOption, QStyle
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPainter
from database.schemas.trip_schema import TripSchema
from frontend.const import map_true, map_false
from frontend.stylesheets import trip_card_stylesheet


class TripCard(QWidget):
    edit_requested = pyqtSignal(int)

    def __init__(self, trip_data: TripSchema):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.trip_data = trip_data

        self.setup_ui()
        self.refresh_ui_content()
        self.setStyleSheet(trip_card_stylesheet)

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, painter, self)
        painter.end()

    # ── UI ──────────────────────────────────────────────────

    def setup_ui(self):
        root = QVBoxLayout()
        root.setContentsMargins(2, 2, 2, 2)
        root.setSpacing(0)
        self.setLayout(root)

        # ── 1. Nagłówek ──
        header = QWidget()
        header.setObjectName("header_section")
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(16, 10, 16, 10)
        header.setLayout(header_layout)

        self.route_label = QLabel()
        self.route_label.setObjectName("route_label")
        self.route_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self.id_badge = QLabel()
        self.id_badge.setObjectName("id_badge")
        self.id_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.edit_button = QPushButton("✎ Edit")
        self.edit_button.setObjectName("btn_edit")
        self.edit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.edit_button.clicked.connect(self._on_edit_click)

        header_layout.addWidget(self.route_label)
        header_layout.addWidget(self.id_badge)
        header_layout.addWidget(self.edit_button)

        # ── 2. Sekcja czasu ──
        time_section = QWidget()
        time_section.setObjectName("time_section")
        time_layout = QVBoxLayout()
        time_layout.setContentsMargins(16, 8, 16, 4)
        time_layout.setSpacing(2)
        time_section.setLayout(time_layout)

        self.start_time_label = QLabel()
        self.start_time_label.setObjectName("time_label")
        self.end_time_label = QLabel()
        self.end_time_label.setObjectName("time_label")

        time_layout.addWidget(self.start_time_label)
        time_layout.addWidget(self.end_time_label)

        # ── 3. Siatka statystyk ──
        stats_section = QWidget()
        stats_section.setObjectName("stats_section")
        stats_grid = QGridLayout()
        stats_grid.setContentsMargins(12, 4, 12, 4)
        stats_grid.setSpacing(8)
        stats_section.setLayout(stats_grid)

        self.stat_labels = {}
        stat_defs = [
            ("distance",    "Dystans"),
            ("duration",    "Czas"),
            ("fuel",        "Paliwo"),
            ("avg_fuel",    "Śr. zużycie"),
        ]
        for col, (key, caption) in enumerate(stat_defs):
            tile = QWidget()
            tile.setObjectName("stat_tile")
            tile_layout = QVBoxLayout()
            tile_layout.setContentsMargins(8, 6, 8, 6)
            tile_layout.setSpacing(2)
            tile_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            tile.setLayout(tile_layout)

            val_lbl = QLabel()
            val_lbl.setObjectName("stat_value")
            val_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

            cap_lbl = QLabel(caption)
            cap_lbl.setObjectName("stat_caption")
            cap_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

            tile_layout.addWidget(val_lbl)
            tile_layout.addWidget(cap_lbl)

            stats_grid.addWidget(tile, 0, col)
            self.stat_labels[key] = val_lbl

        # ── 4. Stopka ──
        footer = QWidget()
        footer.setObjectName("footer_section")
        footer_layout = QVBoxLayout()
        footer_layout.setContentsMargins(16, 4, 16, 10)
        footer_layout.setSpacing(2)
        footer.setLayout(footer_layout)

        self.ev_label = QLabel()
        self.ev_label.setObjectName("footer_label")
        self.details_label = QLabel()
        self.details_label.setObjectName("footer_label")
        self.driver_label = QLabel()
        self.driver_label.setObjectName("footer_label")

        footer_layout.addWidget(self.ev_label)
        footer_layout.addWidget(self.details_label)
        footer_layout.addWidget(self.driver_label)

        # ── Dodanie sekcji do roota ──
        root.addWidget(header)
        root.addWidget(time_section)
        root.addWidget(stats_section)
        root.addWidget(footer)

    # ── Dane ────────────────────────────────────────────────

    def _on_edit_click(self):
        self.edit_requested.emit(self.trip_data.id)

    def update_data(self, new_data: TripSchema):
        self.trip_data = new_data
        self.refresh_ui_content()

    def refresh_ui_content(self):
        d = self.trip_data

        # Nagłówek – trasa
        start_addr = d.start_address or "—"
        end_addr = d.end_address or "—"
        self.route_label.setText(f"{start_addr}  →  {end_addr}")
        self.id_badge.setText(f"#{d.id}")

        # Czas
        self.start_time_label.setText(
            f"🕐  Start: {d.start_time.strftime('%d.%m.%Y, %H:%M')}"
        )
        self.end_time_label.setText(
            f"🏁  Koniec: {d.end_time.strftime('%d.%m.%Y, %H:%M')}"
        )

        # Statystyki
        time_sec = d.duration
        time_hour = time_sec // 3600
        time_minute = (time_sec % 3600) // 60

        self.stat_labels["distance"].setText(f"{d.distance:.1f} km")
        self.stat_labels["duration"].setText(f"{time_hour}h {time_minute}m")
        self.stat_labels["fuel"].setText(f"{d.fuel_consumed:.2f} L")
        self.stat_labels["avg_fuel"].setText(f"{d.average_fuel_consumed:.1f} L/100")

        # Stopka
        ev_dist = d.ev_distance or 0.0
        ev_dur = d.ev_duration or 0.0
        self.ev_label.setText(
            f"⚡ EV: {ev_dist:.1f} km / {ev_dur:.1f} h"
        )

        refuel_txt = map_true if d.refuel else map_false
        period_txt = str(d.period) if d.period else "—"
        self.details_label.setText(
            f"⛽ Tankowanie: {refuel_txt}  ·  📋 Okres: {period_txt}"
        )

        if d.driver:
            name = f"{d.driver.name or ''} {d.driver.surname or ''}".strip()
        else:
            name = "Brak kierowcy"
        self.driver_label.setText(f"👤 {name}")