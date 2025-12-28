from gc import callbacks

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Dict

from database.schemas.user_schema import UserSchema
from frontend.Widgets.UserCreateDialog import UserCreateDialog
from frontend.Widgets.UserDeleteDialog import UserDeleteDialog
from frontend.Widgets.UserRowWidget import UserRowWidget
from frontend.const import create_user_button
from frontend.subpages.UserPage.UserViewModel import UserViewModel


class UserPage(QWidget):

    def __init__(self, userService):
        super().__init__()
        self.vm = UserViewModel(userService)
        self.loadedUserRows: Dict[int, UserRowWidget] = {}
        self.load_user_data()
        self.setup_page()

    def setup_page(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        top_panel= QWidget()
        top_panel_layout = QVBoxLayout()
        top_panel.setLayout(top_panel_layout)

        create_button = QPushButton(create_user_button)
        create_button.clicked.connect(self.on_create_button_clicked)




        title = QLabel("Użytkownicy")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)


        content =QWidget()
        self.content_layout = QVBoxLayout()
        content.setLayout(self.content_layout)

        for row in self.loadedUserRows.values():
            self.content_layout.addWidget(row)



        top_panel_layout.addWidget(title)
        top_panel_layout.addWidget(create_button)

        layout.addWidget(top_panel)
        layout.addWidget(content)
        layout.addStretch()

    def load_user_data(self):
        userList = self.vm.getAllUsers()
        for entry in userList:
            if entry.id not in self.loadedUserRows:
                userRow = UserRowWidget(entry)
                self.loadedUserRows[entry.id] = userRow
                userRow.on_edit_click.connect(self.on_edit_button_clicked)
                userRow.on_delete_click.connect(self.on_delete_button_clicked)


    def updateOrAppend(self, schema: UserSchema):
        if schema.id not in self.loadedUserRows:
            userRow = UserRowWidget(schema)
            self.loadedUserRows[schema.id] = userRow
            userRow.on_edit_click.connect(self.on_edit_button_clicked)
            userRow.on_delete_click.connect(self.on_delete_button_clicked)
            self.content_layout.addWidget(userRow)
        else:
            self.loadedUserRows[schema.id].update_data(schema)


    ###Eventy
    def on_create_button_clicked(self):
        dialog = UserCreateDialog(parent=self)
        if dialog.exec():
            schema = dialog.get_data()
            created = self.vm.createUser(schema)
            self.updateOrAppend(created)
        dialog.deleteLater()

    def on_delete_button_clicked(self, id:int, name: str):
        dialog = UserDeleteDialog(parent=self, id=id, name= name)
        if dialog.exec():
            id = dialog.get_id()
            deleted_id = self.vm.deleteUser(id)
            if deleted_id!=-1:
                self.content_layout.removeWidget(self.loadedUserRows[id])
                self.loadedUserRows[id].deleteLater()

        dialog.deleteLater()

    def on_edit_button_clicked(self, id: int ):
        print(f"to jest edit dostałe {id}")



