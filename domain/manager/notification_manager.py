
from typing import List
import os
from dotenv import load_dotenv
from domain.model.common import PushMessage
import jpush

load_dotenv()
app_key = os.getenv("JPUSH_APP_KEY")
app_secret = os.getenv("JPUSH_APP_SECRET")

_jpush = jpush.JPush(app_key, app_secret)
# _jpush.set_logging("DEBUG")


def send_notification(items: List[PushMessage]):
    for item in items:
        if item.platform != 'android':
            continue
        push = _jpush.create_push()
        push.audience = {"registration_id": [item.target]}
        push.platform = item.platform
        push.notification = jpush.notification(alert="作业批改完成")
        push.message = jpush.message(msg_content=item.content, title="", content_type='Text')
        push.send()