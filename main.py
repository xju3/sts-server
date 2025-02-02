from flask import Flask, request
from llm.gemini import GeminiLLM, GeminiModel
import os

app = Flask(__name__)
app.config['TESTING'] = True
app.config['UPLOAD_FOLDER'] = "/var/tmp"


llm = None

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    if file.content_type not in ['image/jpeg', 'image/png', 'application/pdf']:
        return 'File type not supported', 415

    if file:
        filename = secure_filename(file.filename)
        print(filename)
        
        path =os.path.join(app.config['UPLOAD_FOLDER'])
        file.save(path, filename)
        send_image_to_ai(path, filename)
        return 'File uploaded successfully'


def send_image_to_ai(path, filename):
    pass


if __name__ == "__main__":
    # app.run(debug=True, port=3300, host='0.0.0.0')
    # bot = OllamaChatBot("deepseek-r1:14b")
    # bot = LLMDeepseek()
    # llm = LmStudioQwenCode14b()
    llm = GeminiLLM(GeminiModel.GEMINI_1_5_FLASH)
    llm.get_google_restaurants()
