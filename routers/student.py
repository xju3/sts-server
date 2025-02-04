from model.http import HttpResult, ErrMsg, Ticket
from flask import Blueprint, request
from werkzeug.utils import secure_filename
import uuid
import os

student_router = Blueprint('student_router', __name__)

@student_router.route('/student')
def index():
    return "a student is here!"
