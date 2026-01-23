from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from messenger.core.dependencies import get_current_ws_user
from messenger.services.conversation_service import ConversationService
from messenger.websocket import ws_manager
from messenger.services.message_service import MessageService
from messenger.db.database import SessionLocal
from messenger.services.requests_service import RequestsService
from messenger.websocket.events import EventTypes



router = APIRouter(prefix="/ws", tags=["websocket"])

manager = ws_manager


@router.websocket("")
async def websocket_endpoint(websocket : WebSocket):

    db = SessionLocal()
    user_id = None

    try:

        user_id = await get_current_ws_user(websocket)

        await manager.connect(user_id, websocket)

        message_service = MessageService(db)
        request_service = RequestsService(db)

        while True:

            data = await websocket.receive_json()

            if data["event"] == EventTypes.SYNC_REQUEST:
                last_seen_messages = data['payload']['last_seen_messages']
                last_seen_requests = data['payload']['last_seen_requests']

                messages_sync = message_service.sync_messages(last_seen_messages)
                requests_sync = request_service.sync_requests(user_id, last_seen_requests)

                sync = {
                    "event": EventTypes.SYNC,
                    "payload": {
                        "messages": messages_sync,
                        "requests": requests_sync
                    }

                }

                await manager.send_to_user(user_id, sync)

    except WebSocketDisconnect:
        if user_id is not None:
            await manager.disconnect(user_id, websocket)

    finally:
        db.close()