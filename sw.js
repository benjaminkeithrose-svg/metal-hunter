/* Metal Hunter service worker.
   Site files and data: network first, so every merge to main shows up on the next open; the cache is only the offline fallback.
   Google Fonts: cache first, they never change. */
const CACHE = "mh-v2";
const SHELL = ["./", "index.html", "data/events.json", "data/bands.json", "manifest.webmanifest",
  "icons/icon-192.png", "icons/icon-512.png", "icons/apple-touch-icon.png"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).catch(() => {}));
  self.skipWaiting();
});

self.addEventListener("activate", e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);

  if (url.hostname === "fonts.googleapis.com" || url.hostname === "fonts.gstatic.com") {
    e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(res => {
      const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); return res;
    })));
    return;
  }
  if (url.origin !== location.origin) return;

  // Store pages without their query string so ?look=xerox shares the cached copy.
  const key = req.mode === "navigate" ? new Request(url.origin + url.pathname) : req;
  e.respondWith(fetch(req.url, { cache: "no-cache" }).then(res => {
    if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(key, copy)); }
    return res;
  }).catch(() => caches.match(key, { ignoreSearch: true })
    .then(hit => hit || (req.mode === "navigate" ? caches.match("./") : undefined))));
});
