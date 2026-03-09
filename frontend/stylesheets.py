trip_page_stylesheet = """
/* Stylizacja tylko dla TripsListPage */
TripsListPage {
    background-color: #f5f7fa;
}

TripsListPage QLabel#page_title {
    font-size: 24px;
    font-weight: bold;
    margin: 10px;
}

TripsListPage QScrollArea {
    border: none;
    background-color: transparent;
}

TripsListPage QWidget#cards_container {
    background-color: transparent;
}
"""

trip_card_stylesheet = """
/* ── Karta główna ── */
TripCard {
    background-color: #fafbfc;
    border: 2px solid #cbd5e1;
    border-radius: 14px;
    padding: 0px;
    margin: 6px 4px;
}

TripCard:hover {
    background-color: #f0f2f5;
    border: 2px solid #94a3b8;
}

TripCard QLabel {
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #334155;
    border: none;
    padding: 0px;
    margin: 0px;
}

/* ── Nagłówek (trasa + ID + edit) ── */
QWidget#header_section {
    background-color: #fafbfc;
    border: 2px solid #cbd5e1;
    border-radius: 14px;
    padding: 12px 16px;
}

QLabel#route_label {
    font-size: 15px;
    font-weight: bold;
    color: #1e293b;
}

QLabel#id_badge {
    background-color: #409eff;
    color: #ffffff;
    font-size: 11px;
    font-weight: bold;
    border-radius: 10px;
    padding: 2px 10px;
    max-height: 20px;
}

/* ── Sekcja czasu ── */
QWidget#time_section {
    padding: 8px 16px 4px 16px;
}

QLabel#time_label {
    font-size: 13px;
    color: #475569;
}

/* ── Siatka statystyk ── */
QWidget#stats_section {
    padding: 4px 12px;
}

QWidget#stat_tile {
    background-color: #e2e8f0;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    padding: 10px 8px;
}

QLabel#stat_value {
    font-size: 18px;
    font-weight: bold;
    color: #0f172a;
}

QLabel#stat_caption {
    font-size: 11px;
    color: #64748b;
    font-weight: 500;
}

/* ── Stopka ── */
QWidget#footer_section {
    padding: 4px 16px 12px 16px;
}

QLabel#footer_label {
    font-size: 12px;
    color: #64748b;
}

/* ── Przycisk Edit ── */
TripCard QPushButton#btn_edit {
    background-color: #409eff;
    color: #ffffff;
    border: none;
    padding: 6px 18px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: bold;
}

TripCard QPushButton#btn_edit:hover {
    background-color: #66b1ff;
}

TripCard QPushButton#btn_edit:pressed {
    background-color: #3a8ee6;
}
"""

userRowStyleSheet="""
            UserRowWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
            }
            UserRowWidget:hover {
                background-color: #f9f9f9;
                border: 1px solid #d0d0d0;
            }
            QLabel {
                border: none;
                font-size: 14px;
                color: #333;
            }
            QPushButton {
                background-color: white;
                border: 1px solid #d1d5db;
                border-radius: 4px;
                padding: 5px 10px;
                color: #374151;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #f3f4f6;
                border-color: #9ca3af;
                color: #111827;
            }
            /* Styl specyficzny dla przycisku usuwania (opcjonalnie czerwony przy hover) */
            QPushButton#btn_delete:hover {
                background-color: #fef2f2;
                border-color: #fca5a5;
                color: #dc2626;
            }
        """
reportRowStyleSheet= """
/* ── Wiersz raportu ── */
ReportRowWidget {
    background-color: #fafbfc;
    border: 2px solid #cbd5e1;
    border-radius: 12px;
    margin-bottom: 4px;
}

ReportRowWidget:hover {
    background-color: #f0f2f5;
    border: 2px solid #94a3b8;
}

ReportRowWidget QLabel {
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #334155;
    border: none;
    font-size: 13px;
}

QLabel#report_id {
    font-weight: bold;
    color: #1e293b;
    font-size: 14px;
}

QLabel#report_stat {
    color: #475569;
}

QPushButton#btn_generate {
    background-color: #409eff;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 6px 18px;
    font-size: 12px;
    font-weight: bold;
}

QPushButton#btn_generate:hover {
    background-color: #66b1ff;
}

QPushButton#btn_generate:pressed {
    background-color: #3a8ee6;
}
"""