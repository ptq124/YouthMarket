var staticCacheName = 'djangopwa-v1';
var filesToCache = [
	'http://127.0.0.1:8000/media/icons/icon-72x72.png',
    'http://127.0.0.1:8000/media/icons/icon-96x96.png',
    'http://127.0.0.1:8000/media/icons/icon-128x128.png',
    'http://127.0.0.1:8000/media/icons/icon-144x144.png',
    'http://127.0.0.1:8000/media/icons/icon-152x152.png',
    'http://127.0.0.1:8000/media/icons/icon-192x192.png',
    'http://127.0.0.1:8000/media/icons/icon-384x384.png',
    'http://127.0.0.1:8000/media/icons/icon-512x512.png',
    'http://127.0.0.1:8000/media/icons/icon_.PNG'
    // 'http://127.0.0.1:8000/media/icons/splash-640x1136.png',
    // 'http://127.0.0.1:8000/media/icons/splash-750x1334.png',
    // 'http://127.0.0.1:8000/media/icons/splash-828x1792.png',
    // 'http://127.0.0.1:8000/media/icons/splash-1125x2436.png',
    // 'http://127.0.0.1:8000/media/icons/splash-1242x2208.png',
    // 'http://127.0.0.1:8000/media/icons/splash-1242x2688.png',
    // 'http://127.0.0.1:8000/media/icons/splash-1536x2048.png',
    // 'http://127.0.0.1:8000/media/icons/splash-1668x2224.png',
    // 'http://127.0.0.1:8000/media/icons/splash-1668x2388.png',
    // 'http://127.0.0.1:8000/media/icons/splash-2048x2732.png'
];
self.addEventListener('install', function(event) {
event.waitUntil(
	caches.open(staticCacheName).then(function(cache) {
		return cache.addAll(
			filesToCache
		);
	})
);
});

self.addEventListener('fetch', function(event) {
var requestUrl = new URL(event.request.url);
	if (requestUrl.origin === location.origin) {
	if ((requestUrl.pathname === '/')) {
		event.respondWith(caches.match(''));
		return;
	}
	}
	event.respondWith(
	caches.match(event.request).then(function(response) {
		return response || fetch(event.request);
	})
	);
});
