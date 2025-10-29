# w pliku: database/crud.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload

from .models.trips import Trip
from .schemas.trip_schema import TripSchema
from .schemas.trip_schema import TripCreateSchema


# tripCruds

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