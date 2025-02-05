from model.http import HttpResult, ErrMsg
from model.domain import Ticket
from flask import Blueprint, request
from ai.agent.assignment import AssignmentAgent
from ai.llm.gemini import GeminiLLM, GeminiModel
from werkzeug.utils import secure_filename
import multiprocessing
import uuid
import os

image_router = Blueprint('image_router', __name__)

gemini = GeminiLLM(GeminiModel.GEMINI_2_0_FLASH)
assignment_agent = AssignmentAgent(gemini)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'txt'}  # Allowed file types
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@image_router.route('/image/upload', methods=['POST'])
def upload_file() -> HttpResult:

    client_id = _ticket_id = uuid.uuid4().hex

    errMsg = ErrMsg(_code='0', _msg='success')
    result = HttpResult(_err = errMsg)

    if request.method == 'POST':
        studentId = request.form.get('studentId')  # Get text data
        print(studentId)

        files = request.files.getlist("files") 
        uploaded_files = []
        for file in files:
            if file.filename == '':
                result.err.code = '-1'
                result.err.msg = 'No selected file'

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(image_router.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                uploaded_files.append(file_path) # Add filename to the list
            else:
                result.err.code = '-2'
                result.err.msg = 'file type not allowed'
        if len(uploaded_files) > 0:
            # create a new process to handle assignment review.
            multiprocessing.Process(assignment_agent.check_assignments, args=(_ticket_id, uploaded_files))
    
    if result.err.code == '0': 
        result.data = Ticket(client_id)

    return result.to_json(), 200