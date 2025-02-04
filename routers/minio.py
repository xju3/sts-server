

from flask import Blueprint, request
from minio import Minio
from dotenv import load_dotenv
import os

load_dotenv()
minio_router = Blueprint('minio_router', __name__)

client = Minio(http_client=os.getenv("MINIO_HOST"), 
               access_key=os.getenv("MINIO_ACCESS_KEY"), 
               secret_key=os.getenv("MINIO_SECRET_KEY"),)

bucket_name = "assignments"

@minio_router.route('/minio/get_access_key')
def gen_access_key():
    object_name = request.form['objectName']
    return client.presigned_put_object(bucket_name=bucket_name, object_name=object_name)