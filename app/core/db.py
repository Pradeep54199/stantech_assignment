from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database
from app.core.settings import get_settings, AppSettings


# --------------------------------------------------------------------
# Load settings and build DSN
# --------------------------------------------------------------------
config: AppSettings = get_settings()
db_url = config.postgres.pg_dsn

# --------------------------------------------------------------------
# Create engine 
# --------------------------------------------------------------------
engine = create_engine(db_url, echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --------------------------------------------------------------------
# Database initialization functions
# --------------------------------------------------------------------
def init_database() -> None:
    """
    Ensures the PostgreSQL database and tables exist.
    """
    if not database_exists(engine.url):
        create_database(engine.url)
        print(f"Database created at: {engine.url}")
    else:
        print(f"Database already exists: {engine.url}")
    
    create_tables()


def create_tables() -> None:
    """Creates all SQLAlchemy model tables if they don't exist."""
    print("Creating tables (if not exist)...")
    import app.models
    # noqa: F401 to register models
    Base.metadata.create_all(bind=engine)

    print("Tables created:")
    for tbl in Base.metadata.tables:
        print(f" - {tbl}")


def get_db():
    """
    Automatically closes session on exit.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



