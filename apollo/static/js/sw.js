const STATIC_CACHE = 'static-cache',
    DYNAMIC_CACHE = 'dynamic-cache',
    APP_RESOURCES = [
        '/static/manifest.json',
        '/static/css/index.css',

        '/static/font/material-icons.woff2',
        '/static/font/open-sans-regular-cyrillic.woff2',
        '/static/font/open-sans-medium-cyrillic.woff2',
        '/static/font/open-sans-regular-latin.woff2',
        '/static/font/open-sans-medium-latin.woff2',
        '/static/img/favicon.png',

        '/static/js/lib/compiled.min.js',
        '/static/js/lib/sensor.js',

        '/static/js/widget/currency.js',
        '/static/js/widget/datetime.js',
        '/static/js/widget/indoor-climate.js',
        '/static/js/widget/indoor-climate-report.js',
        '/static/js/widget/weather.js',
        '/static/js/index.js',
    ];


// Cache static resources
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(STATIC_CACHE).then((cache) => {
            return cache.addAll(APP_RESOURCES);
        })
    );
});


// Clean all other caches, except of static
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cache_names) => {
            return Promise.all(
                cache_names.map((cache_name) => {
                    if (cache_name !== STATIC_CACHE) {
                        return caches.delete(cache_name);
                    }
                })
            );
        })
    );
});


// Check all backend calls
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                if (response) {
                    return response;
                }

                return fetch(event.request.clone())
                    .then((response) => {
                        let is_failed = !response || response.status !== 200 || response.type !== 'basic',
                            is_api_call = response.url.indexOf('api') >= 0;

                        // Do not cache failed requests and api calls
                        if (is_failed || is_api_call) {
                            return response;
                        }

                        // Cache app resources
                        caches.open(DYNAMIC_CACHE)
                            .then((cache) => {
                                cache.put(event.request, response.clone());
                            });

                        return response;
                    });
            })
    );
});