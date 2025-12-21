from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox
from PyQt6.QtCore import Qt

from frontend.const import user_delete_dialog


class UserDeleteDialog(QDialog):
    def __init__(self, name: str, id: int, parent=None):
        super().__init__(parent)
        self.name = name
        self.id = id

        self.setWindowTitle("Usuwanie użytkownika")
        self.setUpUI()

    def setUpUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        msg_text = user_delete_dialog(self.name)


        label = QLabel(msg_text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No
        )

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout.addWidget(self.button_box)

    def get_id(self) -> int:
        return self.id