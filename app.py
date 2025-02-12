import os
from flask import Flask 
from flask_socketio import SocketIO
from routers.index import index_router
from routers.minio import minio_router
from routers.account import account_router
from routers.review import review_router
from domain.manager.minio_manager import get_minio_files 


# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.register_blueprint(index_router)
app.register_blueprint(minio_router)
app.register_blueprint(account_router)
app.register_blueprint(review_router)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

def run_app():
    socketio.run(app, host='0.0.0.0', port=3300, debug=True)

def test_minio():
    files = get_minio_files("e48462f6-e903-11ef-9713-ba79e1a32d91/53732440-e913-11ef-ac8b-293b0cbef13d/")
    for file in files:
        print(file)

if __name__ == '__main__':
    run_app()
    # test_minio()