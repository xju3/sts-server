
from domain.model.review import ReviewRequest, ReviewDetail, Assignment
from sqlalchemy.orm import sessionmaker
from utils.common import get_week_ids 
from ai.agent.assignment import AssignmentAgent
from domain.engine import engine 
from domain.manager.task.queue import QueueTaskManager, GenerationTask, TaskStatus
from domain.manager.review_manager import ReviewManager
from domain.manager.gemini_manager import GeminiManager
from utils.minio import get_minio_files, get_minio_file_url
from routers.model.output import ReviewInfo_O, ReviewDetailInfo_O, ReviewRequest_O
from typing import List
import logging, sys
import time
import threading

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger()
review_manager = ReviewManager()
gemini_manager = GeminiManager()



class ReviewService:

    def get_request_by_id(self, request_id):
        request = review_manager.get_request_by_id(request_id=request_id)
        if request is None:
            return {}
        return ReviewRequest_O(id=request_id, images=request.images, studentId=request.student_id)

    def get_request_images(self,request_id) -> List[str]:
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
    
    def set_ai_review_err(self, detail_id):
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        with Session() as session:
            session.query(ReviewDetail).filter(ReviewDetail.id == detail_id).update({"err": 1})
            session.commit()
    
    def get_ai_review_list(self, student_id, date) -> List[ReviewInfo_O]:
        requests = review_manager.get_student_review_requests(student_id, date)
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
        """
            获取AI_REVIEW_ID下的题目列表
        """
        details = []
        list = review_manager.get_ai_review_details(ai_review_id)
        for item in list:
            detail = ReviewDetailInfo_O(id=item.id, 
                                        aiReviewId=item.ai_review_id, 
                                        question=item.question,
                                        options=item.options,
                                        no=item.no, ansAi=item.ans_ai, 
                                        ansStudent=item.ans_student, 
                                        err=item.err,
                                        conclusion=item.conclusion, solution=item.solution, 
                                        knowledge=item.knowledge, suggestion=item.suggestion)
            details.append(detail)
        return details
    
    def gen_weekly_assignments(self):
        generator = QueueTaskManager()
        year_id, week_id = get_week_ids(0)
        Session = sessionmaker(engine)
        task_ids = []
        with Session() as session:
            list = session.query(Assignment).filter(Assignment.year_id == year_id, Assignment.week_id == week_id).all()
            for item in list:
                # 异步方式（使用回调）
                task_id = generator.add_generation_task(
                    subject=item.subject,
                    student_id=item.student_id,
                    knowledge_points=item.points.split(","),
                    callback=self.handle_task_result  # 使用回调函数
                )
                task_ids.append(task_id)
                print(f"Async task started: {task_id}")
        generator.start_worker()
    # 使用示例
    def handle_task_result(self, task: GenerationTask):
        """处理任务结果的回调函数"""
        if task.status == TaskStatus.COMPLETED:
            print(f"Task {task.task_id} completed successfully!")
        else:
            print(f"Task {task.task_id} failed: {task.error_message}")


    def pre_gen_weekly_assignments(self):
        """
            预生成周练习题目任务, 在没有生成题目前，不向用户开放.
        """
        year_id, week_id = get_week_ids(0)
        knowledge_points = review_manager.get_failed_knowledge_points(year_id=year_id, week_id=week_id)
        if len(knowledge_points) == 0:
           return

        Session = sessionmaker(engine)
        with Session() as session:
            for item in knowledge_points:
                student_id = item ['student_id']
                subjects = item ['subjects']
                self.create_assignment(session=session, 
                                       student_id=student_id, 
                                       subjects=subjects, 
                                       year_id=year_id, week_id=week_id )
            session.commit()
                
    
    def create_assignment(self,session, student_id, subjects, year_id, week_id):
        for subject in subjects:
            points = subject['knowledge_points']
            points = ','.join(points)
            name = subject['subject']
            assignment = Assignment(subject=name, student_id=student_id,
                                    year_id= year_id, week_id=week_id, 
                                    status = 0, 
                                    correct = 0,
                                    total=0, points=points)
            session.add(assignment)
            


         
