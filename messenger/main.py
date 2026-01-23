from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from messenger.endpoints import auth, conversations, friends, messages, requests, users
from messenger.websocket import websocket
from messenger.db.database import engine, Base


# erstellt alle table aus dem
Base.metadata.create_all(bind=engine)


app = FastAPI(title="Messenger Backend", version="1.0")


# Rest Endpoints
app.include_router(auth.router, tags=["auth"])
app.include_router(conversations.router,  tags=["conversations"])
app.include_router(friends.router,  tags=["friends"])
app.include_router(messages.router,  tags=["messages"])
app.include_router(requests.router,  tags=["requests"])
app.include_router(users.router,  tags=["users"])


# Websocket Endpoint
app.include_router(websocket.router, tags=["websocket"] )



# granted origins
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:5500/",
    "https://messenger-frontend-git-master-jason-wilmanowskis-projects.vercel.app"
]

# cors middleware for cross origin access to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)