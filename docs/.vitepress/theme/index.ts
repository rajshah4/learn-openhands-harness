import DefaultTheme from "vitepress/theme";
import type { Theme } from "vitepress";
import { installAnalytics } from "./analytics";
import AgentFlightConsole from "./components/AgentFlightConsole.vue";
import HomeFlightTeaser from "./components/HomeFlightTeaser.vue";
import ReferenceLibrary from "./components/ReferenceLibrary.vue";
import VideoGallery from "./components/VideoGallery.vue";
import "./custom.css";

export default {
  extends: DefaultTheme,
  enhanceApp({ app, router }) {
    installAnalytics(router);
    app.component("AgentFlightConsole", AgentFlightConsole);
    app.component("HomeFlightTeaser", HomeFlightTeaser);
    app.component("VideoGallery", VideoGallery);
    app.component("ReferenceLibrary", ReferenceLibrary);
  },
} satisfies Theme;
