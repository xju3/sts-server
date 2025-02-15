from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import Mapped
from utils.common import generate_uuid



class PushMessage:
    def __init__(self, platform, target, content: str) -> None:
        self.platform = platform
        self.target = target
        self.content = content

class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=generate_uuid)