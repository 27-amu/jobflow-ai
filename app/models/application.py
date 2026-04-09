from sqlalchemy import Column, Integer, String, Text
from app.database.db import Base

class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    role = Column(String, nullable=False)
    status = Column(String, nullable=False)
    date_applied = Column(String, nullable=False)
    recruiter_name = Column(String, nullable=True)
    recruiter_email = Column(String, nullable=True)
    follow_up_date = Column(String, nullable=True)
    notes = Column(Text, nullable=True)