
from domain.model.review import ReviewRequest
from sqlalchemy.orm import Session
from domain.engine import db_engine
from domain.manager.review_manager import ReviewManager
from domain.manager.gemini_manager import GeminiManager
from message.dto import ReviewInfo
from domain.manager.minio_manager import MinioManager
from typing import List
import multiprocessing
import uuid

session  = Session(db_engine)
review_manager = ReviewManager()
minio_manager = MinioManager()
gemini_manager = GeminiManager()

class ReviewService:

    def create(self, student_id, request_id):
        request = ReviewRequest(student_id=student_id, id = request_id)
        session.add(request)
        session.commit()
        multiprocessing.Process(self.call_ai, args=(f'{student_id/request_id}',))
    
    def call_ai(self, directory,):
        minio_objects = minio_manager.get_files(directory)
        files = list(map(lambda obj: obj.object_name, minio_objects))
        gemini_manager.review(directory=directory, files =files)

    
    def get_student_review_requests(self, student_id):
        return review_manager.get_student_review_requests(student_id)
    
    def get_ai_review_list(self, student_id) -> List[ReviewInfo]:
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


