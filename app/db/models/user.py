from sqlalchemy import Column, Integer, String
from app.db.base import Base

# ---------------------------------------------------
# SQLAlchemy User model mapped to the "users" table
# ---------------------------------------------------

class User(Base):
    __tablename__ = "users"                     # special class attribute --> Name of the table in the database

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    # password_hash = Column(String ,index=True)
    role = Column(String,index=True)
