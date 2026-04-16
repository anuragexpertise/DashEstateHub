// Service Worker for EstateHub
// Handles push notifications and offline functionality

const CACHE_NAME = 'estatehub-v1';
const urlsToCache = [
  '/',
  '/assets/glass.css',
  '/offline.html'
];

// Install event - cache resources
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
      .then(() => self.skipWaiting())
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', event => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') {
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Return cached response if available
        if (response) {
          return response;
        }

        return fetch(event.request).then(response => {
          // Clone response before caching
          const responseToCache = response.clone();
          
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseToCache);
          });

          return response;
        });
      })
      .catch(() => {
        // Return offline page on network error
        return caches.match('/offline.html');
      })
  );
});

// Push notification event
self.addEventListener('push', event => {
  console.log('Push notification received');
  
  const data = event.data ? event.data.json() : {
    title: 'EstateHub',
    body: 'You have a new notification'
  };

  const options = {
    body: data.body,
    icon: '/assets/RRARWA LOGO.PNG',
    badge: '/assets/RRARWA LOGO.PNG',
    data: data.data || {}
  };

  event.waitUntil(
    self.registration.showNotification(data.title, options)
  );
});

// Notification click event
self.addEventListener('notificationclick', event => {
  console.log('Notification clicked');
  
  event.notification.close();

  // Handle the notification click
  // For login approval, trigger biometric verification
  if (event.notification.data.type === 'login_approval') {
    event.waitUntil(
      clients.matchAll({ type: 'window' }).then(windowClients => {
        // Send message to all windows
        windowClients.forEach(client => {
          client.postMessage({
            type: 'APPROVE_LOGIN',
            data: event.notification.data
          });
        });
      })
    );
  }

  // Navigate to the app
  event.waitUntil(
    clients.matchAll({ type: 'window' }).then(windowClients => {
      if (windowClients.length > 0) {
        return windowClients[0].focus();
      }
      return clients.openWindow('/');
    })
  );
});

// Notification close event (optional)
self.addEventListener('notificationclose', event => {
  console.log('Notification closed');
});
