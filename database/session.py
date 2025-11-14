import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from .models import Base

load_dotenv()
DB_PATH = os.getenv("DATABASE_PATH")
DB_URL = f"sqlite:///{DB_PATH}"

# Tworzenie katalogu na bazę danych jeśli nie istnieje
db_dir = os.path.dirname(DB_PATH)
if db_dir and not os.path.exists(db_dir):
    os.makedirs(db_dir)

# Synchroniczny engine
# check_same_thread=False pozwala używać z różnych wątków (WAŻNE dla QThread!)
engine = create_engine(
    DB_URL,
    echo=False,
    connect_args={"check_same_thread": False}  # Kluczowe dla threading!
)

# Synchroniczny session maker
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

@contextmanager
def get_session() -> Session:
    """Context manager dla synchronicznej sesji"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def init_db():
    """Inicjalizacja bazy danych - tworzenie tabel"""
    Base.metadata.create_all(bind=engine)