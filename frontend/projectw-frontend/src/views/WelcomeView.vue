<script lang="ts" setup>
import WelcomeItem from "../components/WelcomeItem.vue";
import Unit from "../components/Unit/Unit.vue";
import { NConfigProvider, NMessageProvider, NSpace, darkTheme } from "naive-ui";
import ThemeOverride from "../assets/NaiveConfigs/ThemeOverride"
import CreateLobbyButton from "@/components/Landing/CreateLobbyButton.vue";
import JoinLobby from "@/components/Landing/JoinLobby.vue";
</script>

<template>
    <NConfigProvider :theme="darkTheme" :theme-overrides="ThemeOverride">
        <WelcomeItem msg="ProjectW" />
        <NSpace vertical :size="[0,25]">
            <CreateLobbyButton />   
            <NMessageProvider>
                <JoinLobby />
            </NMessageProvider>
        </NSpace>
        <!-- <Unit unit-id="moai" :hp="8" :attack="4" /> -->
    </NConfigProvider>
</template>