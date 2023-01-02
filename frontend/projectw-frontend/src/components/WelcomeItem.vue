<script lang="ts" setup>
defineProps<{
    msg: string;
}>();
</script>

<template>
    <div>
        <h1 class="page-title">{{ msg }}</h1>
    </div>
</template>

<style scoped>
h1 {
    margin-bottom: 5vh;
    font-size: 8rem;
    text-align: center;
    pointer-events: none;
    user-select: none;
}
</style>
