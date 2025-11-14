from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload, Session
from typing import List, Optional

from database.models.trips import Trip
from database.schemas.trip_schema import TripSchema, TripUpdateSchema, TripCreateSchema
from database.session import get_session


class TripService:
    def __init__(self):
        self.session_factory = get_session

    def create_all_trips(self, dtos: List[TripCreateSchema]):
        """Tworzenie wielu tripów naraz"""
        with self.session_factory() as db:
            new_trips = []
            for dto in dtos:
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

    def update_trip(self, trip_update: TripUpdateSchema) -> Optional[Trip]:
        """Aktualizacja pojedynczego tripa"""
        with self.session_factory() as db:
            data = trip_update.model_dump(exclude_unset=True)
            trip_id = data.pop("id", None)
            if not trip_id:
                raise ValueError("TripUpdateSchema must include 'id'")

            # Pobierz trip do aktualizacji
            query = select(Trip).where(Trip.id == trip_id)
            result = db.execute(query)
            trip = result.scalar_one_or_none()

            if not trip:
                return None

            # Zaktualizuj pola
            for key, value in data.items():
                setattr(trip, key, value)

            db.commit()
            db.refresh(trip)
            return trip

    def batch_update_trips(self, updates: List[TripUpdateSchema]):
        """Batch update wielu tripów z przeliczaniem okresów"""
        if not updates:
            return

        with self.session_factory() as db:
            update_mappings = [
                dto.model_dump(exclude_unset=True) for dto in updates
            ]

            # Bulk update
            db.bulk_update_mappings(Trip, update_mappings)

            modified_refuels = [u.id for u in updates if u.id is not None]
            if not modified_refuels:
                db.commit()
                return

            # Logika okresów
            query = (
                select(Trip.start_time, Trip.period, Trip.refuel)
                .where(Trip.id.in_(modified_refuels))
                .order_by(Trip.start_time.asc())
            )
            result = (db.execute(query)).all()

            if not result:
                db.commit()
                return

            start_time, period, refuel = result[0]
            if period is not None:
                if refuel:
                    period += 1
                else:
                    period -= 1
            else:
                period = 1

            query = (
                select(Trip.id, Trip.refuel)
                .where(Trip.start_time >= start_time)
                .order_by(Trip.start_time.asc())
            )
            period_adjustment = db.execute(query).all()

            updates_to_commit = self.__reevaluate_periods(period_adjustment, period)
            db.bulk_update_mappings(Trip, updates_to_commit)
            db.commit()

    def __reevaluate_periods(self, trip_ids: List, start_period: int):
        period = start_period
        result = []
        for (trip_id, refuel) in trip_ids:
            if refuel:
                period += 1
            result.append({"id": trip_id, "period": period})
        return result