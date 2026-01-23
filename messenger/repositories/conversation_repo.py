from messenger.db.models.conversation import Conversation
from sqlalchemy import or_, and_

class ConversationRepository:

    def __init__(self, db):
        self.db = db

    # create new conversation entries
    def create_conversation(self, user_id_1:int, user_id_2:int):

        new_conversation = Conversation(user_id_1=user_id_1, user_id_2=user_id_2)
        self.db.add(new_conversation)
        self.db.commit()
        self.db.refresh(new_conversation)
        return new_conversation


    # get conversation with two users to validate uniqueness before creation
    def get_conversation(self, user_id_1:int, user_id_2:int):

        return self.db.query(Conversation).filter(or_(
                                                        and_(Conversation.user_id_1 == user_id_1,
                                                            Conversation.user_id_2 == user_id_2),
                                                        and_(Conversation.user_id_1 == user_id_2,
                                                            Conversation.user_id_2 == user_id_1))).first()

    def get_conversation_by_id(self, id : int):

        return self.db.query(Conversation).filter(Conversation.id == id).first()

    # get all conversations involving a user
    def get_user_conversation(self, user_id:int):

        return self.db.query(Conversation).filter(or_(Conversation.user_id_1 == user_id,
                                                      Conversation.user_id_2 == user_id)).all()
