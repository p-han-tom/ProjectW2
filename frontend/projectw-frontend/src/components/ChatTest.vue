<template>
    <textarea ref="chatlog" id="chat-log" cols="100" rows="20"></textarea><br />
    <input id="chat-message-input" @keyup="chatMsgKeyUp($event)" type="text" size="100" />
    <br />
    <input id="chat-message-submit" @click="chatMsgSubmit($event)" type="button" value="Send" />
    <div ref="room_name" id="room_name" v-html="roomNameJson"></div>
    <!-- need to change from div. div is temp placeholder -->
</template>

<script>
export default {
    mounted() {
        document.querySelector("#chat-message-input").focus();
        //     const roomName = JSON.parse(
        //         document.querySelector("#room_name").textContent
        //     );

        //     const chatSocket = new WebSocket(
        //         new WebSocket('ws://' + window.location.host + '/ws/match/' + roomName + '/')
        //     );

        //     chatSocket.onmessage = function (e) {
        //         const data = JSON.parse(e.data);
        //         document.querySelector("#chat-log").value += data.message + "\n";
        //     };

        //     chatSocket.onclose = function (e) {
        //         console.error("Chat socket closed unexpectedly");
        //     };
    },
    methods: {
        chatMsgKeyUp(e) {
            if (e.keyCode === 13) {
                // enter, return
                document.querySelector("#chat-message-submit").click();
            }
        },
        chatMsgSubmit(e) {
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
        },
    },
    data() {
        return {
            roomName: "room1",
        };
    },
    computed: {
        roomNameJson() {
            return JSON.stringify({ room_name: this.roomName });
        },
    },
};
</script>
