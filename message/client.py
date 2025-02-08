
import socketio
from model.agent import AiReviewInfo
import json

# sio = socketio.SimpleClient()
# sio.connect("http://localhost:3000")

class SocketIoClient:
    def send_assignment_review_message(self, ticket_id, review_info : AiReviewInfo):
        pass
        # sio.emit("on_review_finished", {"ticket_id": ticket_id, "review_info:": review_info})

