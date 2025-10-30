# w pliku: database/crud.py
from dotenv.cli import unset
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import update

from .models.trips import Trip
from .schemas.trip_schema import TripSchema, TripUpdateSchema
from .schemas.trip_schema import TripCreateSchema
from datetime import datetime


# tripCRUDS
#TRIP CREATE
async def create_all_trips(db: AsyncSession, dtos: list[TripCreateSchema]):
    new_trips = []
    for dto in dtos:
        trip_data= dto.model_dump()
        new_trip = Trip(**trip_data)
        new_trips.append(new_trip)

    db.add_all(new_trips)
    await db.commit()
    print(f"Pomyślnie dodano {len(new_trips)} przejazdów do bazy.")

async def create_trip(db: AsyncSession,trip_dto: TripCreateSchema,) -> Trip:
    trip_data = trip_dto.model_dump()
    new_trip = Trip(**trip_data)
    db.add(new_trip)
    await db.commit()
    await db.refresh(new_trip)
    return new_trip


#TRIP READ
async def get_all_trips(db: AsyncSession) -> list[TripSchema]:
    """
    Pobiera wszystkie przejazdy, "chętnie" (eagerly) ładując powiązane
    obiekty, aby uniknąć problemu N+1.
    """

    query = (
        select(Trip)
        .options(
            # Załaduj kierowcę (User) używając JOIN
            joinedload(Trip.driver),

            # Załaduj pojazd (Vehicle) używając JOIN
            joinedload(Trip.vehicle),

            # Załaduj listę płacących (User) używając 
            # osobnego zapytania SELECT...IN...
            selectinload(Trip.payers)
        )
        .order_by(Trip.start_time.desc())
    )

    result = await db.execute(query)

    # Używamy .unique(), aby SQLAlchemy poprawnie obsłużyło 
    # zduplikowane wiersze z JOIN-ów
    sqlalchemy_trips = result.scalars().unique().all()

    # Kiedy Pydantic (z orm_mode=True) poprosi o trip.driver 
    # lub trip.payers, SQLAlchemy zobaczy, że te dane są już
    # załadowane w pamięci i NIE wykona żadnych nowych zapytań.
    return [TripSchema.model_validate(trip) for trip in sqlalchemy_trips]
async def get_one_trip(db: AsyncSession, trip_id: int) -> TripSchema| None:
    query= select(Trip).where(Trip.id == trip_id)
    db_trip = await db.execute(query)
    return db_trip.one_or_none()

# TRIP UPDATE
async def update_trip(db: AsyncSession, trip_update: TripUpdateSchema) -> Trip | None:
    data = trip_update.model_dump(exclude_unset=True)
    trip_id = data.pop("id", None)
    if not trip_id:
        raise ValueError("TripUpdateSchema must include 'id'")

    query = (
        update(Trip)
        .where(Trip.id == trip_id)
        .values(**data)
    )

    result = await db.execute(query)
    updated_trip = result.scalar_one_or_none()

    await db.commit()
    return updated_trip



async def batch_update_trips(db: AsyncSession, updates: list[TripUpdateSchema]):
    if not updates:
        return
    update_mappings = [
        dto.model_dump(exclude_unset=True) for dto in updates
    ]
    await db.run_sync(
        lambda sync_session: sync_session.bulk_update_mappings(Trip, update_mappings)
    )
    modified_refuels= [u.id for u in updates if u.id is not None]
    if not modified_refuels:
        await db.commit()
        return

    query = (
        select(Trip.start_time, Trip.period, Trip.refuel)
        .where(Trip.id.in_(modified_refuels))
        .order_by(Trip.start_time.asc())
    )
    result = (await db.execute(query)).all()
    start_time, period, refuel = result[0]
    if period is not None:
        if Trip.refuel:
            period+=1
        else:
            period-=1
    else:
        period=1
    query =(
        select(Trip.id, Trip.refuel)
        .where(Trip.start_time>=start_time)
        .order_by(Trip.start_time.asc())
    )
    period_adjustment= (await db.execute(query)).all()
    print(len(period_adjustment))
    updates_to_commit= reevaluate_periods(period_adjustment, period)
    await db.run_sync(lambda s: s.bulk_update_mappings(Trip, updates_to_commit))

    await db.commit()

def reevaluate_periods( trip_ids:[(int, str)], start_period: int):
    period= start_period
    result = []
    for (trip_id, refuel) in trip_ids:
        if refuel:
            period += 1
        result.append({"id": trip_id, "period": period})
    return result
