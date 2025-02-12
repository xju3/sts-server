from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import Mapped
import uuid

def generate_uuid():
    return str(uuid.uuid1())


class PushMessage:
    def __init__(self, platform, target, content: str) -> None:
        self.platform = platform
        self.target = target
        self.content = content

class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=generate_uuid)