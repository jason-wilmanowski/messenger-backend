from fastapi import APIRouter, Depends, HTTPException, Response
from messenger.core.exceptions import UserExistsError, UserNotFoundError, TokenError, InvalidPasswordError
from messenger.schemes.user import UserOutput, UserCreate, UserUpdate, UsersOutput, UserPasswordUpdate
from messenger.services.user_service import UserService
from sqlalchemy.orm import Session
from messenger.core.dependencies import get_db, get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/create", response_model=UserOutput)
def create_user(user_details : UserCreate, db : Session = Depends(get_db)):

    user_service = UserService(db)

    try:
        new_user = user_service.create_user(user_details.email, user_details.password, user_details.name)
    except UserExistsError:
        raise HTTPException(status_code=401, detail="User with that email already exists")

    return new_user


@router.get("/by-id/{user_id}", response_model=UsersOutput)
def get_user_by_id(user_id : int, db : Session = Depends(get_db)):

    user_service = UserService(db)

    try:
        users = user_service.get_user_by_id(user_id)
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")

    return {"users": [users]}

@router.get("/by-name/{user_name}", response_model=dict)
def get_user_by_name(user_name : str, db : Session = Depends(get_db)):

    user_service = UserService(db)
    try:
        users = user_service.get_user_by_username(user_name)
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="No users with that username found")
    user_outputs = [UserOutput.model_validate(user) for user in users]

    return {"users": user_outputs}


@router.patch("/update", response_model=UserOutput)
def update_user(update_details : UserUpdate,user_id : int = Depends(get_current_user), db : Session = Depends(get_db)):

    user_service = UserService(db)
    try:
        updated_user = user_service.update_user(user_id, update_details.model_dump(exclude_unset=True))
    except TokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user


@router.patch("/update-password", response_model=dict)
def update_password(update_details : UserPasswordUpdate, user_id : int = Depends(get_current_user), db : Session = Depends(get_db)):

    user_service = UserService(db)

    try:
        user_service.update_user_password(update_details.password, user_id, update_details.new_password)
    except InvalidPasswordError:
        raise HTTPException(status_code=401, detail="Current Password is invalid")

    return {"success" : True, "message" : "Password updated successfully"}


@router.post("/deactivate", response_model=UserOutput)
def deactivate_user(response : Response , user_id : int = Depends(get_current_user), db : Session = Depends(get_db)):

    user_service = UserService(db)

    try:
        user = user_service.deactivate_user(user_id)
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")

    response.delete_cookie("refresh_token")

    return user

