<script setup>
import { computed, ref } from "vue";
import catalog from "../../../../data/harness-references.json";
const scope = ref("main");
const query = ref("");
const topic = ref("");
const counts = { main: catalog.entries.filter(e => e.scope === "main").length, additional: catalog.entries.filter(e => e.scope === "additional").length };
const filtered = computed(() => catalog.entries.filter(e =>
  (scope.value === "all" || e.scope === scope.value) &&
  (!topic.value || e.topic === topic.value) &&
  (!query.value.trim() || [e.title, e.context, e.kind, e.url, catalog.topics.find(t => t.id === e.topic)?.label].join(" ").toLowerCase().includes(query.value.trim().toLowerCase()))
));
const groups = computed(() => catalog.topics.map(t => ({ ...t, entries: filtered.value.filter(e => e.topic === t.id) })).filter(t => t.entries.length));
</script>

<template>
  <div class="reference-library">
    <p class="reference-intro">Explore the papers, engineering posts, code, and lectures linked in <em>{{ catalog.deckTitle }}</em>, plus sources from its backup material.</p>
    <div class="reference-note"><strong>Current talk or further reading?</strong> The current-talk view follows the {{ catalog.slideCount }}-slide working deck as of October 25, 2026. Further reading collects sources from backup and earlier slides. This records where a source appears, not whether it was presented at an event.</div>
    <div class="reference-scopes" role="group" aria-label="Reference collection">
      <button v-for="option in [{ id: 'main', label: 'Current talk', count: counts.main }, { id: 'additional', label: 'Further reading', count: counts.additional }, { id: 'all', label: 'All sources', count: catalog.entries.length }]" :key="option.id" :aria-pressed="scope === option.id" @click="scope = option.id">{{ option.label }} <span>{{ option.count }}</span></button>
    </div>
    <div class="reference-filters">
      <div><label for="reference-search">Search sources</label><input id="reference-search" v-model="query" type="search" placeholder="Title, topic, author, or domain" /></div>
      <div><label for="reference-topic">Topic</label><select id="reference-topic" v-model="topic"><option value="">All topics</option><option v-for="t in catalog.topics" :key="t.id" :value="t.id">{{ t.label }}</option></select></div>
    </div>
    <p class="reference-results" aria-live="polite">{{ filtered.length }} {{ filtered.length === 1 ? 'source' : 'sources' }}</p>
    <p v-if="!filtered.length">No sources match. Try another topic or search term.</p>
    <section v-for="group in groups" :key="group.id" class="reference-group" :aria-labelledby="`topic-${group.id}`">
      <h2 :id="`topic-${group.id}`">{{ group.label }} <span>{{ group.entries.length }}</span></h2>
      <article v-for="entry in group.entries" :key="entry.id" :id="`ref-${entry.id}`" class="reference-entry">
        <div class="reference-kind">{{ entry.kind }} <span v-if="scope === 'all'"> / {{ entry.scope === 'main' ? 'Current talk' : 'Further reading' }}</span></div>
        <h3><a :href="entry.url" target="_blank" rel="noopener noreferrer">{{ entry.title }} <span aria-hidden="true">↗</span></a></h3>
        <p class="reference-context">{{ entry.scope === 'main' ? 'Talk topic' : 'Related slide' }}: {{ entry.context }}</p>
        <p v-if="entry.mainSlides.length" class="reference-slides">Current deck: {{ entry.mainSlides.map(s => `slide ${s.number}`).join(', ') }}</p>
        <p v-if="entry.citationNote" class="reference-caution">Citation note: {{ entry.citationNote }}</p>
        <details><summary>Source details</summary>
          <p v-if="entry.correction">{{ entry.correction }}</p>
          <ul v-if="entry.mainSlides.length"><li v-for="s in entry.mainSlides" :key="s.number">Current deck, slide {{ s.number }}: {{ s.title }}</li></ul>
          <ul v-if="entry.backupSlides.length"><li v-for="(s, i) in entry.backupSlides" :key="i">{{ s.collection }}{{ s.page ? `, slide ${s.page}` : '' }}: {{ s.title }}</li></ul>
          <p v-if="entry.locators.some(url => url !== entry.url)">Slide links and specific versions:</p>
          <ul v-if="entry.locators.some(url => url !== entry.url)"><li v-for="url in entry.locators.filter(url => url !== entry.url)" :key="url"><a :href="url" target="_blank" rel="noopener noreferrer">{{ url }}</a></li></ul>
        </details>
      </article>
    </section>
    <p class="reference-footnote">This library collects linked citations. Local experiments and slides without external links are not separate references. Sources shared by the talk and backup slides appear once, under Current talk. Slide numbers refer to this snapshot and may change as the deck evolves.</p>
  </div>
</template>

<style scoped>
.reference-intro { font-size: 1.18rem; line-height: 1.7; max-width: 850px; }
.reference-note { padding: 20px 24px; border-left: 3px solid var(--vp-c-brand-1); border-radius: 0 10px 10px 0; background: var(--vp-c-bg-soft); line-height: 1.7; }
.reference-note strong { display: block; margin-bottom: 4px; }
.reference-scopes { display: flex; flex-wrap: wrap; gap: 10px; margin: 28px 0 22px; }
.reference-scopes button { padding: 10px 16px; border: 1px solid var(--vp-c-divider); border-radius: 8px; font-weight: 600; }
.reference-scopes button[aria-pressed="true"] { border-color: var(--vp-c-brand-1); background: var(--vp-c-brand-soft); color: var(--vp-c-brand-1); }
.reference-scopes span { margin-left: 7px; font-size: .85em; opacity: .8; }
.reference-filters { display: grid; grid-template-columns: 1.4fr 1fr; gap: 18px; }
.reference-filters label { display: block; margin-bottom: 7px; font-size: .9rem; font-weight: 600; }
.reference-filters input, .reference-filters select { width: 100%; padding: 11px 12px; border: 1px solid var(--vp-c-divider); border-radius: 7px; background: var(--vp-c-bg); color: var(--vp-c-text-1); font: inherit; }
.reference-results, .reference-footnote { color: var(--vp-c-text-2); font-size: .9rem; }
.reference-group h2 { display: flex; gap: 12px; align-items: baseline; }
.reference-group h2 span { color: var(--vp-c-text-3); font-size: 1rem; font-weight: 400; }
.reference-entry { padding: 21px 0; border-bottom: 1px solid var(--vp-c-divider); scroll-margin-top: 90px; }
.reference-kind { color: var(--vp-c-text-2); font-size: .78rem; letter-spacing: .04em; text-transform: uppercase; }
.reference-entry h3 { margin: 5px 0 7px; line-height: 1.45; font-size: 1.12rem; overflow-wrap: anywhere; }
.reference-entry h3 a { text-decoration: none; }
.reference-entry h3 span { font-size: .8em; }
.reference-entry p { margin: 5px 0; }
.reference-context { line-height: 1.6; }
.reference-slides { font-size: .84rem; color: var(--vp-c-text-2); }
.reference-entry details { margin-top: 9px; color: var(--vp-c-text-2); font-size: .85rem; }
.reference-entry summary { cursor: pointer; }
.reference-entry details a { overflow-wrap: anywhere; }
.reference-caution { padding: 9px 12px; border-radius: 6px; background: var(--vp-c-warning-soft); font-size: .9rem; }
.reference-footnote { margin-top: 36px; }
@media(max-width: 600px) { .reference-filters { grid-template-columns: 1fr; } .reference-scopes { gap: 7px; } .reference-scopes button { padding: 9px 11px; } }
</style>
