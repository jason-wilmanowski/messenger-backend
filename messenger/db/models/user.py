from messenger.db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from messenger.enums import UserStatus

# User Table Structure

class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    status = Column(String, nullable=False, default=UserStatus.ACTIVE.value)
    created = Column(DateTime, default=datetime.utcnow)
