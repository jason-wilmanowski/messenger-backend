from fastapi import HTTPException, Depends, WebSocket, WebSocketException, status
from messenger.core.security import decode_access_token
from messenger.db.database import SessionLocal
from messenger.core.exceptions import TokenError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials



security = HTTPBearer()


# validate JWT from REST endpoints and return UserID (int)
def get_current_user(credentials : HTTPAuthorizationCredentials = Depends(security)) -> int:
    token = credentials.credentials
    try:
        return decode_access_token(token)
    except TokenError as e:
        raise HTTPException(status_code=401, detail=str(e), headers={"WWW-Authenticate": "Bearer"})



# validate JWT from WebSocket Query params and return UserID (int)
async def get_current_ws_user(websocket : WebSocket) -> int:

    token = websocket.query_params.get('token')
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    try:
        user_id = decode_access_token(token)
        return user_id
    except TokenError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)



# open and close DB Session for dependency injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()