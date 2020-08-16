from pydantic import BaseModel

class SessionCreate(BaseModel):
    name: str

class SpotifyData(BaseModel):
    """The data sent to the server from the streamer"""
    room: str
    artist: str
    timestamp_sec: int
    playing: bool
    event_timestamp: int
    spotify_link: str
    video: str
