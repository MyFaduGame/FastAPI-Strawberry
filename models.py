#FastAPI Imports
import sqlalchemy as db

#Local Imports
from database import Base

class Users(Base):
    __tablename__= 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256),nullable=True)