
from flask import Blueprint, render_template, request

index_router = Blueprint('index_router', __name__)

@index_router.route('/')
def index():
    return "api page"  # Create an index.html file

