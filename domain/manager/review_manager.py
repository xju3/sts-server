
from domain.model.review import ReviewAI, ReviewRequest, ReviewDetail
from domain.engine import SessionLocal
from domain.model.common import generate_uuid
from ai.agent.agent import AiReviewInfo
from sqlalchemy import desc
from typing import List

# session = create_session(db_engine)

class ReviewManager:

    def get_student_review_requests(self, student_id) -> List[ReviewRequest]:
        with SessionLocal() as session:
            return session.query(ReviewRequest).filter(ReviewRequest.student_id == student_id).order_by(desc(ReviewRequest.trans_time)).all()

    def get_ai_review_by_request_id(self, request_id) -> ReviewAI:
        with SessionLocal() as session:
            return session.query(ReviewAI).filter(ReviewAI.request_id == request_id).one_or_none()
    
    def get_ai_review_details(self, ai_review_id) -> List[ReviewDetail]:
        with SessionLocal() as session:
            return session.query(ReviewDetail).filter(ReviewDetail.ai_review_id==ai_review_id).all()

    def get_request_by_id(self, request_id) -> ReviewRequest:
        with SessionLocal() as session:
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
            if (problem.options is not None):
                options = ','.join(problem.options)
            else:
                options = None
        
            review_detail = ReviewDetail(ai_review_id=review_ai_id,
                                         no=problem.no,
                                         question=problem.question,
                                         options=options,
                                         ans_student=problem.ans_student,
                                         ans_ai=problem.ans_ai,
                                         conclusion=problem.conclusion,
                                         reason=problem.reason,
                                         knowledge=problem.knowledge,
                                         solution=problem.solution,
                                         suggestion=problem.suggestion)
            details.append(review_detail)
        return review_ai, details
