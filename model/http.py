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

@dataclass
class HttpResult(JSONWizard):
    """this data is used for http response."""
    err: ErrMsg
    data: any

    def __init__(self, _err : ErrMsg = None, _data : any = None) -> None:
        self.err = _err
        self.data = _data



