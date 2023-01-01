<script lang="ts" setup>
import { RouterLink } from "vue-router";
import WelcomeItem from "../components/WelcomeItem.vue"
import Unit from "../components/Unit/Unit.vue";
</script>

<template>
    <RouterLink to="/chattest">Chat test</RouterLink>
    <WelcomeItem msg="ProjectW" />
    <Unit unit-id="moai" :hp="8" :attack="4" />
</template>