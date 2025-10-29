from sqlalchemy import Integer, Column, String, DateTime, Float, Interval, ForeignKey
from sqlalchemy.orm import relationship

from . import Base

class Vehicle(Base):
    __tablename__ = "vehicle"
    id = Column(Integer, primary_key=True)
    vin_number= Column(String, nullable=False)
    trips= relationship("Trip", back_populates="vehicle")

    def __repr__(self):
        return f"<Vehicle {self.id}, {self.vin_number}>"


