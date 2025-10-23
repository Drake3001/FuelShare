from sqlalchemy import Column, Integer, String
from . import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name= Column(String(50), nullable=False )
    surname= Column(String(50), nullable=False )

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, surname={self.surname})>"