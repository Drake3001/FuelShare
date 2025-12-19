

from sqlalchemy import select, update, delete
from typing import List, Optional

from database.models.users import User
from database.schemas.user_schema import UserSchema, UserCreateSchema, UserUpdateSchema
from database.session import get_session


class UserService:
    def __init__(self):
        self.session_factory = get_session

    def create_user(self, user_dto: UserCreateSchema) -> User:
        with self.session_factory() as db:
            user_data = user_dto.model_dump()
            new_user = User(**user_data)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user

    def get_user(self, user_id: int) -> Optional[User]:
        with self.session_factory() as db:
            query = select(User).where(User.id == user_id)
            result = db.execute(query)
            user = result.scalars().one_or_none()
            return user

    def get_all_users(self) -> List[User]:
        with self.session_factory() as db:
            query = select(User).order_by(User.id)
            result = db.execute(query)
            users = result.scalars().unique().all()
            return list(users)

    def get_users_by_ids(self, user_ids: List[int]) -> List[User]:
        with self.session_factory() as db:
            query = select(User).where(User.id.in_(user_ids))
            result = db.execute(query)
            users = result.scalars().unique().all()
            return list(users)

    def update_user(self, user_schema: UserUpdateSchema) -> Optional[User]:
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
            return result.scalars().one()

    def delete_user(self, user_id: int) -> bool:
        with self.session_factory() as db:
            # Sprawdzenie w tej samej sesji
            check_query = select(User).where(User.id == user_id)
            existing_user = db.execute(check_query).scalar_one_or_none()

            if not existing_user:
                return False

            query = delete(User).where(User.id == user_id)
            db.execute(query)
            db.commit()
            return True

    def get_user_by_email(self, email: str) -> Optional[User]:
        with self.session_factory() as db:
            query = select(User).where(User.email == email)
            result = db.execute(query)
            user = result.scalars().one_or_none()
            return user

    def get_users_schema(self) -> List[UserSchema]:
        users = self.get_all_users()
        return [UserSchema.model_validate(user) for user in users]