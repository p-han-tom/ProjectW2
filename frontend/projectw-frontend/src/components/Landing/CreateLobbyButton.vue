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
    <div>
        <NButton size="large" strong @click="handleCreateLobby">Create Game</NButton>
    </div>
</template>

<style scoped>
button {
    text-align: center;
    font-size: 1.25rem;
    display: block;
    margin: 0 auto;
    width: 50%;
    height: 3rem;
}
</style>