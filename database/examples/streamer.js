url = "http://127.0.0.1:5000";

async function create_session() {
    await fetch(url + "/create", {
        method: "POST",
        body: {
            name: "mykull"
        }
    });
}

async function update_session() {
    await fetch(url + "/update", {
        method: "POST",
        body: {
            room: "mykull",
            artist: "lily",
            timestamp_sec: 1,
            playing: true,
            event_timestamp: 2,
            spotify_link: "https://open.spotify.com",
            video: "/watch?v=345"
        }
    });
}

async function delete_session() {
    await fetch(url + "/delete", {
        method: "POST",
        body: {
            name: "mykull"
        }
    });
}

async function main() {
    await create_session();
    await update_session();
    await delete_session();
}

main().then()
