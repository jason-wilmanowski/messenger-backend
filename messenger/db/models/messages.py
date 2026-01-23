from messenger.db.database import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text
from datetime import datetime
from messenger.enums import MessageStatus

# Messages Table Structure

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey('conversation.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    body = Column(Text, nullable=False)
    status = Column(Text, nullable=False, default=MessageStatus.SENT.value)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, onupdate=datetime.utcnow, default=None)

