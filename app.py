import os
from flask import Flask 
from flask_socketio import SocketIO
from routers.index import index_router
from routers.minio import minio_router
from routers.account import account_router
from routers.review import review_router
from flask_apscheduler import APScheduler
from domain.service.review_service import ReviewService


# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.register_blueprint(index_router)
app.register_blueprint(minio_router)
app.register_blueprint(account_router)
app.register_blueprint(review_router)

# service = ReviewService()

# scheduler = APScheduler()
# scheduler.add_job(id='pre_gen_assignment', 
#                   func=service.pre_gen_weekly_assignments, 
#                   trigger='cron', day_of_week='fri', hour=10, min = 0)

# scheduler.add_job(id='ai_gen_assignment', 
#                   func=service.gen_weekly_assignments, 
#                   trigger='cron', day_of_week='fri', hour=10, min=10)

# scheduler.init_app(app)

socketio = SocketIO(app, cors_allowed_origins="*")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3300, debug=True)