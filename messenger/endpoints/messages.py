from fastapi import APIRouter, Depends, HTTPException
from messenger.core.dependencies import get_db, get_current_user
from messenger.services.message_service import MessageService
from sqlalchemy.orm import Session
from messenger.schemes.message import MessageOutput, MessageUpdateDetails, MessageCreate, MessagesOutput, ConversationMessageInput, MessageDeleteDetails
from messenger.core.exceptions import MessageNotFoundError, NotAllowedError, MessageInvalidError, \
    ConversationNotFoundError, MessageAlreadyDeletedError, NoMessagesFoundError
from messenger.websocket import ws_manager
from messenger.websocket.events import EventTypes
from messenger.services.conversation_service import ConversationService



router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("", response_model=MessageOutput)
async def create_message(message: MessageCreate, user_id : int = Depends(get_current_user), db: Session = Depends(get_db)):

    message_service = MessageService(db)

    conversation_service = ConversationService(db)

    try:
        message = message_service.create_message(message.conversation_id, user_id, message.body)
    except MessageInvalidError:
        raise HTTPException(status_code=409, detail="Invalid Message Details")
    except ConversationNotFoundError:
        raise HTTPException(status_code=404, detail="Conversation not found")
    except NotAllowedError:
        raise HTTPException(status_code=403, detail="Not allowed! User is no member of the conversation")


    event = {
        "event" : EventTypes.MESSAGE_NEW,
        "payload" : {
            "id" : message.id,
            "conversation_id" : message.conversation_id,
            "user_id" : message.user_id,
            "body" : message.body,
            "created" : message.created.isoformat(),

        }
    }

    conversation = conversation_service.get_conversation_by_id(message.conversation_id)
    user_ids = (conversation.user_id_1, conversation.user_id_2)


    await ws_manager.broadcast_to_users(user_ids, event)

    return message


@router.get("/{id}", response_model=MessageOutput)
def get_message(id: int, db : Session = Depends(get_db)):

    message_service = MessageService(db)

    try:
        message = message_service.get_message(id)
    except MessageNotFoundError:
        raise HTTPException(status_code=404, detail="Message not found")

    return message

@router.post("/conversation-messages", response_model=MessagesOutput)
def get_conversation_messages(conversation_id: ConversationMessageInput, user_id : int = Depends(get_current_user), db : Session = Depends(get_db)):

    message_service = MessageService(db)

    try:
        messages = message_service.get_all_messages(conversation_id.conversation_id)
    except NoMessagesFoundError:
        return {"messages" : []}

    return {"messages" : messages}


@router.patch("", response_model=MessageOutput)
async def update_message(body : MessageUpdateDetails, user_id : int = Depends(get_current_user), db : Session = Depends(get_db)):

    message_service = MessageService(db)

    conversation_service = ConversationService(db)

    try:
        updated_message = message_service.update_message(body.id, body.body, user_id)
    except MessageNotFoundError:
        raise HTTPException(status_code=404, detail="Message not found")
    except NotAllowedError:
        raise HTTPException(status_code=403, detail="Message Updating not allowed")

    event = {
        "event" : EventTypes.MESSAGE_UPDATED,
        "payload" : {
            "id" : updated_message.id,
            "conversation_id" : updated_message.conversation_id,
            "user_id" : updated_message.user_id,
            "body" : updated_message.body,
            "created" : updated_message.created.isoformat(),
            "updated" : updated_message.updated.isoformat(),
        }
    }

    conversation = conversation_service.get_conversation_by_id(updated_message.conversation_id)
    user_ids = (conversation.user_id_1, conversation.user_id_2)

    await ws_manager.broadcast_to_users(user_ids, event)

    return updated_message


@router.delete("/{id}", response_model=MessageOutput)
async def delete_message(id : int, user_id : int = Depends(get_current_user), db : Session = Depends(get_db)):

    message_service = MessageService(db)

    conversation_service = ConversationService(db)

    try:
        deleted_message = message_service.delete_message(id, user_id)
    except MessageNotFoundError:
        raise HTTPException(status_code=404, detail="Message not found")
    except NotAllowedError:
        raise HTTPException(status_code=403, detail="Message deletion not allowed")
    except MessageAlreadyDeletedError:
        raise HTTPException(status_code=409, detail="Message already deleted")


    event = {
        "event" : EventTypes.MESSAGE_DELETED,
        "payload" : {
            "id" : deleted_message.id,
            "conversation_id" : deleted_message.conversation_id,
            "user_id" : deleted_message.user_id
        }
    }

    conversation = conversation_service.get_conversation_by_id(deleted_message.conversation_id)
    user_ids = (conversation.user_id_1, conversation.user_id_2)

    await ws_manager.broadcast_to_users(user_ids, event)

    return deleted_message