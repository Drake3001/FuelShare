import sys

from database.cruds.crud_trip import TripService
from frontend.App import App
from PyQt6.QtWidgets import QMainWindow, QApplication
import qasync
import asyncio


def main():
    app = QApplication(sys.argv)
    trip_service = TripService()
    window = App(trip_service)
    window.show()
    app.exec()


if __name__ == '__main__':
    main()