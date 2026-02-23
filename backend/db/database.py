from sqlalchemy import create_engine #wrap database connections and provides a common interface for different database backends
from sqlalchemy.orm import sessionmaker # create a new SQLAlchemy session, which is used to interact with the database. It provides methods for querying and manipulating the database, and it manages the connection to the database.
from sqlalchemy.ext.declarative import declarative_base # base class for our database models.

from core.config import settings

# Purpose: Establish the connection to database server. The engine manages a pool of connections that can be reused. All database operations go through this engine. Example: Code -> Engine (creates connection) -> Database server.
engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # create a new SQLAlchemy session factory. The autocommit and autoflush parameters are set to False to ensure that changes to the database are not automatically committed or flushed until explicitly done so in the code. The bind parameter is set to the engine we created earlier, which allows the session to connect to the database.

Base = declarative_base() # create a new base class for our database models. This class will be used as the base for all of our database models, and it provides a common interface for defining the structure of our database tables and the relationships between them.

def get_db():
    db = SessionLocal() # create a new database session using the SessionLocal factory we defined earlier. This ensure this new session is isolated from other session. When request finishes, the session will be closed.
    try:
        yield db # yield the database session to the caller. This allows us to use the session in a context manager, which ensures that the session is properly closed after it is used.
    finally: # when the program is shut down or the session is no longer needed, the finally block will be executed, which ensures that the database session is properly closed and any resources it was using are released.
        db.close() # close the database session after it is used. This is important to free up resources and ensure that connections to the database are properly managed. By using a context manager and yielding the session, we can ensure that the session is always closed, even if an error occurs during its use.


"""
* Looks at all models that inherit from Base
* Checks if their corresponding tables exist in the database
* Creates any missing tables

Base.metadata
* Contains metadata about all models
* Lists all tables that should exist

.create_all(bind=engine)
* For each table in metadata:
    * If it exists: do nothing
    * If it doesn't exist: create it
    
# You defined these models:
class StoryJob(Base):
    __tablename__ = "story_jobs"
    ...

class Story(Base):
    __tablename__ = "stories"
    ...
# When create_tables() is called:
# It says: "I need tables: story_jobs, stories"
# It checks the database
# If they don't exist, it creates them with:
# CREATE TABLE story_jobs (...)
# CREATE TABLE stories (...)
"""
def create_tables():
    Base.metadata.create_all(bind=engine)