from messenger.db.database import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from datetime import datetime
from messenger.enums import RequestStatus

# Friend Request Table Structure

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    send_user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    rec_user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    status = Column(String, nullable=False, default=RequestStatus.SENT.value)
    created = Column(DateTime, default=datetime.utcnow)