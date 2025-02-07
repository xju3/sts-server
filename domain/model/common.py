from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import text, types, Column, String
import uuid

def generate_uuid():
    return str(uuid.uuid1())

class Base(DeclarativeBase):
    id = Column(primary_key=True, default=generate_uuid)