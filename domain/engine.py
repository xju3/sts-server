
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from sqlalchemy.pool import StaticPool


load_dotenv()
db_engine = create_engine(f"postgresql+pg8000://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}@{os.getenv('PG_HOST')}/{os.getenv('PG_DATABASE')}",
                        isolation_level="REPEATABLE READ",
                        poolclass = StaticPool,)