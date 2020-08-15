# from flask import Flask, request
# from flask_cors import CORS
# from flask_socketio import SocketIO
# from firebase import Firebase


# app = Flask(__name__)
# CORS(app)
# 
# socketio = SocketIO(app, logger=True, engineio_logger=True)
# 
# @app.route("/")
# def index():
#     return "Pogify websocket database interface"
# 
# 
# @app.route("/create", methods=["POST"])
# def create_user

import socketio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

fapp = FastAPI()

origins = [
    "*"
]

fapp.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = socketio.ASGIApp(
    socketio_server=sio,
    other_asgi_app=fapp,
    socketio_path="/socket.io/"
)

class SessionCreate(BaseModel):
    name: str

class SpotifyData(BaseModel):
    room: str
    data: str

@fapp.get("/", response_class=HTMLResponse)
async def index():
    with open("index.html", 'r') as fin:
        return fin.read()


@fapp.post("/create")
async def create_session(session: SessionCreate):
    return session


@fapp.post("/update")
async def update_session(data: SpotifyData):
    await sio.emit("onchange", {"data": data.data}, room=data.room)


@sio.on("join")
async def begin_chat(sid, data):
    sio.enter_room(sid, data["stream"])
    await sio.emit("onchange", {"data": f"{sid} has joined"}, room=data["stream"])

