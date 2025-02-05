
from flask import Blueprint, request
from minio import Minio
from dotenv import load_dotenv
import os

load_dotenv()
minio_router = Blueprint('minio_router', __name__)

client = Minio(endpoint=os.getenv("MINIO_END_POINT"), 
               access_key=os.getenv("MINIO_ACCESS_KEY"), 
               secret_key=os.getenv("MINIO_SECRET_KEY"), secure=False)
bucket_name = 'assignments'

class MinioManager:

    def gen_access_key(self, object_name):
        return client.presigned_get_object(bucket_name=bucket_name, object_name=object_name)
    
    def get_files(self, directory):
        return client.list_objects(bucket_name=bucket_name, prefix=directory)