from PyQt6.QtCore import QObject

from database.Services.ReportService import ReportService
from database.Services.TripService import TripService


class ReportViewModel(QObject):
    def __init__(self,trip_service: TripService, report_service: ReportService,  parent=None):
        super().__init__(parent)
        self.periods = []
        self.trip_service = trip_service
        self.report_service = report_service
        self.load_periods()

    def load_periods(self):
        self.periods=self.trip_service.get_unique_periods_and_count()

    def get_periods_data(self):
        return self.periods

    def generate_report(self, period_id):
        self.report_service.generate_report(period_id)

