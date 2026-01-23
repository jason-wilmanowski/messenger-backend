from messenger.db.database import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime


# Friends Table Structure

class Friend(Base):

    __tablename__ = "friends"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id_1 = Column(Integer, ForeignKey("user.id"), nullable=False)
    user_id_2 = Column(Integer, ForeignKey("user.id"), nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
