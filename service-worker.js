self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open('my-cache').then((cache) => {
      return cache.addAll([
        '/',
        '/index.html',
        '/offline.html',  // Fallback page
        '/static/css/style.css',
        '/static/js/app.js',
        '/static/images/logo.png'
      ]);
    })
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((cachedResponse) => {
        // If no cached response, serve the offline page
        return cachedResponse || caches.match('/offline.html');
      })
  );
});
