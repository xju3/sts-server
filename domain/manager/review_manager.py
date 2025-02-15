
from utils.common import get_date_from_week_id
from domain.model.review import ReviewAI, ReviewRequest, ReviewDetail
from domain.engine import SessionLocal
from utils.common import generate_uuid
from ai.agent.agent import AiReviewInfo
from sqlalchemy import desc
from typing import List

# session = create_session(db_engine)

class ReviewManager:

    def get_student_review_requests(self, student_id: str, date : str) -> List[ReviewRequest]:

        from datetime import datetime, timedelta
        today = datetime.strptime(date, '%Y-%m-%d')
        next_day = today + timedelta(days=1)
        
        with SessionLocal() as session:
            return session.query(ReviewRequest).filter(ReviewRequest.student_id == student_id, 
                                                       ReviewRequest.trans_time > today, 
                                                       ReviewRequest.trans_time < next_day).order_by(desc(ReviewRequest.trans_time)).all()

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


    def get_failed_knowledge_points(self, year_id, week_id):
        """
        查询上周所提交作业中学生的错误知识点，按学科分类
        Returns:
            List of dictionaries containing student_id and their failed knowledge points by subject
            [
                {
                    'student_id': 123,
                    'subjects': [
                        {
                            'subject': 'math',
                            'knowledge_points': ['point1', 'point2', ...]
                        },
                        {
                            'subject': 'physics',
                            'knowledge_points': ['point3', 'point4', ...]
                        }
                    ]
                },
                ...
            ]
        """
        # Dictionary to store nested structure: student_id -> subject -> knowledge_points
        results = {}  
        start_date, end_date = get_date_from_week_id(year_id=year_id, week_id=week_id)
        
        with SessionLocal() as session:
            condition = (ReviewRequest.trans_time >= start_date) & (ReviewRequest.trans_time < end_date)
            # 获取上周有作业提交的学生列表
            requests = session.query(ReviewRequest).filter(condition).all()
            
            for request in requests:
                # 经过AI审核过的作业
                review = self.get_ai_review_by_request_id(request_id=request.id)
                
                # 在查到没有批改记录或全部正确的情况下，跳过
                if review is None or review.correct == review.total == 0:
                    continue
                    
                # 查找错误的作业，同时获取subject字段
                details = session.query(ReviewDetail.knowledge).filter(
                    ReviewDetail.ai_review_id == review.id,
                    ReviewDetail.conclusion != 1
                ).all()
                
                if len(details) == 0:
                    continue
                    
                # 初始化该学生的数据结构（如果还没有）
                if request.student_id not in results:
                    results[request.student_id] = {}
                    
                # 处理每个错误详情
                for detail in details:
                    if detail.knowledge and detail.subject:
                        # 初始化该学科的知识点集合（如果还没有）
                        if detail.subject not in results[request.student_id]:
                            results[request.student_id][detail.subject] = set()
                        
                        # 添加该学科的错误知识点
                        points = detail.knowledge.split(',')
                        for point in points:
                            point = point.strip()
                            if point:
                                results[request.student_id][detail.subject].add(point)
        
        # 转换结果格式
        formatted_results = []
        for student_id, subjects_data in results.items():
            # 只包含有错误知识点的学科
            subjects_list = [
                {
                    'subject': subject,
                    'knowledge_points': list(knowledge_points)
                }
                for subject, knowledge_points in subjects_data.items()
                if knowledge_points  # 只包含有错误知识点的学科
            ]
            
            # 只有当学生有错误知识点时才添加到结果中
            if subjects_list:
                formatted_results.append({
                    'student_id': student_id,
                    'subjects': subjects_list
                })
        
        return formatted_results 