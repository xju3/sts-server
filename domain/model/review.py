from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from domain.model.common import Base
from datetime import datetime
from dataclasses import dataclass

@dataclass
class ReviewRequest(Base):
    __tablename__ = "review_request"
    student_id: Mapped[str] = mapped_column(nullable=True,)
    trans_time: Mapped[datetime] = mapped_column(nullable=True, default=datetime.now())
    status: Mapped[int] = mapped_column(nullable=True, default=0)

@dataclass
class ReviewAI(Base):
    __tablename__ = "review_ai"
    request_id: Mapped[str] = mapped_column(nullable=True,)
    start_time: Mapped[datetime] = mapped_column(nullable=True,)
    end_time: Mapped[datetime] = mapped_column(nullable=True,)
    total: Mapped[int] = mapped_column(nullable=True,)
    subject: Mapped[int] = mapped_column(nullable=True,)
    correct: Mapped[int] = mapped_column(nullable=True,)
    incorrect: Mapped[int] = mapped_column(nullable=True,)
    uncertain: Mapped[int] = mapped_column(nullable=True,)
    summary: Mapped[str] = mapped_column(nullable=True,)

@dataclass
class ReviewDetail(Base):
    __tablename__ = "review_detail"
    request_ai_id: Mapped[str] = mapped_column(nullable=True,)
    no: Mapped[str] = mapped_column(nullable=True,)
    ans_student: Mapped[str] = mapped_column(nullable=True,)
    ans_ai: Mapped[str] = mapped_column(nullable=True,)
    conclusion: Mapped[int] = mapped_column(nullable=True,)
    reason: Mapped[str] = mapped_column(nullable=True,)
    solution: Mapped[str] = mapped_column(nullable=True,)
    knowledges: Mapped[str] = mapped_column(nullable=True,)
    suggestions: Mapped[str] = mapped_column(nullable=True,)

