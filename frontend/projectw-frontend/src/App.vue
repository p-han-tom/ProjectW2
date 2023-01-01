<script setup lang="ts">
import Unit from "./components/Unit/Unit.vue";
import WelcomeItem from "./components/WelcomeItem.vue";
</script>

<template>
  <main>
    <WelcomeItem msg="ProjectW" />
  </main>
  <div class="credits">Made by Tom Han, Jerry Lin, Roseak Lin</div>
  <Unit unit-id="moai" :hp="8" :attack="4" />
</template>

<style scoped></style>
