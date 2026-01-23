from fastapi import WebSocket
from messenger.core.security import decode_access_token
from messenger.core.exceptions import TokenError


async def get_current_user(websocket: WebSocket):

    token = websocket.query_params.get('token')

    if not token:
        await websocket.close(code=1008)
        raise TokenError('missing token')

    try:
        user_id = decode_access_token(token)
        return user_id
    except TokenError:
        await websocket.close(code=1008)
        raise