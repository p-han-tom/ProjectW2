import { createApp } from "vue";
import router from "./router"
import App from "./App.vue";

import { create, NButton, NImage, NSpace } from "naive-ui";

import "./assets/main.css";

const app = createApp(App);
const naive = create({ components: [NButton, NSpace, NImage] });

app.use(router);
app.use(naive);

app.mount("#app");