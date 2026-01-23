from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlalchemy.orm import Session
from messenger.core.exceptions import TokenError, UserNotFoundError, InvalidPasswordError
from messenger.services.auth_service import AuthService
from messenger.schemes.user import  UserLogin
from messenger.core.dependencies import get_db
from messenger.core.security import create_access_token, create_refresh_token, decode_refresh_token
from messenger.schemes.auth import TokenOutput


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenOutput)
def login(login_data: UserLogin,response: Response, db : Session = Depends(get_db)):

    auth_service = AuthService(db)

    try:
        user = auth_service.validate_login(login_data.email, login_data.password)
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User email not found")
    except InvalidPasswordError:
        raise HTTPException(status_code=401, detail="Invalid password")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    response.set_cookie(key="refresh_token",
                        value=refresh_token,
                        httponly=True,
                        secure=True,
                        samesite="strict",
                        max_age=30*24*3600)

    return {
            "access_token" : access_token,
            "token_type" : "bearer",
            "user_id" : user.id,
            }



@router.post("/refresh", response_model=TokenOutput)
def refresh( response : Response,refresh_token : str = Cookie(None)):

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token required")

    try:
        user_id = decode_refresh_token(refresh_token)
    except TokenError:
        raise HTTPException(status_code=401, detail=str(TokenError))
    if not user_id:
        raise HTTPException(status_code=401, detail="Could not validate the refresh token")

    new_token = create_access_token(user_id)
    new_refresh_token = create_refresh_token(user_id)

    response.set_cookie(key="refresh_token",
                        value=new_refresh_token,
                        httponly=True,
                        secure=True,
                        samesite="strict",
                        max_age=30*24*3600)

    return {
            "access_token" : new_token,
            "token_type" : "bearer",
            "user_id" : user_id,
            }

