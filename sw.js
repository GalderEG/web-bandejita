const CACHE_NAME = 'bandejita-cache-v1';

// Aquí listamos los archivos estáticos que queremos guardar en el teléfono del usuario
const urlsToCache = [
  '/',
  '/index.html',
  '/manifest.json',
  'https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&display=swap',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
  'https://raw.githubusercontent.com/GalderEG/web-bandejita/main/Imagotipo.png',
  'https://raw.githubusercontent.com/GalderEG/web-bandejita/2c9e405ea2773f4f431c75880bb058fdbb1eb9ed/Encabezado%20bandejita.jpg'
];

// 1. INSTALACIÓN: Guardamos los archivos en caché la primera vez que entran
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Archivos cacheados exitosamente');
        // Usamos addAll pero silenciamos errores si algún recurso externo falla
        return Promise.all(
          urlsToCache.map(url => {
            return cache.add(url).catch(err => console.log('Fallo al cachear: ', url, err));
          })
        );
      })
  );
  self.skipWaiting();
});

// 2. ACTIVACIÓN: Limpiamos cachés viejos si actualizas la versión (v2, v3...)
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Borrando caché antiguo:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// 3. INTERCEPCIÓN (FETCH): Cómo responder cuando la app pide datos
self.addEventListener('fetch', event => {
  const requestUrl = new URL(event.request.url);

  // EXCEPCIÓN: NUNCA cachear el CSV de Google Sheets para garantizar que el menú esté siempre vivo
  if (requestUrl.hostname === 'docs.google.com' || requestUrl.href.includes('output=csv')) {
    event.respondWith(fetch(event.request));
    return;
  }

  // PARA EL RESTO DE LA WEB (Diseño, fuentes, imágenes):
  // Estrategia: Network First, fallback to Cache
  // Intenta buscar en internet primero, si falla (sin conexión), muestra lo guardado.
  event.respondWith(
    fetch(event.request)
      .then(response => {
        // Si la red funciona, actualizamos el caché silenciosamente
        if (response && response.status === 200 && response.type === 'basic') {
          const responseToCache = response.clone();
          caches.open(CACHE_NAME)
            .then(cache => {
              cache.put(event.request, responseToCache);
            });
        }
        return response;
      })
      .catch(() => {
        // Si no hay red, buscamos en el caché
        return caches.match(event.request);
      })
  );
});
