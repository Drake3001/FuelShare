import sys

from frontend.App import App
from PyQt6.QtWidgets import QMainWindow, QApplication

if __name__ == '__main__':
    app= QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())