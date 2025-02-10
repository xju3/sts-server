from domain.engine import engine
from domain.model.common import Base
from domain.model.review import ReviewAI
from domain.model.account import Account

Base.metadata.create_all(engine)