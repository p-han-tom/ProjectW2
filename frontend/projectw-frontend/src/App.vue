<script setup lang="ts">
import { RouterView } from "vue-router";
</script>

<template>
    <n-theme-editor>
        <RouterView />
    </n-theme-editor>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

import { NThemeEditor } from "naive-ui";
export default defineComponent({
    components: {
        NThemeEditor
    }
})
</script>

<style scoped>

</style>
