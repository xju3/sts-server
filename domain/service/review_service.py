
from domain.model.review import ReviewRequest
from sqlalchemy.orm import Session
from domain.engine import db_engine
from domain.manager.review_manager import ReviewManager
from message.dto import ReviewInfo
from typing import List
import multiprocessing
import uuid

session  = Session(db_engine)
review_manager = ReviewManager()

class ReviewService:

    def create(self, student_id, directory):
        request_id = uuid.uuid4()
        request = ReviewRequest(student_id=student_id, directory=directory)
        session.add(request)
        session.commit()
        multiprocessing.Process(self.call_ai, args=(request_id, directory))
    
    def call_ai(self, request_id, directory):
        pass
    
    def get_student_review_requests(self, student_id):
        return review_manager.get_student_review_requests(student_id)
    
    def get_ai_review_list(student_id) -> List[ReviewInfo]:
        requests = review_manager.get_student_review_requests(student_id)
        if len(requests) == 0:
            return None
        
        results = []
        for request in requests:
            ai_review = review_manager.get_ai_review_by_request_id(request.id)
            if ai_review is None:
                continue
            review = ReviewInfo(request_time=request.trans_time, 
                                start_time=ai_review.start_time, end_time=ai_review.end_time,
                                subject = ai_review.subject, 
                                total = ai_review.total, 
                                correct= ai_review.correct, incorrect= ai_review.in_correct, uncertain= ai_review.uncertain, 
                                summary= ai_review.summary)
            results.append(review)
        return results


