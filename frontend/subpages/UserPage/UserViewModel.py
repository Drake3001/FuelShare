from PyQt6.QtCore import QObject

from database.Services.UserService import UserService
from database.schemas.user_schema import UserCreateSchema, UserUpdateSchema


class UserViewModel(QObject):

    def __init__(self, userService: UserService):
        super().__init__()
        self.userService = userService

    def createUser(self, schema: UserCreateSchema):
        new_user= self.userService.create_user(schema)
        return new_user

    def updateUser(self, schema: UserUpdateSchema):
        edited_user = self.userService.update_user(schema)
        return edited_user

    def getAllUsers(self):
        users = self.userService.get_all_users()
        return users
    def deleteUser(self, id: int):
        if id:
            executed = self.userService.delete_user(id)
            if executed:
                return id
            else:
                return -1






