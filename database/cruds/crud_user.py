from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from typing import List, Optional

from database.models.users import User
from database.schemas.user_schema import UserSchema, UserCreateSchema, UserUpdateSchema
from database.session import get_session


class UserService:
    def __init__(self):
        self.session_factory = get_session  # Context manager

    async def create_user(self, user_dto: UserCreateSchema) -> User:
        async with self.session_factory() as db:
            user_data = user_dto.model_dump()
            new_user = User(**user_data)
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            return new_user

    async def get_user(self, user_id: int) -> Optional[User]:
        async with self.session_factory() as db:
            query = select(User).where(User.id == user_id)
            result = await db.execute(query)
            user = result.scalars().one_or_none()
            return user

    async def get_all_users(self) -> List[User]:
        async with self.session_factory() as db:
            query = select(User).order_by(User.id)
            result = await db.execute(query)
            users = result.scalars().all()
            return list(users)

    async def get_users_by_ids(self, user_ids: List[int]) -> List[User]:
        async with self.session_factory() as db:
            query = select(User).where(User.id.in_(user_ids))
            result = await db.execute(query)
            users = result.scalars().all()
            return list(users)

    async def update_user(self, user_schema: UserUpdateSchema) -> Optional[User]:
        async with self.session_factory() as db:
            user_data = user_schema.model_dump(exclude_unset=True)
            user_id = user_schema.id

            # Najpierw sprawdź czy użytkownik istnieje
            existing_user = await self.get_user(user_id)
            if not existing_user:
                return None

            query = update(User).where(User.id == user_id).values(**user_data)
            await db.execute(query)
            await db.commit()

            # Pobierz zaktualizowanego użytkownika
            result = await db.execute(select(User).where(User.id == user_id))
            return result.scalars().one_or_none()

    async def delete_user(self, user_id: int) -> bool:
        async with self.session_factory() as db:
            # Najpierw sprawdź czy użytkownik istnieje
            existing_user = await self.get_user(user_id)
            if not existing_user:
                return False

            query = delete(User).where(User.id == user_id)
            await db.execute(query)
            await db.commit()
            return True

    # Dodatkowe metody pomocnicze
    async def get_user_by_email(self, email: str) -> Optional[User]:
        async with self.session_factory() as db:
            query = select(User).where(User.email == email)
            result = await db.execute(query)
            user = result.scalars().one_or_none()
            return user

    async def get_users_schema(self) -> List[UserSchema]:
        """Zwraca listę użytkowników jako schematy (dla API)"""
        users = await self.get_all_users()
        return [UserSchema.model_validate(user) for user in users]