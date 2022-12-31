<script lang="ts" setup>
defineProps<{
  msg: string
}>()
</script>

<template>
  <div>
    <h1 class="page-title">{{ msg }}</h1>
  </div>
</template>

<style scoped>
</style>
