from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget, QHBoxLayout

from database.Services.ReportService import ReportService
from database.Services.UserService import UserService
from frontend.subpages.ReportPage.ReportView import ReportView
from frontend.subpages.TripPage.TripsView import TripsView
from frontend.subpages.UserPage.UserView import UserPage
from database.Services.TripService import TripService
from scripts.geocoder import geocoder
from scripts.synctrips import synctrips
from datetime import datetime, timezone


class App(QMainWindow):
    def __init__(self, trip_service: TripService, user_service: UserService, report_service: ReportService, worker=None):
        super().__init__()
        self.stacked_widget = None
        self.trips_list_page = None
        self.add_trip_page = None

        #Services
        self.trip_service = trip_service
        self.user_service = user_service
        self.report_service = report_service

        # Background worker do zadań async
        self.worker = worker
        if self.worker:
            self.worker.task_finished.connect(self.on_task_done)
            self.worker_call_for_trips()
        self.batch_size = 10

        #setup
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

        self.setup_pages()

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
        self.trips_btn = QPushButton("Lista Tripów")
        self.trips_btn.clicked.connect(self.show_trips_list)

        # Przycisk użytkownicy (na przyszłość)
        self.users_btn = QPushButton("Użytkownicy")
        self.users_btn.clicked.connect(self.show_users)

        self.reports_btn = QPushButton("Raporty")
        self.reports_btn.clicked.connect(self.show_reports)

        layout.addWidget(self.trips_btn)
        layout.addWidget(self.users_btn)
        layout.addWidget(self.reports_btn)
        layout.addStretch()

        return nav_widget

    def setup_pages(self):
        self.trips_list_page = TripsView(self.trip_service, self.user_service)
        self.stacked_widget.addWidget(self.trips_list_page)


        self.users_page = UserPage(userService=self.user_service)
        self.stacked_widget.addWidget(self.users_page)

        self.reports_page= ReportView(trip_service=self.trip_service, report_service=self.report_service)
        self.stacked_widget.addWidget(self.reports_page)



    def show_trips_list(self):
        self.stacked_widget.setCurrentWidget(self.trips_list_page)
        self.update_navigation_style(self.trips_btn)


    def show_users(self):
        self.stacked_widget.setCurrentWidget(self.users_page)
        self.update_navigation_style(self.users_btn)


    def show_reports(self):
        self.stacked_widget.setCurrentWidget(self.reports_page)
        self.update_navigation_style(self.reports_btn)

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


    def worker_call_for_trips(self):
        last_trip = self.trip_service.get_last_trip_date()
        start_date = last_trip or datetime(2026, 1, 20, tzinfo=timezone.utc)
        self.worker.submit("sync_trips", synctrips, start_date)


    def worker_geo_service_setup(self):
        self.missing_geolocations=self.trip_service.get_all_trips_noLocation()
        batch = self.missing_geolocations[:self.batch_size]
        self.missing_geolocations = self.missing_geolocations[len(batch):]
        script = geocoder
        self.worker.submit("geo_service", script, batch)



    def on_task_done(self, task_name, result):
        if task_name == "sync_trips":
            print("koniec sync trips zrobione ")
            if result:
                self.trip_service.create_all_trips(result)
            self.worker_geo_service_setup()
        if task_name == "geo_service":
            self.trip_service.batch_update_addresses(result)
            print("batch skończony")
            if len(self.missing_geolocations)!=0:
                batch= self.missing_geolocations[:self.batch_size]
                self.missing_geolocations=self.missing_geolocations[self.batch_size:]
                if len(batch)>0:
                    script = geocoder
                    self.worker.submit("geo_service",script,batch)



