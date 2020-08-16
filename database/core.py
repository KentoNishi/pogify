import asyncio
import requests
import os

try:
    import personal
except ImportError:
    try:
        from . import personal
    except ImportError:
        pass

try:
    from schemas import SpotifyData, SessionCreate
except ImportError:
    from .schemas import SpotifyData, SessionCreate

from typing import *


async def get_data(uid: str) -> SpotifyData:
    """
    Get the data for the song the streamer with uid is playing.

    (asyncronous)

    :param uid: the uid of the streamer
    :return: the SpotifyData model
    """
    res = await fetch("GET", f"{firebase_url}/{uid}.json")
    return SpotifyData(**res.json())


async def fetch(method: str, *args, **kwargs) -> requests.Response:
    """
    Async version of requests

    :param method: the requests method to use
    :param args, kwargs: the arguments passed to the request
    :return: what request returns
    """
    func = getattr(requests, method.lower())
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, lambda: func(*args, **kwargs))
    return await future


async def set_data(uid: str, data: SpotifyData) -> bool:
    """
    Returns whether the setting of data was successfull.

    (Coroutine)

    :param uid: the uid to set the data at
    :param data: the spotify data to set 
    :return: whether the operation was successful
    """
    res = await fetch("PUT", f"{firebase_url}/{uid}.json", json=data.dict())
    return res.status_code == 200


async def delete_data(uid: str) -> bool:
    """
    Deletes the data at the uid.

    (Coroutine)

    :param uid: the uid to delete the data at
    :return: whether the operation worked
    """
    res = await fetch("DELETE", f"{firebase_url}/{uid}.json")
    return res.status_code == 200


async def main():
    assert await set_data("hello", __dummy_spotify_data())
    print(await get_data("hello"))
    assert await delete_data("hello")


def __dummy_spotify_data() -> SpotifyData:
    data = {
        "room": "mykull",
        "artist": "lily",
        "timestamp_sec": 10,
        "playing": True,
        "event_timestamp": 100,
        "spotify_link": "https://open.spotify.com",
        "video": "watch?q=1234owo"
    }
    return SpotifyData(**data)


try:
    firebase_url = personal.firebase_url
except:
    firebase_url = os.environ["FIREBASE_URL"]

if __name__ == "__main__":
    asyncio.run(main())
