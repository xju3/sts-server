
from domain.model.review import ReviewAI, ReviewRequest, ReviewDetail
from domain.engine import session 
from domain.model.common import generate_uuid
from sqlalchemy import select, desc
from typing import List


class ReviewManager:

    def get_student_review_requests(self, student_id) -> List[ReviewRequest]:
        return session.execute(select(ReviewRequest).where(ReviewRequest.student_id == student_id)).fetchall()

    def get_ai_review_by_request_id(self, request_id) -> ReviewAI:
        return session.execute(select(ReviewAI).where(ReviewAI.request_id == request_id)).scalar_one_or_none()

    def get_request_by_id(self, request_id) -> ReviewRequest:
        return session.execute(select(ReviewRequest).where(ReviewRequest.id == request_id)).scalar_one_or_none()

    def create_ai_review_info(self, request_id: str, review_info):
        review_ai_id = generate_uuid()
        review_ai = ReviewAI(id=review_ai_id, 
                             request_id=request_id,
                             summary=review_info.summary,
                             total=review_info.total,
                             correct=review_info.correct,
                             incorrect=review_info.incorrect,
                             uncertain=review_info.uncertain)
        details = []
        for problem in review_info.problems:
            review_detail = ReviewDetail(request_ai_id=review_ai_id,
                                         no=problem.no,
                                         ans_student=problem.ans_student,
                                         ans_ai=problem.ans_ai,
                                         conclusion=problem.conclusion,
                                         reason=problem.reason,
                                         knowledges=problem.knowledges,
                                         solution=problem.solution,
                                         suggestions=problem.suggestions)
            details.append(review_detail)
        return review_ai, details
