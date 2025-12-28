from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QLabel, QPushButton,
                             QFrame, QApplication, QVBoxLayout, QStyle)
from PyQt6.QtCore import Qt, pyqtSignal

from database.schemas.user_schema import UserSchema
from frontend.stylesheets import userRowStyleSheet
###TO DO podłączyć te callbacki w kóńcu

class UserRowWidget(QFrame):
    on_edit_click = pyqtSignal(int)
    on_delete_click = pyqtSignal(int, str)

    def __init__(self, user: UserSchema, parent=None):
        super().__init__(parent)
        self.user = user
        self.setup_ui()
        self.setup_styles()
        self.update_data(user)

    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(10)
        self.setLayout(layout)

        # 1. ID
        self.lbl_id = QLabel()  # Inicjalizacja pusta
        self.lbl_id.setFixedWidth(40)
        self.lbl_id.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        # 2. Imię
        self.lbl_name = QLabel()
        self.lbl_name.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        # 3. Nazwisko
        self.lbl_surname = QLabel()
        self.lbl_surname.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        # 4. Email
        self.lbl_email = QLabel()
        self.lbl_email.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.lbl_email.setStyleSheet("color: #666; font-style: italic;")

        # Przyciski
        self.btn_edit = QPushButton(" Edytuj")
        self.btn_delete = QPushButton(" Usuń")

        self.btn_edit.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView))
        self.btn_delete.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon))


        self.btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_delete.clicked.connect(self.on_delete_button_clicked)
        self.btn_edit.clicked.connect(self.on_edit_button_clicked)

        actions_layout = QHBoxLayout()
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(5)
        actions_layout.addWidget(self.btn_edit)
        actions_layout.addWidget(self.btn_delete)

        actions_container = QWidget()
        actions_container.setLayout(actions_layout)

        layout.addWidget(self.lbl_id, 0)
        layout.addWidget(self.lbl_name, 2)
        layout.addWidget(self.lbl_surname, 2)
        layout.addWidget(self.lbl_email, 3)
        layout.addWidget(actions_container, 0)

    def setup_styles(self):
        self.setStyleSheet(userRowStyleSheet)
        self.btn_delete.setObjectName("btn_delete")

    def update_data(self, user: UserSchema):
        self.user = user

        # Aktualizacja tekstów w labelkach
        self.lbl_id.setText(str(self.user.id))
        self.lbl_name.setText(self.user.name or "-")
        self.lbl_surname.setText(self.user.surname or "-")
        self.lbl_email.setText(self.user.email or "-")
    def on_delete_button_clicked(self):
        self.on_delete_click.emit(self.user.id, (self.user.name+' '+self.user.surname))
    def on_edit_button_clicked(self):
        self.on_edit_click.emit(self.user.id)