import { readFileSync } from "node:fs";
import assert from "node:assert/strict";
const catalog = JSON.parse(readFileSync(new URL("../data/harness-references.json", import.meta.url), "utf8"));
const ids = new Set(), urls = new Set(), topics = new Set(catalog.topics.map(t => t.id));
for (const entry of catalog.entries) {
  assert(entry.title.trim(), "Reference title is required");
  assert(!ids.has(entry.id), `Duplicate ID: ${entry.id}`);
  assert(!urls.has(entry.url), `Duplicate URL: ${entry.url}`);
  ids.add(entry.id); urls.add(entry.url);
  assert.equal(new URL(entry.url).protocol, "https:");
  assert(topics.has(entry.topic), `Unknown topic: ${entry.topic}`);
  assert.equal(entry.scope, entry.mainSlides.length ? "main" : "additional");
  assert(entry.mainSlides.length || entry.backupSlides.length, "Missing provenance");
  for (const slide of entry.mainSlides) assert(Number.isInteger(slide.number) && slide.number >= 1 && slide.number <= catalog.slideCount, "Invalid slide number");
}
console.log(`Reference catalog valid: ${catalog.entries.length} unique sources, ${catalog.slideCount} slides.`);
