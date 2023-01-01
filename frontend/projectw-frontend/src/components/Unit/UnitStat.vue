<script setup lang="ts">
const props = defineProps<{
    statValue: number;
    iconPath: string;
}>();
</script>
<template>
    <div id="unitStatContainer">
        <img id="statIcon" :src="props.iconPath" draggable="false" />
        <div id="statText">{{ props.statValue }}</div>
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
#unitStatContainer {
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    height: 25px;
    width: 25px;
}
#statIcon {
    position: absolute;
    width: 100%;
}
#statText {
    -moz-user-select: -moz-none;
    -khtml-user-select: none;
    -webkit-user-select: none;
    -ms-user-select: none;
    user-select: none;

    position: absolute;
    font-size: 20px;
    color: white;
    text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000,
        1px 1px 0 #000;
}
</style>
