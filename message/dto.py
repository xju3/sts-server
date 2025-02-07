from dataclasses import dataclass
from dataclass_wizard import JSONWizard
from typing import List
from datetime import datetime

@dataclass
class SingleValue(JSONWizard):
    """ticket id after uploading image successfully."""
    content: str | None

@dataclass
class StudentInfo(JSONWizard):
    id: str | None
    name: str | None
    school: str | None
    grade: int | None
    parentId: str | None 

@dataclass
class AccountInfo(JSONWizard):
    id: str | None
    parent_id: str | None
    parent_name: str  | None
    students: List[StudentInfo]  | None

@dataclass
class ReviewDetailInfo(JSONWizard):
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
class ReviewInfo(JSONWizard):
    id: str | None
    requestId: str  | None
    subject: str | None
    trans_time: datetime | None
    start_time: datetime | None
    end_time: datetime  | None
    subject: str  | None
    total: int  | None
    correct: int  | None
    incorrect: int  | None
    uncertain: int | None
    summary: str  | None
    details: List[ReviewDetailInfo] | None


    

