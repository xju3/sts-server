from dataclasses import dataclass
from dataclass_wizard import JSONWizard


@dataclass
class ErrMsg(JSONWizard): 
    """error message."""
    code: str
    msg: str
    def __init__(self, _code: str = None, _msg : str = None) -> None:
        self.code = _code
        self.msg = _msg
    
    @classmethod
    def sucess(cls):
        return cls('0', 'success')

    @classmethod
    def failure(cls):
        return cls('1', 'failure')
    

@dataclass
class HttpResult(JSONWizard):
    """this data is used for http response."""
    err: ErrMsg
    data: any

    def __init__(self, err : ErrMsg, data: any):
        self.err = err
        self.data = data

    @classmethod
    def success(cls, data = None):
        return cls(data=data, err= ErrMsg.sucess())
    
    @classmethod
    def failure(cls):
        return cls(err= ErrMsg.failure())
    
    


