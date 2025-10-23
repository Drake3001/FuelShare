import datetime
import logging

from database.session import get_session, init_db
from database.models.users import User
from mtoyconn.synctrips import synctrips

# logging.basicConfig(level=logging.ERROR)
logging.disable(logging.CRITICAL)

# logging.getLogger("httpx").setLevel(logging.WARNING)
# logging.getLogger("pytoyoda").setLevel(logging.WARNING)
# logging.getLogger("urllib3").setLevel(logging.WARNING)

import asyncio
import os

import dotenv
from pytoyoda import *
from dotenv import load_dotenv, find_dotenv
from database import session
async def test():
    dotenv.load_dotenv(dotenv.find_dotenv())
    username = os.getenv("TOYOTA_USERNAME")
    password = os.getenv("TOYOTA_PASSWORD")
    client = MyT(username=username, password=password, use_metric=True)
    await client.login()
    vehicles = await client.get_vehicles()
    for vehicle in vehicles:
        await vehicle.update()
        print(f"Dashboard: {vehicle.dashboard}")
        print(f'Data {vehicle.vin}')
        trips= await vehicle.get_trips(from_date=datetime.date(year=2025, month=10, day=1), to_date=datetime.date(year=2025, month=10, day=17))
        i=1
        for trip in trips:
            print(f"Trip{i}: {trip}")
            i+=1


async def database_test():
    await init_db()
    async with get_session() as session:
        new_user = User(name="Kuba", surname="Kowalski")
        session.add(new_user)
        await session.commit()

async def script_test():
    trip_data= await synctrips(datetime.datetime(2025, 10, 13),
                datetime.datetime(2025, 10, 17))
    async with get_session() as session:
        for entry in trip_data:
            session.add(entry)
        await session.commit()


if __name__ == '__main__':
    # asyncio.run(test())
    asyncio.run(database_test())
    # asyncio.run(script_test())
