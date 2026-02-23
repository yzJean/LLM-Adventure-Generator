# write the endpoints hit by our users
import uuid # generate unique ids for our stories
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session

from db.database import get_db, SessionLocal
from models.story import Story, StoryNode
from models.job import StoryJob
from schemas.story import (
    CompleteStoryResponse, CompleteStoryNodeResponse, CreateStoryRequest)
from schemas.job import StoryJobResponse


router = APIRouter(
    prefix="/stories",
    tags=["stories"]
)
# backend URL: /<api-prefix>/<router>/<endpoint-name>
# example: /api/stories/create-story

# Session will identify in your browser when you are interacting with a website. It is a way to store information about your interactions with the website, such as your login status, preferences, and other data that can be used to personalize your experience. When you visit a website, the server creates a session for you and assigns it a unique session ID. This session ID is then stored in a cookie on your browser, allowing the server to recognize you on subsequent requests and provide you with a personalized experience based on your previous interactions with the website. It's a common way to maintain state and provide a seamless user experience on the web.
def get_session_id(session_id: Optional[str] = Cookie(None)):
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id

# Endpoint, POST: create a new story based on the theme provided by the user
# Return a job response, which contains the job id and the status of the job (e.g., "pending", "completed", "failed")
# Accept a "CreateStoryRequest" object as the request body, which contains the theme of the story to be created
@router.post("/create", response_model=StoryJobResponse) # response_model is a part of FastAPI's response handling system. It allows you to specify a Pydantic model that defines the structure of the response data. When you return a response from your endpoint, FastAPI will automatically validate and serialize the response data according to the specified model. This helps ensure that the response data is consistent and adheres to the expected format, making it easier for clients to consume and understand the API responses.
def create_story(
    request: CreateStoryRequest,
    background_tasks: BackgroundTasks,
    response: Response,
    session_id: str = Depends(get_session_id), # Thread 1: main HTTP thread. Depends: Allow get_session_id to be called on EVERY request and then inject this value into the session_id, so that we can use them in our logic.
    db: Session = Depends(get_db)
):
    response.set_cookie(key="session_id", value=session_id, httponly=True) # The server sets the session_id in the cookie, so that the browser can store it and send it back in subsequent requests

    job_id = str(uuid.uuid4()) # Generate a unique job id for this story creation task.
    job = StoryJob(
        job_id=job_id,
        session_id=session_id,
        theme=request.theme,
        status="pending"
    )

    db.add(job) # First time: ADD to database. Add the job to the database session, but it is not committed yet, so the job is not saved in the database yet. We need to call db.commit() to save the job in the database.
    db.commit() # Thread 1 writes to database

    # create a background task to generate the story, so that we can return the response to the user immediately without waiting for the story generation to complete. The background task will update the job status in the database once the story generation is completed, so that the frontend can check the status of the job and get the story when it is completed.
    background_tasks.add_task(
        generate_story_task,
        job_id=job_id,
        theme=request.theme,
        session_id=session_id
    )
    # # Is equivalent to:
    # generate_story_task(
    #     job_id=job_id,
    #     theme=request.theme,
    #     session_id=session_id
    # )
    """
    Time 1: User makes request
            ↓
    Time 2: Server executes create_story
            ├─ Create job in database
            ├─ Queue background task (generate_story_task)
            ├─ Return response to browser immediately ✅
            ↓
    Time 3: Background thread starts
            ├─ Calls: generate_story_task(job_id="xyz", theme="fantasy", session_id="abc123")
            ├─ Generates story (might take 10+ seconds)
            ├─ Updates database
            └─ User doesn't wait for this ✅
    """

    return job # This is what I actually returning to the frontend

def generate_story_task(job_id: str, theme: str, session_id: str):
    # We need to create a new database session when user reqeusts, because one session can tell users that it is process and the other can do some the background task running in a different thread. Once the background task is completed, we need to update the job status in the database, so that the frontend can check the status of the job and get the story when it is completed. If we use the same database session, we will have some hanging operations where the background task in running and it's using the database, the API will not be able to use the database at the same time. It is a asynchronous task, so we need to create a new database session for it.
    db = SessionLocal() # Thread 2: background thread -> SEPERATE session!

    try:
        # We can't share the same job object between the main and the background task, because they are running in different threads.
        # We're QUERYING an existing job, not creating a new one!
        job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first() # grab the first entry we found
        
        if not job:
            return

        try:
            job.status = "processing" # since the job exists, just modify existing data and then use commit() to save the changes to the database.
            db.commit() # Thread 2 independently manages its own transaction
            
            story = {} # TODO: generate a story
            
            job.story_id = 1 # TODO: update story id
            job.status = "completed"
            job.completed_at = datetime.now()
            db.commit()
        except Exception as e:
            job.status = "failed"
            job.completed_at = datetime.now()
            job.error = str(e)
            db.commit()
    finally:
        db.close()

@router.get("{story_id}/complete", response_model=CompleteStoryResponse)
def get_complete_story(story_id: int, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    #TODO: parse story
    return story

def build_complete_story_tree(db: Session,story: Story) -> CompleteStoryResponse:
    pass
