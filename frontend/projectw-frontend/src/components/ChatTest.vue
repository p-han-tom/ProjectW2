<script setup>
document.querySelector("#chat-message-input").focus();
// const roomName = JSON.parse(
//     document.querySelector("#room_name").textContent
// );

// const chatSocket = new WebSocket(
//     new WebSocket('ws://' + window.location.host + '/ws/match/' + roomName + '/')
// );

// chatSocket.onmessage = function (e) {
//     const data = JSON.parse(e.data);
//     document.querySelector("#chat-log").value += data.message + "\n";
// };

// chatSocket.onclose = function (e) {
//     console.error("Chat socket closed unexpectedly");
// };

const chatMsgKeyUp = (e) => {
    if (e.keyCode === 13) {
        // enter, return
        document.querySelector("#chat-message-submit").click();
    }
}

const chatMsgSubmit = (e) => {
    const messageInputDom = document.querySelector(
        "#chat-message-input"
    );
    const message = messageInputDom.value;
    // chatSocket.send(
    //     JSON.stringify({
    //         message: message,
    //     })
    // );
    document.querySelector("#chat-log").value += message + "\n";
    messageInputDom.value = "";
}

const roomName = "room1"
const roomNameJson = () => {
    return JSON.stringify({ room_name: this.roomName });
}
</script>


<template>
    <textarea ref="chatlog" id="chat-log" cols="100" rows="20"></textarea><br />
    <input id="chat-message-input" @keyup="chatMsgKeyUp($event)" type="text" size="100" />
    <br />
    <input id="chat-message-submit" @click="chatMsgSubmit($event)" type="button" value="Send" />
    <!-- need to change from div. div is temp placeholder -->
</template>
