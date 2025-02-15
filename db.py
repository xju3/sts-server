from domain.engine import engine
from domain.model.common import Base
from domain.model.review import ReviewAI
from domain.model.account import Account
from dotenv import load_dotenv

# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)


load_dotenv()
from domain.service.review_service import ReviewService


service = ReviewService()
service.pre_gen_weekly_assignments()