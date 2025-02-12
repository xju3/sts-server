
from domain.model.review import ReviewRequest
from sqlalchemy.orm import sessionmaker
from domain.engine import engine 
from domain.manager.review_manager import ReviewManager
from domain.manager.gemini_manager import GeminiManager
from domain.manager.minio_manager import get_minio_files, get_minio_file_url
from routers.model.output import ReviewInfo_O, ReviewDetailInfo_O, ReviewRequest_O
from typing import List
import logging, sys
import threading

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger()
review_manager = ReviewManager()
gemini_manager = GeminiManager()

class ReviewService:

    def get_request_by_id(request_id):
        request = review_manager.get_request_by_id(request_id=request_id)
        if request is None:
            return {}
        return ReviewRequest_O(id=request_id, images=request.images, studentId=request.student_id)

    def get_request_origin_images(request_id) -> List[str]:
        request = review_manager.get_request_by_id(request_id=request_id)
        if request is None:
            return []
        dir = f'{request.student_id}/{request.id}/'
        return get_minio_file_url(directory=dir)


    def create(self, student_id, request_id, images):
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = Session()
        try:
            request = ReviewRequest(student_id=student_id, id = request_id, images=images)
            session.add(request)
            session.commit()
            p = threading.Thread(target=self.call_ai, args=(student_id, request_id,))
            p.start()
        except Exception as e:
            logger.error(e)
            session.rollback()  
        finally:
            session.close() 
            
    def call_ai(self, student_id, request_id):
        minio_objects = get_minio_files(f"{student_id}/{request_id}/")
        files = list(map(lambda obj: obj.object_name, minio_objects))
        gemini_manager.review(student_id=student_id, request_id=request_id, files =files)

    def get_student_review_requests(self, student_id):
        return review_manager.get_student_review_requests(student_id)
    
    def get_ai_review_list(self, student_id) -> List[ReviewInfo_O]:
        requests = review_manager.get_student_review_requests(student_id)
        if len(requests) == 0:
            return []
        
        results = []
        for request in requests:
            ai_review = review_manager.get_ai_review_by_request_id(request_id=request.id)
            if ai_review is None:
                continue
            review = ReviewInfo_O(requestId= request.id, 
                                  trans_time=request.trans_time, 
                                  images=request.images,
                                  start_time=ai_review.start_time, end_time=ai_review.end_time, 
                                  subject = ai_review.subject, 
                                  total = ai_review.total, 
                                  correct= ai_review.correct, incorrect= ai_review.incorrect, uncertain= ai_review.uncertain, 
                                  summary= ai_review.summary,id = ai_review.id, details=[])
            review.details = self.get_review_details(review.id)
            results.append(review)
        return results

    def get_review_details(self, ai_review_id) -> List[ReviewDetailInfo_O]: 
        details = []
        list = review_manager.get_ai_review_details(ai_review_id)
        for item in list:
            detail = ReviewDetailInfo_O(id=item.id, 
                                        aiReviewId=item.ai_review_id, 
                                        question=item.question,
                                        options=item.options,
                                        no=item.no, ansAi=item.ans_ai, 
                                        ansStudent=item.ans_student, 
                                        conclusion=item.conclusion, solution=item.solution, 
                                        knowledge=item.knowledge, suggestion=item.suggestion)
            details.append(detail)
        return details
