import { readFile, writeFile, access } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import assert from 'node:assert/strict';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const source = resolve(root, 'data/harness-videos.json');
const catalog = JSON.parse(await readFile(source, 'utf8'));
const args = process.argv.slice(2);
const check = args.includes('--check');
const readmeArg = args.indexOf('--readme');
if (readmeArg !== -1) assert(args[readmeArg + 1] && !args[readmeArg + 1].startsWith('--'), '--readme needs a path');
const readmePath = readmeArg === -1 ? null : resolve(args[readmeArg + 1]);
const domains = { instagram: 'www.instagram.com', youtube: 'www.youtube.com', tiktok: 'www.tiktok.com' };
const names = { instagram: 'Instagram', youtube: 'YouTube', tiktok: 'TikTok' };
const topicIds = new Set(catalog.topics.map(t => t.id));
assert.equal(topicIds.size, catalog.topics.length, 'Topic IDs must be unique');
const seen = new Set();
for (const video of [...catalog.videos, ...(catalog.featuredTalk ? [catalog.featuredTalk] : [])]) {
  assert(/^[A-Za-z0-9_-]+$/.test(video.id) && !seen.has(video.id), `Invalid or duplicate ID: ${video.id}`);
  seen.add(video.id);
  if (video !== catalog.featuredTalk) assert(topicIds.has(video.topic), `Unknown topic for ${video.id}`);
  assert(video.title?.trim() && video.description?.trim(), `Missing copy for ${video.id}`);
  assert(Number.isInteger(video.durationSeconds) && video.durationSeconds > 0, `Expected a measured duration for ${video.id}`);
  if (video !== catalog.featuredTalk) assert(video.durationSeconds <= 180, `Expected a short duration for ${video.id}`);
  assert(/^\d{4}-\d{2}-\d{2}$/.test(video.published) && !Number.isNaN(Date.parse(video.published)), `Invalid date: ${video.id}`);
  assert(/^covers\/[A-Za-z0-9_-]+\.jpg$/.test(video.image), `Invalid cover path: ${video.id}`);
  await access(resolve(root, 'docs/public/video-library', video.image));
  assert(Object.keys(video.links).length, `No watch link for ${video.id}`);
  for (const [platform, link] of Object.entries(video.links)) {
    const url = new URL(link);
    assert(domains[platform] === url.hostname && url.protocol === 'https:' && !url.username && !url.password, `Invalid ${platform} link for ${video.id}`);
    const patterns = { instagram: /^\/reel\/[^/]+\/?$/, youtube: /^\/(shorts\/[^/]+\/?|watch)$/, tiktok: /^\/@[^/]+\/video\/\d+\/?$/ };
    assert(patterns[platform].test(url.pathname), `Expected a video link for ${video.id}`);
    if (platform === 'youtube' && url.pathname === '/watch') assert(url.searchParams.get('v'), `Missing YouTube ID for ${video.id}`);
  }
}

const galleryURL = 'https://rajshah4.github.io/learn-openhands-harness/videos';
const assetURL = 'https://raw.githubusercontent.com/rajshah4/learn-openhands-harness/main/docs/public/video-library/';
const escape = text => String(text).replace(/[&<>"|]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', '|': '&#124;' }[c]));
const start = '<!-- HARNESS-VIDEO-GALLERY:START -->';
const end = '<!-- HARNESS-VIDEO-GALLERY:END -->';
function card(video) {
  const title = escape(video.title);
  const watch = Object.values(video.links)[0];
  const links = Object.entries(video.links).map(([platform, url]) => `<a href="${escape(url)}">${names[platform]}</a>`).join(' · ');
  const duration = `${Math.floor(video.durationSeconds / 60)}:${String(video.durationSeconds % 60).padStart(2, '0')}`;
  return `<a href="${escape(watch)}"><img src="${assetURL}${video.image}" width="150" alt="Watch ${title}"></a><br><strong>${title}</strong> (${duration})<br>${escape(video.description)}<br>${links}`;
}
const lines = [start, '## Video gallery', ''];
if (catalog.featuredTalk) {
  const talk = catalog.featuredTalk;
  const runtime = `${Math.floor(talk.durationSeconds / 60)}:${String(talk.durationSeconds % 60).padStart(2, '0')}`;
  const month = new Intl.DateTimeFormat('en-US', { month: 'long', year: 'numeric', timeZone: 'UTC' }).format(new Date(talk.published + 'T12:00:00Z'));
  lines.push('### Featured full talk', '', '| Featured full talk |', '| --- |', `| <a href="${escape(talk.links.youtube)}"><img src="${assetURL}${talk.image}" width="600" alt="Watch ${escape(talk.title)}"></a><br><strong>${escape(talk.title)}</strong> (${runtime}, ${month})<br>${escape(talk.description)}<br><a href="${escape(talk.links.youtube)}">Watch on YouTube</a> · <a href="${escape(talk.resources['Slides and references'])}">Slides and references</a> |`, '');
}
lines.push('### Short videos', '', `Standalone shorts on the decisions around a coding agent. [Browse and search all ${catalog.videos.length} shorts](${galleryURL}) on the Learn Harness Engineering site.`, '');
for (const topic of catalog.topics) {
  const videos = catalog.videos.filter(v => v.topic === topic.id);
  if (!videos.length) continue;
  lines.push(`### ${topic.label}`, '', '| | |', '| --- | --- |');
  for (let i = 0; i < videos.length; i += 2) lines.push(`| ${card(videos[i])} | ${videos[i + 1] ? card(videos[i + 1]) : ''} |`);
  lines.push('');
}
lines.push(end);
const fragment = lines.join('\n');
const outputs = [
  [resolve(root, 'docs/public/video-library/catalog.json'), JSON.stringify(catalog, null, 2) + '\n'],
  [resolve(root, 'data/harness-videos.generated.md'), fragment + '\n'],
];
if (readmePath) {
  const readme = await readFile(readmePath, 'utf8');
  assert.equal(readme.includes(start), readme.includes(end), 'Gallery markers must be paired');
  let updated;
  if (readme.includes(start)) {
    assert.equal(readme.split(start).length, 2, 'Gallery start must be unique');
    assert.equal(readme.split(end).length, 2, 'Gallery end must be unique');
    assert(readme.indexOf(start) < readme.indexOf(end), 'Gallery markers are reversed');
    updated = readme.slice(0, readme.indexOf(start)) + fragment + readme.slice(readme.indexOf(end) + end.length);
  } else {
    const anchor = '\n## Vocabulary';
    assert(readme.includes(anchor), 'Cannot locate README insertion point');
    updated = readme.replace(anchor, `\n${fragment}\n\n---\n${anchor}`);
  }
  outputs.push([readmePath, updated]);
}
for (const [path, content] of outputs) {
  if (check) assert.equal(await readFile(path, 'utf8'), content, `Generated gallery is stale: ${path}`);
  else await writeFile(path, content);
}
console.log(`${check ? 'Checked' : 'Synced'} ${catalog.videos.length} videos, ${catalog.topics.length} topics${readmePath ? ', and repository README' : ''}.`);
