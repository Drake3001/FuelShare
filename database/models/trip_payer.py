from sqlalchemy import Integer, Column, String, DateTime, Float, Interval, ForeignKey
from . import Base

class TripPayer(Base):
    __tablename__ = "trip_payer"
    trip_id = Column(Integer, ForeignKey('trip.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
