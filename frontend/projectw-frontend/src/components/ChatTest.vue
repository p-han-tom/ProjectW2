<script setup>
import { onMounted, ref } from "vue";
onMounted(() => {
    document.querySelector("#chat-message-input").focus();

    // fetch("http://locahost:8000/chat/" + roomName.value + "/")
    //     .then(response => console.log(response))
    //     .then(data => {
    //         console.log(data);
    //     })
    //     .catch(error => {
    //         console.log(error);
    //     });
});

const roomName = ref("room1");

const chatSocket = new WebSocket(
    "ws://localhost:8000/ws/chat/" + roomName.value + "/"
);

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    document.querySelector("#chat-log").value += data.message + "\n";
};

chatSocket.onclose = function (e) {
    console.error("Chat socket closed unexpectedly");
};

function chatMsgKeyUp(e) {
    if (e.keyCode === 13) {
        // enter, return
        document.querySelector("#chat-message-submit").click();
    }
}

function chatMsgSubmit(e) {
    const messageInputDom = document.querySelector("#chat-message-input");
    const message = messageInputDom.value;
    chatSocket.send(
        JSON.stringify({
            message: message,
        })
    );
    messageInputDom.value = "";
    roomName.value = "room2";
}
</script>

<template>
    <textarea ref="chatlog" id="chat-log" cols="100" rows="20"></textarea><br />
    <input id="chat-message-input" @keyup="chatMsgKeyUp($event)" type="text" size="100" />
    <br />
    <input id="chat-message-submit" @click="chatMsgSubmit($event)" type="button" value="Send" />
    <div>{{ roomName }}</div>
    <!-- need to change from div. div is temp placeholder -->
</template>
