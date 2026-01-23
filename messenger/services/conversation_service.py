from messenger.repositories.conversation_repo import ConversationRepository
from messenger.core.exceptions import ConversationExistsError, UserNotFoundError, SameUserIDError, \
    ConversationNotFoundError
from messenger.repositories.friends_repo import FriendsRepository
from messenger.repositories.user_repo import UserRepository


class ConversationService:

    def __init__(self, db):

        self.repository = ConversationRepository(db)
        self.user_repository = UserRepository(db)
        self.friends_repository = FriendsRepository(db)


    def create_conversation(self, user_id_1 : int, user_id_2 : int):
        if user_id_1 == user_id_2:
            raise SameUserIDError

        check_user = self.user_repository.get_user_by_id(user_id_2)

        if not check_user:
            raise UserNotFoundError()

        validate = self.repository.get_conversation(user_id_1, user_id_2)

        if validate:
            raise ConversationExistsError()

        return self.repository.create_conversation(user_id_1, user_id_2)

    def create_or_get_conversation(self, user_id_1 : int, user_id_2 : int):

        conversation = self.repository.get_conversation(user_id_1, user_id_2)
        if conversation:
            return conversation
        created_conversation = self.repository.create_conversation(user_id_1, user_id_2)
        return created_conversation

    def get_conversation(self, user_id_1 : int, user_id_2 : int):
        return self.repository.get_conversation(user_id_1, user_id_2)

    def get_conversation_by_id(self, id : int):
        return self.repository.get_conversation_by_id(id)

    def get_user_conversation(self, user_id : int):

        conversations = self.repository.get_user_conversation(user_id)
        current_conversations = []
        if conversations:
            for conversation in conversations:
                friendship = self.friends_repository.get_friendship(conversation.user_id_1, conversation.user_id_2)
                if friendship:
                    current_conversations.append(conversation)
        return current_conversations
