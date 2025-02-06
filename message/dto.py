from dataclasses import dataclass
from dataclass_wizard import JSONWizard
from typing import List
from datetime import datetime

@dataclass
class SingleValue(JSONWizard):
    """ticket id after uploading image successfully."""
    content: str

@dataclass
class StudentInfo(JSONWizard):
    id: str
    name: str
    school: str
    grade: int

@dataclass
class AccountInfo(JSONWizard):
    id: str
    parent_id: str
    parent_name: str
    students: List[StudentInfo] 

@dataclass
class ReviewInfo(JSONWizard):
    request_time: datetime
    start_time: datetime
    end_time: datetime
    subject: str
    total: int
    correct: int
    incorrect: int
    uncertain: int
    summary: str


    

