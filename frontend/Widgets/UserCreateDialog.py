from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout, QLineEdit, QFormLayout
from typing import List

from database.schemas.user_schema import UserCreateSchema
from frontend.const import CreateUserDialogTitle, user_fields


class UserCreateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.input_fields: List = []
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName(CreateUserDialogTitle)
        layout = QFormLayout()

        for name in user_fields:
            self.input_fields.append(QLineEdit())
            layout.addRow(name, self.input_fields[-1])

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_data(self):
        return UserCreateSchema(name=self.input_fields[0].text(), surname=self.input_fields[1].text(), email=self.input_fields[2].text())
