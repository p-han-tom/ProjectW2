<script setup lang="ts">
import UnitStat from "./UnitStat.vue";
import { computed } from "vue";

const props = defineProps<{
    unitId: string;
    hp: number;
    attack: number;
}>();
const unitIdTable: Record<string, string> = {
    moai: "src/assets/units/moai.svg",
};
const unitIcon = computed(() => unitIdTable[props.unitId]);
</script>
<template>
    <div id="container">
        <img id="unitIcon" :src="unitIcon" draggable="false" />
        <div id="statsContainer">
            <UnitStat
                class="stat"
                icon-path="src/assets/icons/heart.svg"
                :stat-value="hp"
            />
            <UnitStat
                class="stat"
                icon-path="src/assets/icons/dagger.svg"
                :stat-value="attack"
            />
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
