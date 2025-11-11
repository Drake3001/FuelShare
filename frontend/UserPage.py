from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class UserPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_page()

    def setup_page(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel("➕ Dodawanie Nowego Tripu")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
                margin: 20px;
            }
        """)

        content = QLabel("Tu będzie formularz dodawania nowego tripu...")
        content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content.setStyleSheet("font-size: 16px; color: #7f8c8d;")

        layout.addWidget(title)
        layout.addWidget(content)
        layout.addStretch()