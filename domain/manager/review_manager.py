
from domain.model.review import ReviewAI, ReviewRequest, ReviewDetail
from domain.engine import db_engine
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from typing import List

read_session = Session(db_engine)

class ReviewManager:
    def get_student_review_requests(self, student_id) -> List[ReviewRequest]:
        return read_session.execute(select(ReviewRequest).where(ReviewRequest.student_id == student_id)).fetchall()

    def get_ai_review_by_request_id(self, request_id) -> ReviewAI:
        return read_session.execute(select(ReviewAI).where(ReviewAI.request_id == request_id)).scalar_one_or_none()