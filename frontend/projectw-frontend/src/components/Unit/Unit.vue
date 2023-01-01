<script setup lang="ts">
import UnitStat from "./UnitStat.vue";
import { computed } from "@vue/reactivity";

const props = defineProps<{
  unitId: string;
  hp: number;
  attack: number;
}>();

function getIconPath(id: string): string {
  switch (id) {
    case "moai":
      return "src/assets/units/moai.svg";
  }
  return "";
}
const unitIcon = computed(() => getIconPath(props.unitId));
const hpIcon = "src/assets/icons/heart.svg";
const attackIcon = "src/assets/icons/dagger.svg";
</script>
<template>
  <div id="container">
    <img id="unitIcon" :src="unitIcon" draggable="false" />
    <div id="statsContainer">
      <UnitStat class="stat" :icon-path="hpIcon" :stat-value="hp" />
      <UnitStat class="stat" :icon-path="attackIcon" :stat-value="attack" />
    </div>
  </div>
</template>
<style scoped>
img {
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -o-user-select: none;
  user-select: none;
}
#container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100px;
  height: 100px;
}
#unitIcon {
  width: 80%;
}
#statsContainer {
  position: absolute;
  top: 0;
  right: 0;
}
</style>
