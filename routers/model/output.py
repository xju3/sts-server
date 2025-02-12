from dataclasses import dataclass
from dataclass_wizard import JSONWizard
from typing import List
from datetime import datetime



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
        return cls('1', "failure")
    
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
    def failure(cls, message):
        err = ErrMsg(_code= '-1', _msg= message)
        return cls(data = [], err= err)
    

@dataclass
class SingleValue_O(JSONWizard):
    """ticket id after uploading image successfully."""
    content: str | None

@dataclass
class StudentInfo_O(JSONWizard):
    id: str | None
    name: str | None
    school: str | None
    grade: int | None
    accountId: str | None 

@dataclass
class Parent_O(JSONWizard):
    id: str | None
    name: str | None
    accountId: str | None

@dataclass
class AccountInfo_O(JSONWizard):
    parent: Parent_O
    students: List[StudentInfo_O]  | None


@dataclass
class ReviewRequest_O(JSONWizard):
    id: str | None
    studentId: str | None
    images: int | None

@dataclass
class ReviewDetailInfo_O(JSONWizard):
    id: str | None
    aiReviewId : str | None
    no: str | None
    ansStudent: str | None
    ansAi: str | None
    conclusion: int | None
    solution: str | None
    knowledge: str | None
    suggestion: str | None


@dataclass
class ReviewInfo_O(JSONWizard):
    id: str | None
    requestId: str  | None
    subject: str | None
    images: int | None
    trans_time: datetime | None
    start_time: datetime | None
    end_time: datetime  | None
    subject: str  | None
    total: int  | None
    correct: int  | None
    incorrect: int  | None
    uncertain: int | None
    summary: str  | None
    details: List[ReviewDetailInfo_O] | None


    

