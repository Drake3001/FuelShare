from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .users import User
from .trips import Trip
from .trip_payer import TripPayer
from .vehicle_user import VechicleUser
from .vehicles import Vehicle