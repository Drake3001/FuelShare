from dotenv.cli import unset
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete

from database.models.users import User
from database.schemas.user_schema import UserSchema, UserCreateSchema, UserUpdateSchema


async def create_user(db: AsyncSession, user_dto: UserCreateSchema) -> User:
    user_data=user_dto.model_dump()
    new_user=User(**user_data)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user(db: AsyncSession, user_id) -> User | None:
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalars().one_or_none()
    return user


async def update_user(db: AsyncSession, user_schema: UserUpdateSchema) -> User | None:
    user_data = user_schema.model_dump(exclude_unset=True)
    user_id = user_schema.id

    query = update(User).where(User.id == user_id).values(**user_data)
    await db.execute(query)
    await db.commit()

    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().one_or_none()


async def delete_user(db: AsyncSession, user_id)->  None:
    query = delete(User).where(User.id == user_id)
    result = await db.execute(query)
