from sqlalchemy import Integer, Column, String, DateTime, Float, Interval, ForeignKey
from . import Base


class Trip(Base):
    __tablename__ = 'trip'

    id = Column(Integer, primary_key=True)

    # Localizations
    start_lat = Column(Float, nullable=False)
    start_lon = Column(Float, nullable=False)
    end_lat = Column(Float, nullable=False)
    end_lon = Column(Float, nullable=False)

    # Times
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    duration = Column(Integer, nullable=False)

    # Distance
    distance = Column(Float, nullable=False)

    # EV informations
    ev_duration = Column(Integer, nullable=True)
    ev_distance = Column(Float, nullable=True)

    # Fuel
    fuel_consumed = Column(Float, nullable=False)
    average_fuel_consumed = Column(Float, nullable=False)

    #UserDriving
    user = Column(Integer, ForeignKey('user.id'), nullable=True)


    def __repr__(self):
        return (f"Trip(id={self.id}, start=({self.start_lat}, {self.start_lon}), "
                f"end=({self.end_lat}, {self.end_lon}), start_time={self.start_time}, "
                f"end_time={self.end_time}, duration={self.duration}, distance={self.distance}, "
                f"fuel={self.fuel_consumed}, avg_fuel={self.average_fuel_consumed})")