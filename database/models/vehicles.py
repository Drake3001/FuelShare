from sqlalchemy import Integer, Column, String, DateTime, Float, Interval, ForeignKey
from . import Base


class Vehicle(Base):
    __tablename__ = "vehicle"
    id = Column(Integer, primary_key=True)
    vin_number= Column(String, nullable=False)

    def __repr__(self):
        return f"<Vehicle {self.id}, {self.vin_number}>"