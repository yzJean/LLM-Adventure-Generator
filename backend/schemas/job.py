from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class StoryJobBase(BaseModel):
    theme: str

class StoryJobResponse(BaseModel):
    job_id: str
    status: str
    created_at: datetime
    story_id: Optional[int] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None

    class Config:
        from_attributes = True # how Pydantic reads data from the SQLAlchemy object (using attribute access like job.job_id instead of dict access like job["job_id"]
        
class StoryJobCreate(StoryJobBase):
    pass