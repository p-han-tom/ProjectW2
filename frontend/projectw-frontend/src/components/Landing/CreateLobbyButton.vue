<script setup lang="ts">
import { NButton } from "naive-ui";

function handleCreateLobby() {
    fetch("http://127.0.0.1:8000/lobby/createLobby/")
        .then((res) => {
            switch (res.status) {
                case 200:
                    res.json().then((res) => {
                        const lobbyCode: string = res.lobby_code;
                        // Redirect to lobby
                    });
            }
        })
        .catch((e) => {
            console.log(e);
        });
}
</script>
<template>
    <NButton @click="handleCreateLobby">Create Game</NButton>
</template>
