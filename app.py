import os
from flask import Flask 
from flask_socketio import SocketIO
from message.manager import SocketManager
from routers.index import index_router
from routers.minio import minio_router
from routers.account import account_router
from routers.review import review_router


# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.register_blueprint(index_router)
app.register_blueprint(minio_router)
app.register_blueprint(account_router)
app.register_blueprint(review_router)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Create SocketManager instance
socket_manager = SocketManager(socketio)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3300, debug=True)
    # llm = GeminiLLM(GeminiModel.GEMINI_2_0_FLASH)
    # llm = DeepseekChatBot()
    # llm.chat("hello")
    # agent = AssignmentAgent(llm.deepSeek)
    # agent.check_assignments_gemini('/Users/tju/Workspace/projects/sts/server/files/uploads')