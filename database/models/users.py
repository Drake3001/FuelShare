from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name= Column(String(50), nullable=False )
    surname= Column(String(50), nullable=False )
    trips_driven = relationship("Trip", back_populates="driver")
    trips_paid= relationship("Trip", back_populates="payers", secondary="trip_payer")


    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, surname={self.surname})>"

