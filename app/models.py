'''
Here the table models are defined using sqlalchemy by expanding the Base from database.py

models are defined as classes and columns as attributes
'''

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP, DATE
from sqlalchemy.sql.expression import text as txt
from sqlalchemy.orm import relationship

from app.database import Base


class Users(Base):
    __tablename__ = "users"  # This is used to define the table name

    id = Column(Integer, primary_key=True, nullable=False) # nullable=False means that is not Null
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, server_default="new")     # server_default is the default value
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=txt('CURRENT_TIMESTAMP'))  #CURRENT_TIMESTAMP set sqlite column to the current datetime
    name = Column(String, nullable=False, server_default="New User")



# Define the Todo table
class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False) #Using content insted of "text" since text is a function
    dueDate = Column(DATE(), nullable=True)
    done = Column(Boolean, nullable=False, default=False)
    important = Column(Boolean, nullable=False, default=False)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=txt('CURRENT_TIMESTAMP'))  #CURRENT_TIMESTAMP set sqlite column to the current datetime
    
    # Relationship to parent
    owner = relationship('Users')



