import socketio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

try:
    from . import core
    from .schemas import SpotifyData, SessionCreate
except:
    import core
    from schemas import SpotifyData, SessionCreate

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


@fapp.get("/", response_class=HTMLResponse)
async def index():
    with open("index.html", 'r') as fin:
        return fin.read()


@fapp.post("/create")
async def create_session(session: SessionCreate):
    return session


@fapp.post("/update")
async def update_session(data: SpotifyData):
    await sio.emit("onchange", {"data": data.dict()}, room=data.room)
    await core.set_data(data.room, data)


@fapp.post("/delete")
async def delete(session: SessionCreate):
    await core.delete_data(session.name)


@sio.on("join")
async def begin_chat(sid, data):
    """
    Joins user into chat room and sends them data

    sends: {
        data: SpotifyData
        success: bool
    }
    """
    sio.enter_room(sid, data["stream"])
    try:
        data = await core.get_data(data["stream"])
        data = data.dict()
        data["success"] = True
    except:
        data = {"success": False}
    await sio.emit("onchange", {"data": data}, room=sid)
