import { defineConfig } from "vitepress";

export default defineConfig({
  title: "Learn Harness Engineering with OpenHands",
  description:
    "A hands-on course for learning harness engineering with OpenHands, Agent Canvas, the SDK, traces, metrics, and model routing.",
  base: "/learn-openhands-harness/",
  cleanUrls: true,
  themeConfig: {
    siteTitle: "Learn Harness Engineering with OpenHands",
    nav: [
      { text: "Start", link: "/start-here" },
      { text: "Concepts", link: "/concepts/" },
      { text: "Projects", link: "/projects/" },
      { text: "Library", link: "/library/" },
      { text: "Videos", link: "/videos" },
      {
        text: "GitHub",
        link: "https://github.com/rajshah4/learn-openhands-harness",
      },
    ],
    sidebar: {
      "/concepts/": [
        {
          text: "Concepts",
          items: [
            { text: "Overview", link: "/concepts/" },
            { text: "Why OpenHands", link: "/concepts/why-openhands" },
            { text: "Visual Intro", link: "/concepts/visual-intro" },
            { text: "Harness Levers", link: "/concepts/harness-levers" },
            { text: "Experiments", link: "/concepts/experiments" },
          ],
        },
      ],
      "/projects/": [
        {
          text: "Projects",
          items: [
            { text: "Overview", link: "/projects/" },
            { text: "P01: Agent Trace", link: "/projects/p01-agent-trace" },
            { text: "P02: Model Routing", link: "/projects/p02-model-routing" },
            { text: "P03: Retrieval", link: "/projects/p03-retrieval" },
            { text: "P04: Decomposition", link: "/projects/p04-decomposition" },
            { text: "P05: Memory", link: "/projects/p05-memory" },
            { text: "P06: Safety", link: "/projects/p06-safety" },
            { text: "P07: Critic Capstone", link: "/projects/p07-capstone" },
            { text: "P08: Dynamic Workflows", link: "/projects/p08-dynamic-workflows" },
            { text: "P09: Model Routing Benchmark", link: "/projects/p09-model-routing-benchmark" },
            { text: "P10: Indexing Agent History", link: "/projects/p10-history-index" },
          ],
        },
      ],
      "/library/": [
        {
          text: "Library",
          items: [
            { text: "Overview", link: "/library/" },
            { text: "Copy-Ready Artifacts", link: "/library/artifacts" },
            { text: "Trace Checklist", link: "/library/trace-checklist" },
          ],
        },
      ],
      "/": [
        {
          text: "Course",
          items: [
            { text: "Home", link: "/" },
            { text: "Start Here", link: "/start-here" },
            { text: "Quickstart", link: "/quickstart" },
            { text: "Harness Tour", link: "/harness-tour" },
            { text: "Videos", link: "/videos" },
          ],
        },
      ],
    },
    socialLinks: [
      {
        icon: "github",
        link: "https://github.com/rajshah4/learn-openhands-harness",
      },
      {
        icon: "youtube",
        link: "https://www.youtube.com/watch?v=KijChx7q2nY",
      },
    ],
    footer: {
      message:
        "Built as a friendly front door for the runnable OpenHands harness lab.",
      copyright: "MIT Licensed",
    },
    search: {
      provider: "local",
    },
  },
});
