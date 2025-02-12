from flask import Blueprint, request
from domain.service.account_service import AccountService 
from routers.common import success, failure
from routers.model.input import Registration_I, LoginHistory_I

account_service = AccountService()
account_router = Blueprint('account_router', __name__)

@account_router.post("/account/login/history",)
def login_history():
    body = request.get_json()
    data = LoginHistory_I(**body)
    account_service.create_login_history(data)
    return success({})


@account_router.route("/account/create",  methods=['POST'])
def create_account():
    body = request.get_json()
    data = Registration_I(**body)
    if data.student is None:
        return failure("学生姓名不能为空.")
    account_service.create_account(data)
    data = account_service.login(account_name=data.account)
    return success(data)

@account_router.post("/account/login")
def login():
    body = request.get_json()
    account = body['account']
    data = account_service.login(account_name=account, access_code=None)
    if data is None:
        return failure("账号不存在")
    return success(data)

@account_router.put("/account/schools/<float:lat>/<float:lng>")
def get_schools(lat, lng):
    data = account_service.get_schools(lat, lng)
    return success(data)