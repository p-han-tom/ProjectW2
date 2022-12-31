import { createApp } from "vue";
import App from "./App.vue";

import { create, NButton, NImage, NSpace } from "naive-ui";

import "./assets/main.css";

const app = createApp(App);
const naive = create({ components: [NButton, NSpace, NImage] });

app.use(naive).mount("#app");
