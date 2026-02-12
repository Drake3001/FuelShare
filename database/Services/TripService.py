from sqlalchemy import select, func, asc, desc
from sqlalchemy.orm import joinedload, selectinload
from typing import List, Optional, Tuple

from database.models.trips import Trip
from database.models.users import User
from database.schemas.trip_schema import TripSchema, TripUpdateSchema, TripCreateSchema
from database.session import get_session
from datetime import datetime


class TripService:
    def __init__(self):
        self.session_factory = get_session

    def create_all_trips(self, dtos: List[TripCreateSchema]):
        with self.session_factory() as db:
            new_trips = []
            for dto in dtos[::-1]:
                trip_data = dto.model_dump()
                new_trip = Trip(**trip_data)
                new_trips.append(new_trip)

            db.add_all(new_trips)
            db.commit()
            print(f"Pomyślnie dodano {len(new_trips)} przejazdów do bazy.")

    def create_trip(self, trip_dto: TripCreateSchema) -> Trip:
        """Tworzenie pojedynczego tripa"""
        with self.session_factory() as db:
            trip_data = trip_dto.model_dump()
            new_trip = Trip(**trip_data)
            db.add(new_trip)
            db.commit()
            db.refresh(new_trip)
            return new_trip

    def get_all_trips(self) -> List[TripSchema]:
        """Pobieranie wszystkich tripów z relacjami"""
        with self.session_factory() as db:
            query = (
                select(Trip)
                .options(
                    joinedload(Trip.driver),
                    joinedload(Trip.vehicle),
                    selectinload(Trip.payers)
                )
                .order_by(Trip.start_time.desc())
            )

            result = db.execute(query)
            sqlalchemy_trips = result.scalars().unique().all()
            return [TripSchema.model_validate(trip) for trip in sqlalchemy_trips]

    def get_one_trip(self, trip_id: int) -> Optional[TripSchema]:
        """Pobieranie pojedynczego tripa"""
        with self.session_factory() as db:
            query = select(Trip).where(Trip.id == trip_id)
            result = db.execute(query)
            trip = result.scalar_one_or_none()
            return TripSchema.model_validate(trip) if trip else None

    def update_trip(self, trip_update: TripUpdateSchema) -> (Optional[TripSchema], List[int]):
        with self.session_factory() as db:
            data = trip_update.model_dump(exclude_unset=True)

            trip_id = data.pop("id")
            payer_ids = data.pop("payer_ids", None)

            stmt = select(Trip).where(Trip.id == trip_id).options(selectinload(Trip.payers))
            trip = db.execute(stmt).scalar_one_or_none()

            if not trip:
                return None

            old_start_time = trip.start_time

            for key, value in data.items():
                if hasattr(trip, key):
                    setattr(trip, key, value)

            if payer_ids is not None:
                if payer_ids:
                    users_stmt = select(User).where(User.id.in_(payer_ids))
                    new_payers = db.execute(users_stmt).scalars().all()
                    trip.payers = list(new_payers)
                else:
                    trip.payers = []

            db.flush()

            recalc_start_time = min(old_start_time, trip.start_time)
            modified_trips=self._recalculate_periods_from(db, recalc_start_time)

            db.commit()

            result_query = (
                select(Trip)
                .where(Trip.id == trip_id)
                .options(
                    joinedload(Trip.driver),
                    joinedload(Trip.vehicle),
                    selectinload(Trip.payers)
                )
            )
            updated_trip = db.execute(result_query).scalar_one()

            return TripSchema.model_validate(updated_trip), modified_trips

    def get_incomplete_trips(self) -> List[TripSchema]:
        """Zwraca tripy bez przypisanego kierowcy LUB bez płatników"""
        with self.session_factory() as db:
            query = (
                select(Trip)
                .options(joinedload(Trip.driver), selectinload(Trip.payers))
                .where(
                    (Trip.driver_id == None) | (~Trip.payers.any())
                )
                .order_by(Trip.start_time.desc())
            )
            result = db.execute(query).scalars().unique().all()
            return [TripSchema.model_validate(t) for t in result]

    def _recalculate_periods_from(self, db, start_time: datetime) -> List[Tuple[int, int]]:

        prev_trip_query = (
            select(Trip)
            .where(Trip.start_time < start_time)
            .order_by(Trip.start_time.desc())
            .limit(1)
        )
        prev_trip = db.execute(prev_trip_query).scalar_one_or_none()

        if prev_trip and prev_trip.period:
            current_period = prev_trip.period
        else:
            current_period = 0

        future_trips_query = (
            select(Trip)
            .where(Trip.start_time >= start_time)
            .order_by(Trip.start_time.asc())
        )
        future_trips = db.execute(future_trips_query).scalars().all()
        modified_trips=[]
        for trip in future_trips:
            if trip.refuel:
                current_period += 1
            if trip.period != current_period:
                trip.period = current_period
            modified_trips.append((trip.id, trip.period))
        return modified_trips

    def get_trips_by_user_id(self, user_id: int) -> List[TripSchema]:
        with self.session_factory() as db:
            query = (
                select(Trip)
                .options(joinedload(Trip.driver), selectinload(Trip.payers))
                .where(
                    (Trip.driver_id == user_id) | (~Trip.payers)
                )
                .order_by(Trip.start_time.desc())
            )
    def get_unique_periods_and_count(self):
        with self.session_factory() as db:
            query = (
                select(Trip.period, func.count(Trip.id), func.count(Trip.id).filter(Trip.driver_id == None).label("anonymous_trips"))
                .group_by(Trip.period)
                .order_by(Trip.period.asc().nulls_last())
            )
            result = db.execute(query).all()
            return result
    def get_last_trip_date(self):
        with self.session_factory() as db:
            query = (
                select(Trip.end_time)
                .order_by(Trip.start_time.desc())
                .limit(1)
            )
            result = db.execute(query).scalar()
        return result
