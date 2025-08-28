// Service worker untuk mode online (tidak cache)
self.addEventListener("install", event => {
  // Langsung activate tanpa simpan cache
  self.skipWaiting();
});

self.addEventListener("activate", event => {
  clients.claim();
});

self.addEventListener("fetch", event => {
  // Semua request langsung ke network
  event.respondWith(fetch(event.request));
});
