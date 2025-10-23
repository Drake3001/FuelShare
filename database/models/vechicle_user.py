from sqlalchemy import Integer, Column, String, DateTime, Float, Interval, ForeignKey
from . import Base

class VechicleUser(Base):
    __tablename__ = "vechicle_user"
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    vehicle_id= Column(Integer, ForeignKey('vehicle.id'), primary_key=True)