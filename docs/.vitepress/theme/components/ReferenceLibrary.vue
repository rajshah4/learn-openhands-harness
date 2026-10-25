<script setup>
import { computed, ref } from "vue";
import catalog from "../../../../data/harness-references.json";
const query = ref("");
const topic = ref("");
const filtered = computed(() => catalog.entries.filter(e =>
  (!topic.value || e.topic === topic.value) &&
  (!query.value.trim() || [e.title, e.url, catalog.topics.find(t => t.id === e.topic)?.label].join(" ").toLowerCase().includes(query.value.trim().toLowerCase()))
));
const groups = computed(() => catalog.topics.map(t => ({ ...t, entries: filtered.value.filter(e => e.topic === t.id) })).filter(t => t.entries.length));
</script>

<template>
  <div class="reference-library">
    <p class="reference-intro">Papers, code, and further reading on harness engineering.</p>
    <div class="reference-filters">
      <div><label for="reference-search">Search sources</label><input id="reference-search" v-model="query" type="search" placeholder="Title, topic, or URL" /></div>
      <div><label for="reference-topic">Topic</label><select id="reference-topic" v-model="topic"><option value="">All topics</option><option v-for="t in catalog.topics" :key="t.id" :value="t.id">{{ t.label }}</option></select></div>
    </div>
    <p class="reference-results" aria-live="polite">{{ filtered.length }} {{ filtered.length === 1 ? 'source' : 'sources' }}</p>
    <p v-if="!filtered.length">No sources match. Try another topic or search term.</p>
    <section v-for="group in groups" :key="group.id" class="reference-group" :aria-labelledby="`topic-${group.id}`">
      <h2 :id="`topic-${group.id}`">{{ group.label }} <span>{{ group.entries.length }}</span></h2>
      <article v-for="entry in group.entries" :key="entry.id" :id="`ref-${entry.id}`" class="reference-entry">
        <h3><a :href="entry.url" target="_blank" rel="noopener noreferrer">{{ entry.title }} <span aria-hidden="true">↗</span></a></h3>
        <a class="reference-url" :href="entry.url" target="_blank" rel="noopener noreferrer">{{ entry.url }}</a>
      </article>
    </section>
  </div>
</template>

<style scoped>
.reference-intro { color: var(--vp-c-text-2); }
.reference-filters { display: grid; grid-template-columns: 1.4fr 1fr; gap: 18px; margin-top: 24px; }
.reference-filters label { display: block; margin-bottom: 7px; font-size: .9rem; font-weight: 600; }
.reference-filters input, .reference-filters select { width: 100%; padding: 9px 12px; border: 1px solid var(--vp-c-divider); border-radius: 7px; background: var(--vp-c-bg); color: var(--vp-c-text-1); font: inherit; }
.reference-results { color: var(--vp-c-text-2); font-size: .85rem; }
.reference-group h2 { display: flex; gap: 12px; align-items: baseline; margin-top: 28px; padding-top: 18px; font-size: 1.15rem; }
.reference-group h2 span { color: var(--vp-c-text-3); font-size: .85rem; font-weight: 400; }
.reference-entry { padding: 10px 0; border-bottom: 1px solid var(--vp-c-divider); scroll-margin-top: 90px; }
.reference-entry h3 { margin: 0; line-height: 1.45; font-size: .98rem; overflow-wrap: anywhere; }
.reference-entry h3 a { text-decoration: none; }
.reference-entry h3 span { font-size: .8em; }
.reference-url { display: block; color: var(--vp-c-text-2); font-size: .78rem; line-height: 1.5; text-decoration: none; overflow-wrap: anywhere; }
@media(max-width: 600px) { .reference-filters { grid-template-columns: 1fr; gap: 12px; } }
</style>
