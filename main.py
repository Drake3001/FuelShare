import sys

from database.Services.TripService import TripService
from database.Services.UserService import UserService
from frontend.App import App
from PyQt6.QtWidgets import QMainWindow, QApplication
import qasync
import asyncio


def main():
    app = QApplication(sys.argv)
    trip_service = TripService()
    user_service = UserService()
    window = App(trip_service, user_service)
    window.show()
    app.exec()


if __name__ == '__main__':
    main()