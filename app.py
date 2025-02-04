import os
from flask import Flask, render_template
from flask_socketio import SocketIO
from socket_manager import SocketManager
from routers.index import index_router

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.register_blueprint(index_router)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Create SocketManager instance
socket_manager = SocketManager(socketio)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3300, debug=True)