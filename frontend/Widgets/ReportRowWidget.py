from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QHBoxLayout,
    QStyleOption, QStyle, QSizePolicy
)

from frontend.stylesheets import reportRowStyleSheet


class ReportRowWidget(QWidget):
    on_generate_clicked = pyqtSignal(int)

    def __init__(self, stats, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        # Obsługa przypadku, gdy period_num to None (Twoje zapytanie z SQL)
        self.period_num = stats[0] if stats[0] is not None else 0
        self.count = stats[1]
        self.unfilled = stats[2]

        self.setup_ui()
        self.apply_styles()
        self.refresh_data()

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, painter, self)
        painter.end()

    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(20)
        self.setLayout(layout)

        # Okres (ID badge)
        self.lbl_id = QLabel()
        self.lbl_id.setObjectName("report_id")
        self.lbl_id.setFixedWidth(100)

        # Statystyki
        self.lbl_count = QLabel()
        self.lbl_count.setObjectName("report_stat")
        self.lbl_count.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self.lbl_unfilled = QLabel()
        self.lbl_unfilled.setObjectName("report_stat")
        self.lbl_unfilled.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        if self.period_num != 0:
            self.gen_button = QPushButton('📄 Generuj Raport')
            self.gen_button.setObjectName("btn_generate")
            self.gen_button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.gen_button.clicked.connect(self.on_generate)

        layout.addWidget(self.lbl_id)
        layout.addWidget(self.lbl_count, 1)
        layout.addWidget(self.lbl_unfilled, 1)
        if self.period_num != 0:
            layout.addWidget(self.gen_button)

    def apply_styles(self):
        self.setStyleSheet(reportRowStyleSheet)

    def refresh_data(self):
        p_text = f"📋 Okres: {self.period_num}" if self.period_num != 0 else "Brak ID"
        self.lbl_id.setText(p_text)
        self.lbl_count.setText(f"Suma: {self.count}")
        self.lbl_unfilled.setText(f"Bez UserID: {self.unfilled}")

    def on_generate(self):
        self.on_generate_clicked.emit(self.period_num)