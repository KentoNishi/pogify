var socket = io.connect("http://127.0.0.1:5000/");

var mydata = {
    uid: undefined
};

socket.on("connect", () => {
    console.log("hey");
    socket.emit("join", {"stream": "mykull"});
})

socket.on("onchange", (msg) => {
    console.log(msg.data);
})
