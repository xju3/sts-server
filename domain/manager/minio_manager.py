
from flask import Blueprint, request
from minio import Minio
from dotenv import load_dotenv
from typing import List
import os

load_dotenv()
minio_router = Blueprint('minio_router', __name__)

END_POINT = os.getenv("MINIO_END_POINT")

client = Minio(endpoint=END_POINT, 
               access_key=os.getenv("MINIO_ACCESS_KEY"), 
               secret_key=os.getenv("MINIO_SECRET_KEY"), secure=False)
bucket_name = 'assignments'

def gen_minio_access_key(object_name):
        return client.presigned_put_object(bucket_name=bucket_name, object_name=object_name)
    
def get_minio_files( directory) -> List[str]:
        return client.list_objects(bucket_name=bucket_name, prefix=directory)

def get_minio_file_url(directory) -> List[str]:
    minio_objects = get_minio_files(directory=directory)
    return list(map(lambda obj: f"http://{END_POINT}/{bucket_name}/{obj.object_name}" , minio_objects))