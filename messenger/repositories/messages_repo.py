from messenger.db.models.messages import Message
from sqlalchemy import and_
from datetime import datetime

from messenger.enums import MessageStatus


class MessagesRepository:

    def __init__(self, db):

        self.db = db


    # create new message entry
    def create_message(self, conversation_id : int, user_id : int, body : str):

        new_message = Message(conversation_id = conversation_id, user_id = user_id, body = body)
        self.db.add(new_message)
        self.db.commit()
        self.db.refresh(new_message)
        return new_message


    # get all messages from a conversation
    def get_all_messages(self, conversation_id : int):
        return self.db.query(Message).filter(and_(Message.conversation_id == conversation_id,
                                                  Message.status != MessageStatus.DELETED.value)).all()

    # get all messages from a user inside a conversation
    def get_all_user_messages(self,conversation_id, user_id : int):
        return self.db.query(Message).filter(and_(Message.user_id == user_id,
                                                  Message.conversation_id == conversation_id)).all()

    # get single message via message id
    def get_message(self, message_id : int):
        return self.db.query(Message).filter(Message.id == message_id).first()


    # sync all messages with higher id than last seen message id
    def sync_messages(self, last_seen_ids : dict):
        result = {}
        for conversation_id, last_seen_id in last_seen_ids.items():
            messages = self.db.query(Message).filter(and_(Message.conversation_id == conversation_id,
                                             Message.id > last_seen_id)).all()
            if messages:
                messages[conversation_id] = messages
        return result


    # update body of the chosen message
    def update_message(self, message_id : int, body : str):
        message = self.get_message(message_id)
        message.body = body
        message.updated = datetime.utcnow()
        self.db.commit()
        self.db.refresh(message)
        return message


    # delete message via message_id
    def delete_message(self, message_id : int, status : str):
        message = self.get_message(message_id)
        message.status = status
        self.db.commit()
        return message
