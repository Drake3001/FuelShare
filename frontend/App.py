import sys
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QStackedWidget, QHBoxLayout
from frontend.TripPage import TripsListPage
from frontend.UserPage import UserPage

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stacked_widget = None
        self.trips_list_page = None
        self.add_trip_page = None

        self.setup_main_window()
        self.setup_ui()

    def setup_main_window(self):
        self.setWindowTitle("Trip Manager")
        self.setGeometry(100, 100, 1200, 800)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        header = self.create_header()
        main_layout.addWidget(header)

        nav_bar = self.create_navigation_bar()
        main_layout.addWidget(nav_bar)

        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Inicjalizacja stron
        self.setup_pages()

        # Ustaw domyślną stronę
        self.show_trips_list()

    def create_header(self):
        header_widget = QWidget()
        header_widget.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                padding: 15px;
                border-bottom: 2px solid #34495e;
            }
        """)

        layout = QHBoxLayout()
        header_widget.setLayout(layout)

        # Tytuł aplikacji
        title = QLabel("🚗 Trip Manager")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
        """)

        layout.addWidget(title)
        layout.addStretch()

        # Status lub informacje użytkownika
        status = QLabel("Zalogowany: Admin")
        status.setStyleSheet("color: #ecf0f1;")
        layout.addWidget(status)

        return header_widget

    def create_navigation_bar(self):
        nav_widget = QWidget()
        nav_widget.setStyleSheet("""
            QWidget {
                background-color: #34495e;
                padding: 10px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                margin: 0 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton.active {
                background-color: #e74c3c;
            }
        """)

        layout = QHBoxLayout()
        nav_widget.setLayout(layout)

        # Przycisk listy tripów
        self.trips_btn = QPushButton("📋 Lista Tripów")
        self.trips_btn.clicked.connect(self.show_trips_list)

        # Przycisk użytkownicy (na przyszłość)
        self.users_btn = QPushButton("👥 Użytkownicy")
        self.users_btn.clicked.connect(self.show_users)

        layout.addWidget(self.trips_btn)
        layout.addWidget(self.users_btn)
        layout.addStretch()

        return nav_widget

    def setup_pages(self):
        # Strona 1: Lista tripów
        self.trips_list_page = TripsListPage()
        self.stacked_widget.addWidget(self.trips_list_page)


        # Strona 4: Użytkownicy (placeholder)
        self.users_page = UserPage()
        self.stacked_widget.addWidget(self.users_page)


    def show_trips_list(self):
        self.stacked_widget.setCurrentWidget(self.trips_list_page)
        self.update_navigation_style(self.trips_btn)


    def show_users(self):
        self.stacked_widget.setCurrentWidget(self.users_page)
        self.update_navigation_style(self.users_btn)

    def update_navigation_style(self, active_button):
        # Reset wszystkich przycisków
        buttons = [self.trips_btn, self.users_btn]

        for btn in buttons:
            style = btn.styleSheet()
            if 'active' in style:
                style = style.replace('QPushButton.active', 'QPushButton')
            btn.setStyleSheet(style)

        active_style = active_button.styleSheet()
        if 'QPushButton {' in active_style:
            active_style = active_style.replace('QPushButton {', 'QPushButton.active {')
        active_button.setStyleSheet(active_style)