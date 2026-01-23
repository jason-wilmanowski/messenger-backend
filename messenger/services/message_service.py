from messenger.enums import MessageStatus
from messenger.repositories.conversation_repo import ConversationRepository
from messenger.repositories.messages_repo import MessagesRepository
from messenger.core.exceptions import MessageNotFoundError, MessageInvalidError, NotAllowedError, ConversationNotFoundError, MessageAlreadyDeletedError, NoMessagesFoundError
from messenger.core.encrypting import EncryptText

class MessageService:

    def __init__(self, db):

        self.repository = MessagesRepository(db)
        self.conversation_repository = ConversationRepository(db)

    def create_message(self, conversation_id : int, user_id : int, body : str):
        for valid in [conversation_id, user_id, body]:

            if not valid:
                raise MessageInvalidError()

        encrypted_body = EncryptText.encrypt(body)

        check_conversation = self.conversation_repository.get_conversation_by_id(conversation_id)
        if not check_conversation:
            raise ConversationNotFoundError()
        elif check_conversation.user_id_1 != user_id and check_conversation.user_id_2 != user_id:
            raise NotAllowedError()

        message = self.repository.create_message(conversation_id, user_id, encrypted_body)
        message.body = EncryptText.decrypt(message.body)

        return message


    def get_all_messages(self, conversation_id : int):
        messages = self.repository.get_all_messages(conversation_id)

        if not messages:
            raise NoMessagesFoundError()

        for message in messages:
            message.body = EncryptText.decrypt(message.body)

        return messages

    def get_all_user_messages(self, conversation_id : int, user_id : int):
        messages = self.repository.get_all_user_messages(conversation_id, user_id)

        if not messages:
            raise MessageNotFoundError()

        for message in messages:
            message.body = EncryptText.decrypt(message.body)

        return messages

    def get_message(self, message_id : int):
        message = self.repository.get_message(message_id)

        if not message:
            raise MessageNotFoundError()

        message.body = EncryptText.decrypt(message.body)
        return message


    def sync_messages(self, last_seen_ids : dict):
        synced_messages = self.repository.sync_messages(last_seen_ids)

        for conversation_id, messages in synced_messages.items():
            for msg in messages:
                msg.body = EncryptText.decrypt(msg.body)
                msg.created = msg.created.isoformat()
                if msg.updated:
                    msg.updated = msg.updated.isoformat()

        if not synced_messages:
            return None

        return synced_messages



    def update_message(self, message_id : int, body : str, user_id : int):
        validate = self.repository.get_message(message_id)

        if not validate:
            raise MessageNotFoundError()
        elif validate.user_id != user_id:
            raise NotAllowedError()

        encrypted_body = EncryptText.encrypt(body)
        updated_message = self.repository.update_message(message_id, encrypted_body)
        updated_message.body = EncryptText.decrypt(updated_message.body)
        return updated_message


    def delete_message(self, message_id : int, user_id : int):
        validate = self.repository.get_message(message_id)

        if not validate:
            raise MessageNotFoundError()
        elif not validate.user_id == user_id:
            raise NotAllowedError()
        elif validate.status == MessageStatus.DELETED.value:
            raise MessageAlreadyDeletedError()
        return self.repository.delete_message(message_id, MessageStatus.DELETED)