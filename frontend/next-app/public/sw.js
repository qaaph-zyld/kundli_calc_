/**
 * Service Worker for Kundli Calculator PWA
 * Enables offline functionality and caching
 */

const CACHE_NAME = 'kundli-calc-v3';
const STATIC_CACHE = 'kundli-static-v3';
const DYNAMIC_CACHE = 'kundli-dynamic-v3';

// Static assets to cache immediately
const STATIC_ASSETS = [
  '/',
  '/offline',
  '/manifest.json',
  '/_next/static/css/app.css',
];

// API endpoints to cache
const API_CACHE_PATTERNS = [
  /\/api\/v1\/health/,
  /\/api\/v1\/yogas\/categories/,
  /\/api\/v1\/compatibility\/koota-info/,
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
  console.log('[SW] Installing service worker...');
  
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => {
        console.log('[SW] Caching static assets');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => self.skipWaiting())
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating service worker...');
  
  event.waitUntil(
    caches.keys()
      .then((keys) => {
        return Promise.all(
          keys
            .filter((key) => key !== CACHE_NAME && key !== STATIC_CACHE && key !== DYNAMIC_CACHE)
            .map((key) => {
              console.log('[SW] Deleting old cache:', key);
              return caches.delete(key);
            })
        );
      })
      .then(() => self.clients.claim())
  );
});

// Fetch event - serve from cache or network
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }
  
  // Skip Chrome extensions and other non-http(s) requests
  if (!url.protocol.startsWith('http')) {
    return;
  }
  
  // API requests - network first, then cache
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(networkFirstStrategy(request));
    return;
  }
  
  // Static assets - cache first
  if (isStaticAsset(url.pathname)) {
    event.respondWith(cacheFirstStrategy(request));
    return;
  }
  
  // Pages - stale while revalidate
  event.respondWith(staleWhileRevalidate(request));
});

// Cache first strategy
async function cacheFirstStrategy(request) {
  const cached = await caches.match(request);
  if (cached) {
    return cached;
  }
  
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(STATIC_CACHE);
      cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    return caches.match('/offline');
  }
}

// Network first strategy
async function networkFirstStrategy(request) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      // Cache successful API responses
      if (shouldCacheAPI(request.url)) {
        const cache = await caches.open(DYNAMIC_CACHE);
        cache.put(request, response.clone());
      }
    }
    return response;
  } catch (error) {
    // Try to return cached response
    const cached = await caches.match(request);
    if (cached) {
      return cached;
    }
    
    // Return offline fallback for API
    return new Response(
      JSON.stringify({ 
        error: 'Offline', 
        message: 'You are currently offline. Please check your connection.',
        offline: true 
      }),
      { 
        status: 503,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
}

// Stale while revalidate strategy
async function staleWhileRevalidate(request) {
  const cached = await caches.match(request);
  
  const networkPromise = fetch(request)
    .then((response) => {
      if (response.ok) {
        const cache = caches.open(DYNAMIC_CACHE);
        cache.then((c) => c.put(request, response.clone()));
      }
      return response;
    })
    .catch(() => null);
  
  return cached || networkPromise || caches.match('/offline');
}

// Helper: Check if URL is a static asset
function isStaticAsset(pathname) {
  const staticExtensions = ['.js', '.css', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.woff', '.woff2'];
  return staticExtensions.some((ext) => pathname.endsWith(ext)) || pathname.startsWith('/_next/static/');
}

// Helper: Check if API response should be cached
function shouldCacheAPI(url) {
  return API_CACHE_PATTERNS.some((pattern) => pattern.test(url));
}

// Background sync for calculations
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-calculations') {
    event.waitUntil(syncCalculations());
  }
});

async function syncCalculations() {
  // Get pending calculations from IndexedDB
  // This would sync any calculations made while offline
  console.log('[SW] Syncing pending calculations...');
}

// Push notifications
self.addEventListener('push', (event) => {
  if (event.data) {
    const data = event.data.json();
    
    const options = {
      body: data.body || 'New update available',
      icon: '/icons/icon-192x192.png',
      badge: '/icons/badge-72x72.png',
      vibrate: [100, 50, 100],
      data: {
        url: data.url || '/'
      }
    };
    
    event.waitUntil(
      self.registration.showNotification(data.title || 'Kundli Calculator', options)
    );
  }
});

// Notification click handler
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  
  event.waitUntil(
    clients.openWindow(event.notification.data.url)
  );
});

console.log('[SW] Service worker loaded');
