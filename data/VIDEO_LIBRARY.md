# Shared video library

Edit `data/harness-videos.json` to update the video gallery. This is the single authored list for the Learn Harness Engineering website and the harness-engineering repository README.

The VitePress gallery imports this JSON directly. The sync script generates the public JSON feed and the GitHub-compatible thumbnail gallery. It replaces only the marked section in the target README.

```sh
# From the learn-openhands-harness repository:
npm run videos:sync -- --readme ../harness-engineering/README.md
npm run videos:check -- --readme ../harness-engineering/README.md
npm run docs:build
```

Commit the catalog, generated fragment, public feed, and any covers in this repository. Commit the generated README section in harness-engineering. Publish this repository first so the README's shared cover URLs are available. A normal website build refreshes the public feed and generated fragment but never edits another repository.

## Add or update a video

- Keep the stable video `id` when adding platform matches. One video has one card.
- Add only verified public video URLs under `links`. Supported keys are `instagram`, `youtube`, and `tiktok`. Omit unknown links. The first link is the cover/title destination; every known platform appears as a watch link.
- Use a topic ID from `topics`. File order is the default browsing order. Visitors can also sort newest first.
- Save a durable JPEG cover in `docs/public/video-library/covers/`. Set `image` to its relative path. Do not use expiring Instagram CDN URLs.
- Keep `published` as the original publication date. Do not estimate durations.
- Use a short editorial title and a self-contained description. Keep research receipts and evaluation caveats out of gallery copy.

## Initial inventory

The initial 16 shorts are the primary selections from the October 24, 2026 Instagram archive review. Instagram captions and metadata established their topic relevance; video stream metadata established their measured durations. This was not a complete audiovisual review. Two preliminary candidates were excluded after duration verification: the May 3 harness introduction (1,200 seconds) and March 21 skills evaluation upload (574 seconds). They are long uploads, not shorts. The 10 reserve candidates remain in the original audit rather than appearing as duplicates in the initial gallery. The covers were retrieved through the connected account on October 24, 2026. Their pixels are checked into the site, so page visits do not call the Instagram API.

Public feed: `https://rajshah4.github.io/learn-openhands-harness/video-library/catalog.json`.

## Featured talk and YouTube matches

`featuredTalk` holds the wide full-talk card, independently of the shorts and their filters. The May 3, 2026 YouTube page reports a runtime of 2,054 seconds (34:14). Its original YouTube thumbnail is stored locally. Fifteen shorts were matched through the public @rajistics Shorts listing and verified against their titles, publication dates, and runtimes. Their durations agree with the Instagram versions within one second. Unknown matches remain absent.
