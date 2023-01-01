<script lang="ts" setup>
import { RouterLink } from "vue-router";
import WelcomeItem from "../components/WelcomeItem.vue";
import Unit from "../components/Unit/Unit.vue";
import { NConfigProvider, NMessageProvider, NSpace, darkTheme } from "naive-ui";
import CreateLobbyButton from "@/components/Landing/CreateLobbyButton.vue";
import JoinLobby from "@/components/Landing/JoinLobby.vue";
</script>

<template>
    <NConfigProvider :theme="darkTheme">
        <RouterLink to="/chattest">Chat test</RouterLink>
        <WelcomeItem msg="ProjectW" />
        <NSpace vertical>
            <CreateLobbyButton />
            <NMessageProvider>
                <JoinLobby />
            </NMessageProvider>
        </NSpace>
        <Unit unit-id="moai" :hp="8" :attack="4" />
    </NConfigProvider>
</template>
