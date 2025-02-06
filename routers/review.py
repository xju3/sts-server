from flask import Blueprint, request
from routers.common import success
from domain.service.review_service import ReviewService

review_router = Blueprint('review_router', __name__)
review_service = ReviewService()



@review_router.put('/review/request/create/<string:studentId>/<string:requestId>')
def create(studentId, requestId):
    review_service.create(studentId, requestId)
    return success()

@review_router.route('/review/request/get', methods=['POST'])
def get_requests():
    student_id = request.form.get("student_id")
    data = review_service.get_student_review_requests(student_id)
    return success(data)

@review_router.route('/review/ai/list/<student_id>', methods=['GET'])
def get_ai_review_list(student_id):
    data = review_service.get_ai_review_list(student_id)
    return success(data)

@review_router.route('/review/ai/<ai_review_id>', methods=['GET'])
def get_ai_review(ai_review_id):
    data = review_service.get_ai_review(ai_review_id)
    return success(data)
