if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/service-worker.js')
        .then((registration) => {
          console.log('Service Worker registered with scope:', registration.scope);
        })
        .catch((error) => {
          console.log('Service Worker registration failed:', error);
        });
    });

    self.addEventListener('fetch', (event) => {
        event.respondWith(
          caches.match(event.request)
            .then((cachedResponse) => {
              // If no cached response, serve the offline page
              return cachedResponse || caches.match('/base_not.html');
            })
        );
      });
      
  }


  