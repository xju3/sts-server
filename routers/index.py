
from flask import Blueprint, render_template, request

index_router = Blueprint('index_router', __name__)

@index_router.route('/')
def index():
    return render_template('index.html')  # Create an index.html file

