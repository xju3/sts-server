from flask import Blueprint, request
from routers.common import success
from domain.service.review_service import ReviewService

review_router = Blueprint('review_router', __name__)
review_service = ReviewService()



@review_router.put('/review/request/create/<string:studentId>/<string:requestId>/<int:images>')
def create(studentId, requestId, images):
    """
        Function: 创建作业检查请求
    """
    review_service.create(studentId, requestId, images)
    return success([])

@review_router.route('/review/request/get', methods=['POST'])
def get_requests():
    """
        Function: 获取指定学生的作业记录.
    """
    student_id = request.form.get("student_id")
    data = review_service.get_student_review_requests(student_id)
    return success(data)

@review_router.get('/review/request/images/<string:request_id>')
def get_request(request_id :str):
    """获取作业图片"""
    data = review_service.get_request_origin_images(request_id)
    return success(data)

@review_router.put('/review/ai/list/<student_id>')
def get_ai_review_list(student_id):
    data = review_service.get_ai_review_list(student_id)
    return success(data )

@review_router.route('/review/ai/<ai_review_id>', methods=['GET'])
def get_ai_review_details(ai_review_id):
    data = review_service.get_review_details(ai_review_id)
    return success(data)
