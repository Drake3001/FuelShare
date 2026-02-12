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
/* Stylizacja tylko dla TripCard - wyższy priorytet */
TripCard {
    background-color: #ffffff;
    border: 5px solid #e1e5e9;
    border-radius: 12px;
    padding: 16px;
    margin: 8px;
    min-height: 120px;
}

TripCard QLabel {
    font-family: 'Segoe UI', Arial, sans-serif;
}

TripCard QLabel:first-child {
    font-weight: bold;
    border: 5px solid #e1e5e9;
    color: #409eff;
    font-size: 14px;
}

TripCard QPushButton {
    background-color: #409eff;
    color: white;
    border: none;
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: bold;
}

TripCard QPushButton:hover {
    background-color: #66b1ff;
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
            ReportRowWidget {
                background-color: #ffffff;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                margin-bottom: 2px;
            }
            ReportRowWidget:hover {
                background-color: #f8f9fa;
                border: 1px solid #0078d7;
            }
            QLabel {
                color: #333333;
                font-size: 13px;
                font-family: 'Segoe UI', Arial;
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                border-radius: 4px;
                padding: 6px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:pressed {
                background-color: #004578;
            }
        """