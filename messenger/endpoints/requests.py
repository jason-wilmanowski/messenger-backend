from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from messenger.core.dependencies import get_current_user, get_db
from messenger.services.requests_service import RequestsService
from messenger.core.exceptions import RequestNotFoundError, RequestBlockedError, FriendshipExistsError, \
    RequestExistsError, NoRequestsFoundError, SameUserIDError
from messenger.schemes.request import RequestOutput, RequestsOutput, UpdateRequestOutput, CreateRequest, \
    UpdateRequestInput, UpdateSentRequestInput, BlockedRequestsOutput
from messenger.websocket.events import EventTypes
from messenger.websocket import ws_manager


router = APIRouter(prefix="/requests", tags=["requests"])



@router.post("/create", response_model=RequestOutput)
async def create_request(rec_user_id : CreateRequest , user_id : int = Depends(get_current_user), db : Session = Depends(get_db)):

    request_service = RequestsService(db)

    try:
        request = request_service.create_request(user_id, rec_user_id.id)
    except RequestExistsError:
        raise HTTPException(status_code=409, detail="Request already exists")
    except FriendshipExistsError:
        raise HTTPException(status_code=409, detail="Friendship already exists")
    except RequestBlockedError:
        raise HTTPException(status_code=409, detail="User blocked your requests")
    except SameUserIDError:
        raise HTTPException(status_code=409, detail="Cannot create request with same user id")

    event = {
        "event" : EventTypes.REQUEST_NEW,
        "payload" : {
            "id" : request.id,
            "send_user_id" : request.send_user_id,
            "rec_user_id" : request.rec_user_id,
            "status" : request.status,
            "created" : request.created.isoformat(),
        }
    }

    user_ids = (request.send_user_id, request.rec_user_id)

    await ws_manager.broadcast_to_users(user_ids, event)

    return request

@router.get("/blocked", response_model=BlockedRequestsOutput)
def get_blocked_requests(user_id : int = Depends(get_current_user), db : Session = Depends(get_db)):
    request_service = RequestsService(db)

    try:
        blocked_requests = request_service.get_blocked_requests(user_id)
    except NoRequestsFoundError:
        return {"blocked_requests" : []}
    return {"blocked_requests" : blocked_requests}

@router.get("/{id}", response_model=RequestOutput)
def get_request(id: int, db : Session = Depends(get_db)):

    request_service = RequestsService(db)

    try:
        request = request_service.get_request_by_id(id)
    except RequestNotFoundError:
        raise HTTPException(status_code=404, detail="Request not found")

    return request



@router.post("/get", response_model=RequestsOutput)
def get_received_requests(user_id : int = Depends(get_current_user), db: Session = Depends(get_db)):

    request_service = RequestsService(db)

    try:
        requests = request_service.get_rec_requests(user_id)
    except NoRequestsFoundError:
        return {"requests" : []}

    return {"requests" : requests}


@router.post("/send", response_model=RequestsOutput)
def get_sent_requests(user_id : int = Depends(get_current_user), db: Session = Depends(get_db)):

    request_service = RequestsService(db)

    try:
        requests = request_service.get_sent_requests(user_id)
    except NoRequestsFoundError:
        return {"requests": []}

    return {"requests" : requests}


@router.post("/update", response_model=dict)
async def update_request(update_details : UpdateRequestInput, user_id : int = Depends(get_current_user), db : Session = Depends(get_db)):

    request_service = RequestsService(db)

    try:
        request = request_service.update_request(update_details.send_user_id, user_id, update_details.status)
    except RequestNotFoundError:
        raise HTTPException(status_code=404, detail="Request not found")

    req = request["request"]

    event = {
        "event" : EventTypes.REQUEST_UPDATED,
        "payload" : {
            "id" : req.id,
            "send_user_id" : req.send_user_id,
            "rec_user_id" : req.rec_user_id,
            "status" : req.status,
            "created_at" : req.created.isoformat(),
        }
    }

    user_ids = (req.send_user_id, req.rec_user_id)


    await ws_manager.broadcast_to_users(user_ids, event)

    if request["friendship"]:
        friendship = request["friendship"]

        event_fr = {
            "event" : EventTypes.FRIENDSHIP_NEW,
            "payload": {
                "id" : friendship.id,
                "user_id_1" : friendship.user_id_1,
                "user_id_2" : friendship.user_id_2,
                "created_at" : friendship.created.isoformat()
            }
        }

        await ws_manager.broadcast_to_users(user_ids, event_fr)

    return {"success" : True}



@router.post("/update-sent", response_model=dict)
async def update_sent_requests(update_details : UpdateSentRequestInput,user_id : int = Depends(get_current_user), db : Session = Depends(get_db)):

    request_service = RequestsService(db)

    try:
        request = request_service.update_request(user_id, update_details.rec_user_id, update_details.status)
    except RequestNotFoundError:
        raise HTTPException(status_code=404, detail="Request not found")

    req = request["request"]

    event = {
        "event": EventTypes.REQUEST_UPDATED,
        "payload": {
            "id": req.id,
            "send_user_id": req.send_user_id,
            "rec_user_id": req.rec_user_id,
            "status": req.status,
            "created_at": req.created.isoformat(),
        }
    }

    user_ids = (req.send_user_id, req.rec_user_id)

    await ws_manager.broadcast_to_users(user_ids, event)

    return {"success": True}
