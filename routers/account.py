

from flask import Blueprint, render_template, request
from domain.service.account_service import AccountService 
from model.http import HttpResult
from routers.common import success, failure
import json


account_service = AccountService()

account_router = Blueprint('account_router', __name__)

@account_router.route("/account/create",  methods=['POST'])
def create_account():
    mobile = request.form.get('mobile')
    school= request.form.get('school')
    parent_name = request.form.get('parent_name')
    student_name = request.form.get('student_name')
    grade = request.form.get('grade')
    account_service.create_account(mobile, school, grade, parent_name, student_name)
    data = account_service.login(mobile=mobile)
    return success(data)

@account_router.route("/account/login",  methods=['POST'])
def login():
    mobile = request.form.get('mobile')
    data = account_service.login(mobile=mobile, access_code=None)
    return success(data)

@account_router.route("/account/test",  methods=['POST'])
def test():
    return success()




