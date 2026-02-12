from PyQt6.QtWidgets import QWidget, QVBoxLayout

from database.Services.ReportService import ReportService
from database.Services.TripService import TripService
from frontend.Widgets.ReportRowWidget import ReportRowWidget
from frontend.subpages.ReportPage.ReportViewModel import ReportViewModel


class ReportView(QWidget):
    def __init__(self,trip_service: TripService, report_service: ReportService,  parent=None):
        super().__init__(parent)
        self.vm = ReportViewModel(trip_service=trip_service, report_service=report_service)
        self.loaded_report_row = []
        self.setupPage()

    def setupPage(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        period_data = self.vm.get_periods_data()
        for entry in period_data:
            widget = ReportRowWidget(entry)
            widget.on_generate_clicked.connect(self.on_generate_button_clicked)
            self.loaded_report_row.append(widget)
            layout.addWidget(widget)

    def on_generate_button_clicked(self, period_id):
        self.vm.generate_report(period_id)









