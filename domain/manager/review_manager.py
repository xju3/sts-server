
from domain.model.review import ReviewAI, ReviewRequest, ReviewDetail
from domain.engine import db_engine
from domain.model.common import generate_uuid
from model.agent import AiReviewInfo
from sqlalchemy import desc
from sqlalchemy.orm import create_session
from typing import List

session = create_session(db_engine)

class ReviewManager:

    def get_student_review_requests(self, student_id) -> List[ReviewRequest]:
        return session.query(ReviewRequest).filter(ReviewRequest.student_id == student_id).order_by(desc(ReviewRequest.trans_time)).all()

    def get_ai_review_by_request_id(self, request_id) -> ReviewAI:
        return session.query(ReviewAI).filter(ReviewAI.request_id == request_id).one_or_none()
    
    def get_ai_review_details(self, ai_review_id) -> List[ReviewDetail]:
        return session.query(ReviewDetail).filter(ReviewDetail.ai_review_id==ai_review_id).all()

    def get_request_by_id(self, request_id) -> ReviewRequest:
        return session.query(ReviewRequest).filter(ReviewRequest.id == request_id).one_or_none()

    def create_ai_review_info(self, request_id: str, agent_review_info : AiReviewInfo):
        review_ai_id = generate_uuid()
        review_ai = ReviewAI(id=review_ai_id, 
                             request_id=request_id,
                             subject=agent_review_info.subject,
                             summary=agent_review_info.summary,
                             total=agent_review_info.total,
                             correct=agent_review_info.correct,
                             incorrect=agent_review_info.incorrect,
                             uncertain=agent_review_info.uncertain)
        details = []
        for problem in agent_review_info.problems:
            review_detail = ReviewDetail(ai_review_id=review_ai_id,
                                         no=problem.no,
                                         ans_student=problem.ans_student,
                                         ans_ai=problem.ans_ai,
                                         conclusion=problem.conclusion,
                                         reason=problem.reason,
                                         knowledge=problem.knowledge,
                                         solution=problem.solution,
                                         suggestion=problem.suggestion)
            details.append(review_detail)
        return review_ai, details
