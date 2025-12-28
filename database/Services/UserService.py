from PyQt6.QtCore import QObject, pyqtSignal
from sqlalchemy import select, update, delete
from typing import List, Optional

from database.models.users import User
from database.schemas.user_schema import UserSchema, UserCreateSchema, UserUpdateSchema
from database.session import get_session


class UserService(QObject):
    user_data_changed = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.session_factory = get_session

    def create_user(self, user_dto: UserCreateSchema) -> UserSchema:
        with self.session_factory() as db:
            user_data = user_dto.model_dump()
            new_user = User(**user_data)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return UserSchema.model_validate(new_user)

    def get_user(self, user_id: int) -> Optional[UserSchema]:
        with self.session_factory() as db:
            query = select(User).where(User.id == user_id)
            result = db.execute(query)
            user = result.scalars().one_or_none()

            if user:
                return UserSchema.model_validate(user)
            return None

    def get_all_users(self) -> List[UserSchema]:
        with self.session_factory() as db:
            query = select(User).order_by(User.id)
            result = db.execute(query)
            users = result.scalars().unique().all()

            return [UserSchema.model_validate(u) for u in users]

    def get_users_by_ids(self, user_ids: List[int]) -> List[UserSchema]:
        with self.session_factory() as db:
            query = select(User).where(User.id.in_(user_ids))
            result = db.execute(query)
            users = result.scalars().unique().all()

            return [UserSchema.model_validate(u) for u in users]

    def update_user(self, user_schema: UserUpdateSchema) -> Optional[UserSchema]:
        with self.session_factory() as db:
            user_data = user_schema.model_dump(exclude_unset=True)
            user_id = user_data.pop("id", None)

            check_query = select(User).where(User.id == user_id)
            existing_user = db.execute(check_query).scalar_one_or_none()

            if not existing_user:
                return None

            query = update(User).where(User.id == user_id).values(**user_data)
            db.execute(query)
            db.commit()


            result = db.execute(select(User).where(User.id == user_id))
            updated_user = result.scalars().one()
            self.user_data_changed.emit(updated_user.id)
            return UserSchema.model_validate(updated_user)

    def delete_user(self, user_id: int) -> bool:
        """
        Tutaj zwracamy bool, więc schema nie jest potrzebna,
        ale logika pozostaje ta sama.
        """
        with self.session_factory() as db:
            check_query = select(User).where(User.id == user_id)
            existing_user = db.execute(check_query).scalar_one_or_none()

            if not existing_user:
                return False

            query = delete(User).where(User.id == user_id)
            db.execute(query)
            db.commit()
            self.user_data_changed.emit(user_id)
            return True

    def get_user_by_email(self, email: str) -> Optional[UserSchema]:
        with self.session_factory() as db:
            query = select(User).where(User.email == email)
            result = db.execute(query)
            user = result.scalars().one_or_none()

            if user:
                return UserSchema.model_validate(user)
            return None
