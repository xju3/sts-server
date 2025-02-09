
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from dotenv import load_dotenv
import os
from sqlalchemy.pool import StaticPool


load_dotenv()
url = f"postgresql+psycopg2://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}@{os.getenv('PG_HOST')}/{os.getenv('PG_DATABASE')}";
engine = create_engine(
    url,
    pool_size=20,  # Maximum number of connections in the pool (default is 5)
    max_overflow=10,  # Maximum number of connections that can be created beyond pool_size (default is 10)
    pool_recycle=3600,  # Recycle connections after 1 hour (in seconds). Helps prevent stale connections
    pool_timeout=30, # Timeout for getting a connection from the pool (default is 30 seconds)
    echo=False # Set to True for debugging. Prints SQL statements.
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()