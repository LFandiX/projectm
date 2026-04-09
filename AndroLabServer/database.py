from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

# SQLite database (file akan dibuat otomatis jika belum ada)
engine = create_engine(
    "sqlite:///mydb.db",
    echo=False,
    future=True
)

db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # Import models agar semua table terdaftar ke metadata
    import models
    Base.metadata.create_all(bind=engine)
