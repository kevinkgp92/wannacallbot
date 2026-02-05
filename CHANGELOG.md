# ♈ WANNA CALL? - CHANGELOG

---

## 🔥 [2.2.15] - 2026-02-05 (BLACK OPS NETWORK OVERHAUL)

### 🇪🇸 ESPAÑOL
- **SOCKS SUPPORT**: El motor de red ahora soporta SOCKS4 y SOCKS5, multiplicando por 10 la capacidad de encontrar proxys españoles.
- **ALIVE CHECK 2.0**: Implementada verificación multi-protocolo y timeouts agresivos de 25s para redes móviles.
- **SANITY CLEANUP**: Eliminada la contaminación de listas globales en la Fase 1 para evitar falsos positivos y acelerar el arranque.

### 🇺🇸 ENGLISH
- **SOCKS SUPPORT**: The network engine now supports SOCKS4 and SOCKS5, increasing Spanish proxy yield by 10x.
- **ALIVE CHECK 2.0**: Implemented multi-protocol verification and 25s timeouts for mobile networks.
- **SANITY CLEANUP**: Removed global list pollution from Phase 1 to avoid false positives and speed up startup.

---

## 🔥 [2.2.14] - 2026-02-05 (EXTREME PROXY RECOVERY)

### 🇪🇸 ESPAÑOL
- **DEEP SCRAPING**: Implementado motor de parsing HTML para extraer proxys españoles de `ProxyNova` y `ProxyList.org` directamente.
- **RESILIENCIA ++**: Aumentado el timeout de verificación a **25 segundos** para capturar redes residenciales y móviles lentas pero funcionales.
- **GEO-FALLBACK**: Añadida `ipapi.co` como tercera vía de verificación de geolocalización.

### 🇺🇸 ENGLISH
- **DEEP SCRAPING**: Implemented HTML parsing engine to extract Spanish proxies from `ProxyNova` and `ProxyList.org` directly.
- **RESILIENCE ++**: Increased verification timeout to **25 seconds** to capture slow but functional residential/mobile networks.
- **GEO-FALLBACK**: Added `ipapi.co` as a third geolocation verification fallback.

---

## 🔥 [2.2.13] - 2026-02-05 (REBRANDING & ASSET SYNC)

### 🇪🇸 ESPAÑOL
- **REBRANDING**: Renombrado el logo principal a `wannacallbot_logo.png`.
- **LIMPIEZA**: Eliminado rastro total de referencias antiguas a "carnerosbot".

### 🇺🇸 ENGLISH
- **REBRANDING**: Renamed main logo to `wannacallbot_logo.png`.
- **CLEANUP**: Removed all old references to "carnerosbot".

---

## 🔥 [2.2.12] - 2026-02-05 (NUCLEAR NETWORK OPTIMIZATION)

### 🇪🇸 ESPAÑOL
#### OPTIMIZACIÓN DE RED Y PROXYS
- **ES SOURCES ++**: Inyectadas 15+ nuevas fuentes diarias de España para eliminar la dependencia de búsquedas globales lentas.
- **GEO-CACHE INTELIGENTE**: Implementada caché local de geolocalización para evitar bloqueos por exceso de peticiones (Rate Limit) y acelerar la verificación.
- **ALIVE CHECK 2.0**: Optimizado para la latencia de servicios residenciales españoles, asegurando conexiones estables en OSINT.
- **ESCUDO DE ROTACIÓN**: Añadido límite de 5 rotaciones por sesión para prevenir bucles infinitos en el motor de búsqueda.

### 🇺🇸 ENGLISH
#### NETWORK & PROXY OPTIMIZATION
- **ES SOURCES ++**: Injected 15+ new daily Spanish sources to eliminate dependency on slow global searches.
- **SMART GEO-CACHE**: Implemented local geolocation cache to prevent Rate Limit blocks and accelerate verification.
- **ALIVE CHECK 2.0**: Optimized for high-latency Spanish residential services, ensuring stable OSINT connections.
- **ROTATION GUARD**: Added a limit of 5 rotations per session to prevent infinite loops in the search engine.

---

## 🔥 [2.2.11] - 2026-02-05 (NUCLEAR CLEANUP & UI REFINEMENT)

### 🇪🇸 ESPAÑOL
#### REFINAMIENTO Y LIMPIEZA
- **NUCLEAR CLEANUP**: Eliminados más de 12 archivos obsoletos, logs y restos de versiones antiguas para un repositorio "Grial" impecable.
- **RESTABLECIMIENTO GUI**: Revertido el título de la ventana y el texto de los botones a su base profesional estable.
- **MOTORES PROXY ES++**: Añadidas 12+ fuentes adicionales de proxys españoles de alta intensidad para maximizar el éxito en OSINT.
- **FIX: ALIVE CHECK**: Optimizada la lógica de verificación para detectar proxys españoles reales con mayor precisión.

### 🇺🇸 ENGLISH
#### REFINEMENT & CLEANUP
- **NUCLEAR CLEANUP**: Removed over 12 obsolete files, logs, and leftovers from old versions for a pristine "Grial" repository.
- **GUI RESTORATION**: Reverted window titles and button text back to their stable professional baseline.
- **ES++ PROXY ENGINES**: Added 12+ additional high-intensity Spanish proxy sources to maximize OSINT success.
- **FIX: ALIVE CHECK**: Optimized verification logic to detect real Spanish proxies with higher precision.

---

## 🔥 [2.2.10] - 2026-02-05 (PROXY ENGINE UPGRADE)

### 🇪🇸 ESPAÑOL
#### MEJORAS EN EL MOTOR DE PROXYS
- **CACHÉ PERSISTENTE**: Implementado `core/proxies_cache.json` para recordar proxys funcionales entre sesiones.
- **SOPORTE SOCKS EXTREME**: Añadido soporte nativo para proxys SOCKS4 y SOCKS5, optimizando la tasa de éxito en España.
- **ALIVE CHECK 2.0**: Nueva lógica de verificación multi-objetivo (Google + Cloudflare) para máxima fiabilidad.
- **AUTO-BLACKLIST**: El sistema ahora elimina dinámicamente los proxys caídos de la caché.

### 🇺🇸 ENGLISH
#### PROXY ENGINE UPGRADE
- **PERSISTENT CACHE**: Implemented `core/proxies_cache.json` to remember working proxies across sessions.
- **EXTREME SOCKS SUPPORT**: Added native support for SOCKS4 and SOCKS5 proxies, optimizing success rate in Spain.
- **ALIVE CHECK 2.0**: New multi-target verification logic (Google + Cloudflare) for maximum reliability.
- **AUTO-BLACKLIST**: The system now dynamically removes dead proxies from the cache.

---

## 🔥 [2.2.9] - 2026-02-05 (CRITICAL PROXY FIX)

### 🇪🇸 ESPAÑOL
#### REPARACIÓN CRÍTICA
- **FIX: NameError 'urls'**: Corregido un error de sangría en `core/proxy_scraper.py` que impedía el inicio de los navegadores.
- **SINCRO TOTAL v2.2.9**: Versión unificada para asegurar que todos los usuarios reciban el parche de navegación.

---

## 🔥 [2.2.8] - 2026-02-05 (STABILITY & SYNC RELEASE)
- **THREAD-SAFE UPDATER**: Corregido el error de "main thread" mediante una cola de procesos (Queue).
- **PROXIES ES++**: Añadidas 10+ fuentes de proxys españoles de alta calidad.
- **PORTABLE MODE**: El ejecutable ahora es un único archivo (One-File) para máxima portabilidad.

---

### 🇺🇸 ENGLISH
#### CRITICAL FIX
- **FIX: NameError 'urls'**: Corrected an indentation error in `core/proxy_scraper.py` that prevented browsers from starting.
- **TOTAL v2.2.9 SYNC**: Unified version to ensure all users receive the navigation patch.

---
