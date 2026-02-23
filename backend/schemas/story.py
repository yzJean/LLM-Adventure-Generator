from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel

# All of schemes are needed to inherit from BaseModel, or at least have one parent class which is the BaseModel 
# => pydantic automatically validate data

class StoryOptionsSchema(BaseModel):
    text: str
    node_id: Optional[int] = None

# No from_attributes (request only), Used when: client sends node data, validate request data
class StoryNodeBase(BaseModel):
    content: str
    is_ending: bool = False
    is_winning_ending: bool = False

# Has from_attributes (response from ORM), Used when: returning Story ORM objects
class StoryBase(BaseModel):
    title: str
    session_id: Optional[str] = None
    class Config:
        from_attributes = True

class CreateStoryRequest(BaseModel):
    theme: str

#  Used for responses
class CompleteStoryNodeResponse(StoryNodeBase):
    id: int
    options: List[StoryOptionsSchema] = []

    class Config:
        from_attributes = True

class CompleteStoryResponse(StoryBase):
    id: int
    created_at: datetime
    root_nodes: CompleteStoryNodeResponse
    all_nodes: Dict[int, CompleteStoryNodeResponse]

    class Config:
        from_attributes = True
        
        
"""
Add from_attributes = True if:
@router.post("/something", response_model=YourSchema)  # ← Response model
def endpoint(...):
    obj = db.query(Model).first()  # Returns ORM object
    return obj  # Need from_attributes!
    
Don't add it if:
@router.post("/something")  # ← Just accepting data
def endpoint(data: YourSchema, ...):  # Request validation only
    # data is already validated dict from JSON
    # No ORM object involved

"""