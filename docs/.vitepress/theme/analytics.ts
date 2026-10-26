import { inBrowser, type Router } from "vitepress";

const endpoint = "https://learn-harness-engineering.goatcounter.com/count";
const siteHost = "rajshah4.github.io";
const siteBase = "/learn-openhands-harness/";

type Count = {
  path: string;
  title?: string;
  event?: boolean;
};

declare global {
  interface Window {
    goatcounter?: {
      no_onload?: boolean;
      count?: (values: Count) => void;
    };
  }
}

// Keep the destination stable and omit query strings and fragment identifiers.
export function resourceEvent(url: URL): string | undefined {
  if (!/^https?:$/.test(url.protocol)) return;
  if (/\.(pdf|zip)$/i.test(url.pathname)) {
    return `download-${url.pathname.split("/").pop()}`;
  }
  if (url.hostname === "github.com" || url.hostname === "www.github.com") {
    return `github-${url.pathname.replace(/^\//, "")}`;
  }
  if (["youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be",
    "instagram.com", "www.instagram.com", "vimeo.com", "www.vimeo.com"].includes(url.hostname)) {
    const video = url.hostname.endsWith("youtube.com") && url.pathname === "/watch"
      ? `/watch/${encodeURIComponent(url.searchParams.get("v") ?? "unknown")}`
      : url.pathname;
    return `video-${url.hostname}${video}`;
  }
}

export function installAnalytics(router: Router) {
  if (!inBrowser || location.hostname !== siteHost || !location.pathname.startsWith(siteBase)) return;
  if (document.querySelector("script[data-goatcounter]")) return;

  let lastPath = "";
  const countPage = () => {
    const count = window.goatcounter?.count;
    if (!count || lastPath === location.pathname) return;
    lastPath = location.pathname;
    count({ path: lastPath, title: document.title });
  };

  const previousRouteChange = router.onAfterRouteChange;
  router.onAfterRouteChange = async (to) => {
    await previousRouteChange?.(to);
    countPage();
  };

  document.addEventListener("click", (event) => {
    const anchor = event.target instanceof Element ? event.target.closest("a") : null;
    if (!anchor?.href) return;
    const name = resourceEvent(new URL(anchor.href));
    if (!name) return;
    // Include the source in the event name so the dashboard keeps sources separate.
    window.goatcounter?.count?.({
      path: `${name} (from ${location.pathname})`,
      title: `${anchor.textContent?.trim().replace(/\s+/g, " ").slice(0, 150) || name} (from ${location.pathname})`,
      event: true,
    });
  }, { capture: true });

  // Count the current route when the async script is ready, even after a quick navigation.
  window.goatcounter = { no_onload: true };
  const script = document.createElement("script");
  script.async = true;
  script.src = "https://gc.zgo.at/count.js";
  script.dataset.goatcounter = endpoint;
  script.onload = countPage;
  document.head.appendChild(script);
}
