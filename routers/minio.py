
from flask import Blueprint, request
from domain.manager.minio_manager import MinioManager
from message.dto import SingleValue
from routers.common import success, failure
minio_router = Blueprint('minio_router', __name__)
bucket_name = "assignments"

minio_manager = MinioManager()
@minio_router.route('/minio/get_access_key', methods=['POST'])
def gen_access_key():
    data = request.get_json()
    object_name = data["objectName"]
    url = minio_manager.gen_access_key(object_name)
    return success(obj=SingleValue(content=url))