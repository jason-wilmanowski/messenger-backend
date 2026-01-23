from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):

        # stores every connected user -> user_id : [websockets]
        self.active_connections = {}


    # Connect to Websocket
    async def connect(self,user_id : int,  websocket : WebSocket):

        await websocket.accept()

        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()

        self.active_connections[user_id].add(websocket)


    # Disconnect from Websocket
    async def disconnect(self,user_id : int, websocket : WebSocket):

        connections = self.active_connections.get(user_id)

        if not connections:
            return

        connections.discard(websocket)

        if not connections:

            del self.active_connections[user_id]


    # Send data / events to user after input from REST Endpoints
    async def send_to_user(self, user_id: int, data: dict):
        connections = self.active_connections.get(user_id)
        if not connections:
            return

        for websocket in connections:
            try:
                await websocket.send_json(data)
            except Exception as e:
                print(f"Error sending to user {user_id}: {e}")


    # get all active users out of an user id array
    def get_active_users(self, user_ids : set[int]):
        active_users = set()
        for uid in user_ids:
            if uid in self.active_connections:
                active_users.add(uid)
        return active_users


    # Broadcasting system for multiple users
    async def broadcast_to_users(self, user_ids: set[int], data: dict):
        for user_id in user_ids:
            await self.send_to_user(user_id, data)