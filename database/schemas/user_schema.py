from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    surname: str

class UserCreateSchema(BaseModel):
    pass

class UserUpdateSchema(UserCreateSchema):
    name: str | None = None
    surname: str | None = None

class UserSchema(UserBase):
    id: int
    class Config:
        orm_mode = True
