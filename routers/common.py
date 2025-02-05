
from model.http import HttpResult
import json

def success(obj = None):
    if obj == None:
        return json.dumps(HttpResult.success().to_dict)
    return json.dumps(HttpResult.success(obj).to_dict())


def failure():
    return json.dumps(HttpResult.fa)
