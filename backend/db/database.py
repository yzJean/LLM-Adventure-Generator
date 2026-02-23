from sqlalchemy import create_engine #wrap database connections and provides a common interface for different database backends
from sqlalchemy.orm import sessionmaker # create a new SQLAlchemy session, which is used to interact with the database. It provides methods for querying and manipulating the database, and it manages the connection to the database.
from sqlalchemy.ext.declarative import declarative_base # base class for our database models.

from core.config import settings

engine = create_engine(settings.DATABASE_URL) # create a new SQLAlchemy engine using the database URL specified in the settings. The connect_args parameter is used to pass additional arguments to the database connection, in this case, we are setting check_same_thread to False for SQLite databases to allow multiple threads to access the database simultaneously.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # create a new SQLAlchemy session factory. The autocommit and autoflush parameters are set to False to ensure that changes to the database are not automatically committed or flushed until explicitly done so in the code. The bind parameter is set to the engine we created earlier, which allows the session to connect to the database.

Base = declarative_base() # create a new base class for our database models. This class will be used as the base for all of our database models, and it provides a common interface for defining the structure of our database tables and the relationships between them.

def get_db():
    db = SessionLocal() # create a new database session using the SessionLocal factory we defined earlier. This session will be used to interact with the database and perform operations such as querying and manipulating data.
    try:
        yield db # yield the database session to the caller. This allows us to use the session in a context manager, which ensures that the session is properly closed after it is used. The yield statement allows us to return the session to the caller while still maintaining control over when it is closed.
    finally: # when the program is shut down or the session is no longer needed, the finally block will be executed, which ensures that the database session is properly closed and any resources it was using are released.
        db.close() # close the database session after it is used. This is important to free up resources and ensure that connections to the database are properly managed. By using a context manager and yielding the session, we can ensure that the session is always closed, even if an error occurs during its use.


def create_tables():
    Base.metadata.create_all(bind=engine) # create all tables in the database based on the models defined using the Base class. The metadata attribute of the Base class contains information about the structure of the database tables, and the create_all method is used to create the tables in the database if they do not already exist. The bind parameter is set to the engine we created earlier, which allows the method to connect to the database and execute the necessary SQL commands to create the tables. This function can be called at the start of the application to ensure that all necessary tables are created before any operations are performed on the database.