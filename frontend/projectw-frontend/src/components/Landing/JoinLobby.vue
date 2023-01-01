<script setup lang="ts">
import {
    NButton,
    NInput,
    NSpace,
    useMessage,
    type MessageReactive,
    type MessageType,
} from "naive-ui";
import { ref } from "vue";

const inputGameCode = ref<null | typeof NInput>(null);
const message = useMessage();
let msgReactive: MessageReactive | null = null;

function handleJoinLobby() {
    // Do nothing if inputGameCode ref is not initialized yet
    if (!inputGameCode.value) return;

    msgReactive = message.loading("Attempting to join game...");

    let gameCode: string = inputGameCode.value.inputElRef.value;

    // Make HTML request to backend to check if the lobby exists. If it does, join it
    fetch(gameCode)
        .then((res) => {
            switch (res.status) {
                case 200:
                    updateMsgReactive(
                        "Game found. Attempting to join...",
                        "success"
                    );
                    console.log(res);
            }
        })
        .catch((e) => {
            updateMsgReactive("Could not join game.", "error");
            console.log(e);
        });
}
function updateMsgReactive(content: string, type: MessageType) {
    if (!msgReactive) return;
    msgReactive.content = content;
    msgReactive.type = type;
    msgReactive.duration = 5000;
}
</script>
<template>
    <NSpace>
        <NInput
            type="text"
            placeholder="Game code"
            clearable
            ref="inputGameCode"
        ></NInput>
        <NButton @click="handleJoinLobby">Join Game</NButton>
    </NSpace>
</template>
