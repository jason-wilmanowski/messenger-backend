from messenger.websocket.events import EventTypes
from fastapi import APIRouter, HTTPException, Depends
from messenger.services.friends_service import FriendsService
from messenger.core.exceptions import FriendshipNotFoundError, NoFriendsFoundError
from messenger.schemes.friend import FriendsOutput, FriendsItem, FriendshipOutput
from messenger.core.dependencies import get_current_user, get_db
from sqlalchemy.orm import Session
from messenger.websocket import ws_manager

router = APIRouter(prefix="/friends", tags=["friends"])



@router.get("/all", response_model=FriendsOutput)
def get_all_friends(user_id : int = Depends(get_current_user), db : Session = Depends(get_db)):

    friends_service = FriendsService(db)

    try:
        friends = friends_service.get_friends(user_id)
    except NoFriendsFoundError:
        return {"friends" : []}

    return {"friends" : friends}

@router.get("/active", response_model=dict)
def get_active_friends(user_id : int = Depends(get_current_user), db : Session = Depends(get_db)):

    friends_service = FriendsService(db)
    try:
        all_friends = friends_service.get_friends(user_id)
    except NoFriendsFoundError:
        return {"active_friends" : []}
    all_friend_ids = {f.id for f in all_friends}
    active_friends = ws_manager.get_active_users(all_friend_ids)

    return {"active_friends" : list(active_friends)}

@router.get("/{friend_id}", response_model=FriendshipOutput)
def get_friendship(friend_id : int,user_id : int = Depends(get_current_user), db : Session = Depends(get_db)):

    friends_service = FriendsService(db)
    try:
        friendship = friends_service.get_friendship(user_id, friend_id)
    except FriendshipNotFoundError:
        raise HTTPException(status_code=404, detail="No friendship found")

    return {"friendship" : friendship}


@router.delete("/{friend_id}", response_model=FriendshipOutput)
async def delete_friendship(friend_id : int, user_id : int = Depends(get_current_user), db : Session = Depends(get_db)):

    friends_service = FriendsService(db)

    try:
        deleted_friendship = friends_service.delete_friendship(friend_id, user_id)
    except FriendshipNotFoundError:
        raise HTTPException(status_code=404, detail="No friendship found")

    event = {
        "event" : EventTypes.FRIENDSHIP_DELETED,
        "payload" : {
            "id" : deleted_friendship.id,
            "user_id_1" : deleted_friendship.user_id_1,
            "user_id_2" : deleted_friendship.user_id_2,
            "created_at" : deleted_friendship.created.isoformat(),
        }
    }

    user_ids = (deleted_friendship.user_id_1, deleted_friendship.user_id_2)
    await ws_manager.broadcast_to_users(user_ids, event)

    deleted_friendship.created = deleted_friendship.created.isoformat()
    return deleted_friendship