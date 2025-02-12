
from flask import Blueprint, request
from domain.manager.minio_manager import gen_minio_access_key 
from routers.model.output import SingleValue_O
from routers.common import success
minio_router = Blueprint('minio_router', __name__)
bucket_name = "assignments"

@minio_router.route('/minio/get_access_key', methods=['POST'])
def gen_access_key():
    data = request.get_json()
    object_name = data["objectName"]
    url = gen_minio_access_key(object_name)
    return success(obj=SingleValue_O(content=url))