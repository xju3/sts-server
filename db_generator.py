from domain.engine import db_engine
from domain.model.review import ReviewAI
from domain.model.account import Account


ReviewAI.metadata.create_all(db_engine)
Account.metadata.create_all(db_engine)