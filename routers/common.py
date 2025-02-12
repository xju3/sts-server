
from routers.model.output import HttpResult
import json

def success(obj = None):
    if obj == None:
        return json.dumps(HttpResult.success().to_dict)
    return json.dumps(HttpResult.success(obj).to_dict())


def failure(message):
    return json.dumps(HttpResult.failure(message).to_dict())
