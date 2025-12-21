from pydantic import BaseModel

class UserBase(BaseModel):
    name: str  | None
    surname: str | None
    email: str | None

class UserCreateSchema(UserBase):
    pass


class UserUpdateSchema(UserBase):
    id: int
    name: str | None = None
    surname: str | None = None
    email: str | None = None

class UserSchema(UserBase):
    id: int
    class Config:
        from_attributes = True
