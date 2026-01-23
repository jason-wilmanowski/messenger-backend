from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from messenger.services.conversation_service import ConversationService
from messenger.schemes.conversation import ConversationCreate, ConversationOutput, UserConversationsOutput, \
    ConversationCreateOrGet
from messenger.core.dependencies import get_current_user, get_db
from messenger.core.exceptions import ConversationExistsError, UserNotFoundError, SameUserIDError, \
    ConversationNotFoundError

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("", response_model=ConversationOutput)
def create_conversation(user_id_2 : int, user_id_1 : int = Depends(get_current_user), db: Session = Depends(get_db)):

    conv_service = ConversationService(db)

    try:
        created_conversation = conv_service.create_conversation(user_id_1, user_id_2)
    except ConversationExistsError:
        raise HTTPException(status_code=409, detail="Conversation already exists")
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="Requested User not found")
    except SameUserIDError:
        raise HTTPException(status_code=409, detail ="Cannot start conversation with same user")

    return created_conversation


@router.post("/create-get", response_model=ConversationOutput)
def create_or_get_conversation(user_id : ConversationCreateOrGet, user_id_1 : int = Depends(get_current_user), db: Session = Depends(get_db)):

    conv_service = ConversationService(db)
    return conv_service.create_or_get_conversation(user_id.user_id_2, user_id_1)


@router.get("", response_model=UserConversationsOutput)
def get_user_conversations(user_id : int = Depends(get_current_user), db : Session = Depends(get_db)):

    conv_service = ConversationService(db)

    conversations = conv_service.get_user_conversation(user_id)

    if not conversations:
        return {"conversations": []}

    return {"conversations" : conversations}


@router.get("/{id}", response_model=ConversationOutput)
def get_conversation(id: int, db : Session = Depends(get_db)):

    conv_service = ConversationService(db)

    conversation = conv_service.get_conversation_by_id(id)

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return conversation




