from flask import Blueprint, request
from domain.service.account_service import AccountService 
from routers.common import success, failure

account_service = AccountService()
account_router = Blueprint('account_router', __name__)

@account_router.route("/account/create",  methods=['POST'])
def create_account():

    request_body = request.get_json()
    mobile = request_body.get('mobile')
    school= request_body.get('school')
    parent_name = request_body.get('parent')
    student_name = request_body.get('student')
    grade = request_body.get('grade')

    if student_name is None:
        return failure("学生姓名不能为空.")


    # mobile = request.form.get('mobile')
    # school= request.form.get('school')
    # parent_name = request.form.get('parent_name')
    # student_name = request.form.get('student_name')
    # grade = request.form.get('grade')
    account_service.create_account(mobile, school, grade, parent_name, student_name)
    data = account_service.login(mobile=mobile)
    return success(data)

@account_router.route("/account/login",  methods=['POST'])
def login():
    data = request.get_json()
    data = account_service.login(mobile=data['mobile'], access_code=None)
    return success(data)

@account_router.route("/account/test",  methods=['POST'])
def test():
    return success()




