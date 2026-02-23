# it is a binary tree structure, where each node can have at most two children. It is used to represent hierarchical data, such as a story with multiple branches and choices. Each node in the tree represents a point in the story, and the edges represent the choices that lead to different branches of the story.


# SQL alchemy is an Object-Relational Mapping (ORM) library for Python that provides a high-level interface for working with databases. It allows developers to interact with databases using Python objects and classes, rather than writing raw SQL queries. This can make it easier to manage database interactions and improve code readability. In this code snippet, we are importing various components from SQLAlchemy that will be used to define our database models and interact with the database. These components include Column, Integer, String, DateTime, Boolean, ForeignKey, and JSON, which are used to define the structure of our database tables and the types of data they will store.
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.database import Base

# table inherited from Base
class Story(Base):
    __tablename__ = "stories"

    # primary_key: a unique value
    # index: can look up the index to find the row faster, which can improve query performance when searching for specific stories in the database. By indexing the id column, we can quickly retrieve a story based on its unique identifier, which is especially beneficial when dealing with large datasets.
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    session_id = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 1-to-many relationship type.
    # referece to StoryNode model
    nodes = relationship("StoryNode", back_populates="story") # define a relationship between the Story and StoryNode models. This allows us to easily access the nodes associated with a story by using the nodes attribute of the Story model. The back_populates parameter is used to specify the name of the attribute in the StoryNode model that will be used to access the related Story object, which is defined as story in the StoryNode model. This relationship allows us to easily navigate between stories and their associated nodes in our application.

# table inherited from Base
class StoryNode(Base):
    __tablename__ = "story_nodes"
    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id"), index=True)
    content = Column(String)
    is_root = Column(Boolean, default=False)
    is_ending = Column(Boolean, default=False)
    is_winning = Column(Boolean, default=False)
    options = Column(JSON, default=list)

    # referece to Story model
    story = relationship("Story", back_populates="nodes") # define a relationship between the StoryNode and Story models. This allows us to easily access the story associated with a node by using the story attribute of the StoryNode model. The back_populates parameter is used to specify the name of the attribute in the Story model that will be used to access the related StoryNode objects, which is defined as nodes in the Story model. This relationship allows us to easily navigate between nodes and their associated stories in our application.
