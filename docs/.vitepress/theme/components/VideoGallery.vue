<script setup>
import { computed, ref } from 'vue';
import { withBase } from 'vitepress';
import catalog from '../../../../data/harness-videos.json';

const query = ref('');
const topic = ref('all');
const order = ref('topic');
const failedImages = ref(new Set());
const platforms = { instagram: 'Instagram', youtube: 'YouTube', tiktok: 'TikTok' };
const labels = Object.fromEntries(catalog.topics.map(t => [t.id, t.label]));
const counts = Object.fromEntries(catalog.topics.map(t => [t.id, catalog.videos.filter(v => v.topic === t.id).length]));
const videos = computed(() => {
  const search = query.value.trim().toLowerCase();
  const matches = catalog.videos.filter(v => (topic.value === 'all' || v.topic === topic.value)
    && `${v.title} ${v.description} ${labels[v.topic]}`.toLowerCase().includes(search));
  return order.value === 'newest' ? matches.sort((a, b) => b.published.localeCompare(a.published)) : matches;
});
function reset() { query.value = ''; topic.value = 'all'; }
function formatDate(date) {
  return new Intl.DateTimeFormat('en-US', { month: 'short', year: 'numeric', timeZone: 'UTC' }).format(new Date(`${date}T12:00:00Z`));
}
function imageFailed(id) { failedImages.value = new Set([...failedImages.value, id]); }
function duration(seconds) { return `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, '0')}`; }
</script>

<template>
  <section class="video-library" aria-label="Harness engineering video library">
    <article v-if="catalog.featuredTalk" class="featured-talk" aria-label="Featured full talk">
      <a class="featured-cover" :href="catalog.featuredTalk.links.youtube" target="_blank" rel="noopener noreferrer" :aria-label="`Watch ${catalog.featuredTalk.title} on YouTube (opens in a new tab)`">
        <img :src="withBase(`/video-library/${catalog.featuredTalk.image}`)" alt="" width="1920" height="1080" />
        <span class="video-play" aria-hidden="true">▶</span><span class="video-duration">{{ duration(catalog.featuredTalk.durationSeconds) }}</span>
      </a>
      <div class="featured-info">
        <p class="featured-label">FULL TALK <span aria-hidden="true">/</span> {{ formatDate(catalog.featuredTalk.published) }}</p>
        <h2><a :href="catalog.featuredTalk.links.youtube" target="_blank" rel="noopener noreferrer">{{ catalog.featuredTalk.title }}</a></h2>
        <p>{{ catalog.featuredTalk.description }}</p>
        <div class="featured-links"><a :href="catalog.featuredTalk.links.youtube" target="_blank" rel="noopener noreferrer">Watch on YouTube <span aria-hidden="true">↗</span></a><a v-for="(url, label) in catalog.featuredTalk.resources" :key="label" :href="url">{{ label }}</a></div>
      </div>
    </article>
    <div class="library-intro">
      <p>Short explainers on tools, memory, routing, verification, and agent teams. Pick a topic or find a specific idea.</p>
      <span class="library-stat">{{ catalog.videos.length }} shorts <span aria-hidden="true">/</span> {{ catalog.topics.length }} topics <span aria-hidden="true">/</span> by Rajiv Shah</span>
    </div>
    <div class="library-controls">
      <label class="library-search">Find a video<input v-model="query" type="search" placeholder="Try compaction, skills, or routing" /></label>
      <label class="library-sort">Browse order<select v-model="order"><option value="topic">By topic</option><option value="newest">Newest first</option></select></label>
    </div>
    <div class="library-topics" role="group" aria-label="Filter by topic">
      <button type="button" :aria-pressed="topic === 'all'" @click="topic = 'all'">All topics <span>{{ catalog.videos.length }}</span></button>
      <button v-for="t in catalog.topics" :key="t.id" type="button" :aria-pressed="topic === t.id" @click="topic = t.id">{{ t.label }} <span>{{ counts[t.id] }}</span></button>
    </div>
    <p class="library-count" role="status" aria-live="polite">{{ videos.length }} {{ videos.length === 1 ? 'video' : 'videos' }}{{ topic !== 'all' ? ` in ${labels[topic]}` : '' }}{{ query.trim() ? ` matching “${query.trim()}”` : '' }}</p>
    <div v-if="videos.length" class="library-grid">
      <article v-for="video in videos" :id="video.id" :key="video.id" class="video-card">
        <a class="video-cover" :href="Object.values(video.links)[0]" target="_blank" rel="noopener noreferrer" :aria-label="`Watch ${video.title} (opens in a new tab)`">
          <img v-if="!failedImages.has(video.id)" :src="withBase(`/video-library/${video.image}`)" alt="" width="540" height="960" loading="lazy" decoding="async" @error="imageFailed(video.id)" />
          <span v-else class="video-cover-fallback">{{ video.title }}</span>
          <span class="video-play" aria-hidden="true">▶</span><span class="video-format">SHORT</span><span class="video-duration" :aria-label="`${video.durationSeconds} seconds`">{{ duration(video.durationSeconds) }}</span>
        </a>
        <div class="video-info">
          <div class="video-meta"><span>{{ labels[video.topic] }}</span><time :datetime="video.published">{{ formatDate(video.published) }}</time></div>
          <h2><a :href="Object.values(video.links)[0]" target="_blank" rel="noopener noreferrer">{{ video.title }}</a></h2>
          <p>{{ video.description }}</p>
          <div class="video-platforms" :aria-label="`Watch ${video.title} on`">
            <a v-for="(url, platform) in video.links" :key="platform" :href="url" target="_blank" rel="noopener noreferrer" :aria-label="`Watch ${video.title} on ${platforms[platform]} (opens in a new tab)`">{{ platforms[platform] }} <span aria-hidden="true">↗</span></a>
          </div>
        </div>
      </article>
    </div>
    <div v-else class="library-empty"><h2>No videos match that search.</h2><p>Try another phrase or explore all topics.</p><button type="button" @click="reset">Clear filters</button></div>
    <p class="library-footer">Choose a platform beneath each short to watch it there.</p>
  </section>
</template>

<style scoped>
:global(.video-library-page .VPDoc:not(.has-sidebar) .content), :global(.video-library-page .VPDoc .content-container) { max-width:1100px; }
.video-library { margin:24px 0 48px; }
.featured-talk { display:grid; grid-template-columns:minmax(0,1.2fr) minmax(0,1fr); border:1px solid var(--vp-c-border); background:var(--vp-c-bg-elv); border-radius:8px; overflow:hidden; margin-bottom:36px; }
.featured-cover { display:block; position:relative; background:#211e19; align-self:center; }
.featured-cover img { display:block; width:100%; aspect-ratio:16/9; object-fit:contain; }
.featured-info { padding:28px; align-self:center; }
.featured-info .featured-label { font-family:var(--vp-font-family-mono); font-size:11px; letter-spacing:.08em; color:var(--vp-c-text-2); margin:0 0 12px; }
.featured-label span { padding:0 8px; }
.featured-info h2 { font-family:'Quincy CF',Georgia,serif; font-weight:400; font-size:clamp(24px,3vw,34px); line-height:1.15; margin:0 0 14px; padding:0; border:0; }
.featured-info h2 a { text-decoration:none; color:var(--vp-c-text-1); }
.featured-info p { font-size:14px; line-height:1.55; color:var(--vp-c-text-2); margin:0 0 20px; }
.featured-links { display:flex; flex-wrap:wrap; gap:10px 20px; font-size:13px; font-weight:600; }
@media(max-width:700px) { .featured-talk { grid-template-columns:minmax(0,1fr); } .featured-info { padding:22px; } }
.library-intro { max-width:720px; margin-bottom:32px; }
.library-stat { display:inline-flex; flex-wrap:wrap; gap:12px; font-size:13px; margin-top:10px; color:var(--vp-c-text-2); }
.library-controls { display:flex; align-items:flex-end; gap:16px; margin:28px 0 18px; }
.library-controls label { display:flex; flex-direction:column; gap:8px; font-size:13px; font-weight:600; }
.library-search { flex:1; }
.library-controls input,.library-controls select { background:var(--vp-c-bg-elv); color:var(--vp-c-text-1); border:1px solid var(--vp-c-border); border-radius:6px; padding:12px 14px; font:inherit; font-size:15px; min-height:48px; }
.library-controls input { width:100%; }
.library-controls select { padding-right:30px; appearance:auto; }
input:focus-visible,select:focus-visible,button:focus-visible,a:focus-visible { outline:3px solid var(--vp-c-brand-2); outline-offset:4px; }
.library-topics { display:flex; flex-wrap:wrap; gap:8px; }
.library-topics button,.library-empty button { border:1px solid var(--vp-c-border); border-radius:6px; padding:9px 12px; font-size:13px; line-height:1.5; color:var(--vp-c-text-1); cursor:pointer; }
.library-topics button[aria-pressed=true] { background:var(--vp-c-text-1); color:var(--vp-c-bg); border-color:var(--vp-c-text-1); }
.library-topics button:hover { border-color:var(--vp-c-text-1); }
.library-topics button span { opacity:.7; font-size:11px; margin-left:4px; }
.library-count { font-size:13px; color:var(--vp-c-text-2); margin:20px 0 16px; }
.library-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:24px; }
.video-card { border:1px solid var(--vp-c-border); border-radius:8px; overflow:hidden; background:var(--vp-c-bg-elv); display:flex; flex-direction:column; min-width:0; scroll-margin-top:100px; }
.video-cover { position:relative; display:flex; justify-content:center; align-items:center; background:#211e19; overflow:hidden; aspect-ratio:4/5; text-decoration:none; }
.video-cover img { display:block; width:100%; height:100%; object-fit:contain; }
.video-play { position:absolute; bottom:14px; right:14px; background:#faf3df; color:#22150d; border-radius:50%; width:38px; height:38px; display:grid; place-items:center; font-size:14px; padding-left:3px; box-shadow:0 2px 12px #0005; }
.video-cover:hover .video-play { background:#ffff8b; }
.video-format { position:absolute; left:12px; top:12px; font-size:10px; letter-spacing:.1em; color:#fff; background:#17120edb; padding:3px 7px; border-radius:3px; }
.video-duration { position:absolute; bottom:16px; left:12px; color:#fff; background:#17120edb; border-radius:3px; padding:2px 7px; font-size:12px; font-family:var(--vp-font-family-mono); }
.video-cover-fallback { color:#faf3df; font-family:Georgia,serif; font-size:27px; line-height:1.3; padding:28px; }
.video-info { padding:18px; display:flex; flex-direction:column; flex:1; }
.video-meta { display:flex; flex-wrap:wrap; justify-content:space-between; gap:4px 10px; color:var(--vp-c-text-2); font-size:11px; line-height:1.4; }
.video-info h2 { font-size:19px; line-height:1.3; letter-spacing:-.02em; border:0; margin:12px 0 8px; padding:0; }
.video-info h2 a { color:var(--vp-c-text-1); text-decoration:none; }
.video-info h2 a:hover { text-decoration:underline; }
.video-info p { color:var(--vp-c-text-2); font-size:14px; line-height:1.55; margin:0 0 22px; }
.video-platforms { display:flex; flex-wrap:wrap; gap:10px 16px; margin-top:auto; }
.video-platforms a { font-size:13px; font-weight:600; text-decoration:underline; text-underline-offset:3px; }
.library-empty { padding:40px 24px; border:1px dashed var(--vp-c-border); border-radius:8px; text-align:center; }
.library-empty h2 { font-size:22px; margin:0; padding:0; border:0; }
.library-footer { margin-top:28px; font-size:13px; color:var(--vp-c-text-2); }
@media(max-width:1100px) { .library-grid { grid-template-columns:repeat(2,minmax(0,1fr)); } }
@media(max-width:600px) { .library-controls { flex-direction:column; align-items:stretch; } .library-grid { grid-template-columns:minmax(0,1fr); gap:20px; } .video-cover { max-height:400px; aspect-ratio:4/5; } .video-meta { font-size:12px; } .video-info { padding:20px; } .video-info h2 { font-size:22px; } }
</style>
