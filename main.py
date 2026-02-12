import sys

from database.Services.ReportService import ReportService
from database.Services.TripService import TripService
from database.Services.UserService import UserService
from frontend.App import App
from PyQt6.QtWidgets import QApplication
from background_worker import BackgroundWorker


def main():
    ###setup services
    app = QApplication(sys.argv)
    trip_service = TripService()
    user_service = UserService()
    report_service = ReportService()


    ##setup worker
    worker = BackgroundWorker()
    worker.start()

    window = App(trip_service, user_service, report_service, worker)
    window.show()
    exit_code = app.exec()

    worker.stop()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()