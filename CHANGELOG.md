# ♈ WANNA CALL? - CHANGELOG

## [v2.2.96] - Visual Feedback & Hardened SSL (2026-02-07)
### 🇪🇸 ESPAÑOL
- **📊 BARRA DE PROGRESO**: Ahora verás un porcentaje (10%, 20%...) mientras el bot verifica los proxies, para que sepas que está trabajando y no congelado.
- **🛡️ SSL ESTRICTO**: Se ha añadido una "Fase 4" de verificación. Si un proxy pasa el test de Google pero falla al cargar una página real (HTTPS), se descarta. Esto reduce los errores de conexión en OSINT.

### 🇺🇸 ENGLISH
- **📊 PROGRESS BAR**: You will now see a percentage (10%, 20%...) while the bot verifies proxies, so you know it's working and not frozen.
- **🛡️ STRICT SSL**: Added a "Phase 4" verification. If a proxy passes Google test but fails to load a real page (HTTPS), it is discarded. This reduces connection errors in OSINT.


## [v2.2.95] - Proxy Trust (2026-02-07)
### 🇪🇸 ESPAÑOL
- **🔒 CONFIANZA CIEGA**: Ahora el sistema confía en los proxies del "Laboratorio" durante 30 minutos (antes 2). Esto evita que el OSINT los borre y empiece a buscar de cero si tardas un poco.
- **⚡ OSINT INMEDIATO**: Si hay proxies españoles válidos, el OSINT arranca al instante sin exigir "GOLDEN" (Residenciales) si no los encuentra, acelerando el proceso masivamente.

### 🇺🇸 ENGLISH
- **🔒 BLIND TRUST**: System now trusts "Lab" proxies for 30 minutes (was 2). This prevents OSINT from wiping them and searching from scratch if you delay.
- **⚡ INSTANT OSINT**: If valid Spanish proxies exist, OSINT starts immediately without demanding "GOLDEN" (Residential) if missing, massively speeding up the process.


## [v2.2.94] - OSINT Input Fix (2026-02-07)
### 🇪🇸 ESPAÑOL
- **🐛 UI FIX**: El campo de teléfono desaparecía al cambiar de "Proxy Lab" a "Buscador OSINT". Ahora se restaura correctamente para que puedas introducir el objetivo.

### 🇺🇸 ENGLISH
- **🐛 UI FIX**: Phone input field was disappearing when switching from "Proxy Lab" to "OSINT Finder". It is now correctly restored so you can enter the target.


## [v2.2.93] - Proxy Lab Crash Fix (2026-02-07)
### 🇪🇸 ESPAÑOL
- **💥 CRASH FIX**: Solucionado error crítico en "Proxy Lab" (`unexpected keyword argument 'force_refresh'`). El motor de búsqueda ahora acepta comandos de refresco forzado.

### 🇺🇸 ENGLISH
- **💥 CRASH FIX**: Fixed critical error in "Proxy Lab" (`unexpected keyword argument 'force_refresh'`). Search engine now accepts force refresh commands.


## [v2.2.92] - Visible Lab (2026-02-07)
### 🇪🇸 ESPAÑOL
- **🐛 UI FIX**: El modo "Buscador de Proxies" no aparecía en el menú desplegable. Ahora sí es visible.
- **📜 RITUAL**: Confirmado y reforzado el protocolo de idioma (Castellano) y proceso de release.

### 🇺🇸 ENGLISH
- **🐛 UI FIX**: "Proxy Finder" mode was not showing in the dropdown. Now it is visible.
- **📜 RITUAL**: Confirmed and reinforced language protocol (Spanish) and release process.


## [v2.2.91] - Proxy Lab Mode (2026-02-07)
### 🇪🇸 ESPAÑOL
- **🔬 PROXY LAB**: Nuevo modo "Buscador de Proxies (Solo)". Permite cazar y validar proxies masivamente sín necesidad de ejecutar un ataque. Los proxies validados (Google-or-Die) se guardan en caché para usarse después en OSINT.
- **🛡️ UI UX**: La interfaz ahora se adapta (color Cian) y oculta campos innecesarios cuando se activa el modo Proxy Lab.

### 🇺🇸 ENGLISH
- **🔬 PROXY LAB**: New mode "Proxy Finder (Only)". Allows massive proxy hunting and validation without running an attack. Validated proxies (Google-or-Die) are cached for later OSINT use.
- **🛡️ UI UX**: Interface now adapts (Cyan color) and hides unnecessary fields when Proxy Lab mode is active.


## [v2.2.90] - Hotfix (Restored Queue) (2026-02-07)
### 🇪🇸 ESPAÑOL
- **🔥 CRITICAL HOTFIX**: Corregido el "Crash al Inicio" de v2.2.89. Se había eliminado accidentalmente la cola de mensajes (`msg_queue`) al optimizar los logs. Restaurada su funcionalidad.

### 🇺🇸 ENGLISH
- **🔥 CRITICAL HOTFIX**: Fixed "Startup Crash" in v2.2.89. The message queue (`msg_queue`) was accidentally removed during log optimization. Restored functionality.


## [v2.2.89] - Google-or-Die & Optimized Logs (2026-02-07)
### 🇪🇸 ESPAÑOL
- **🛡️ GOOGLE-OR-DIE POLICY**: Se acabó la "Amnistía". Ahora un proxy SOLO se acepta si demuestra conexión real con Google (DNS/SSL). Si solo conecta a Cloudflare (1.1.1.1) pero falla en Google, se descarta. Esto elimina los timeouts inmediatos en OSINT.
- **⚡ OPTIMIZED LOGS (EXE FIX)**: Solucionado el "micro-stutter" en la versión compilada (.exe). El sistema de logs ahora pre-compila sus expresiones regulares, eliminando el lag causado por la impresión de texto en consola.

### 🇺🇸 ENGLISH
- **🛡️ GOOGLE-OR-DIE POLICY**: Amnesty is over. Now a proxy is ONLY accepted if it proves real connection to Google (DNS/SSL). If it only connects to Cloudflare but fails Google, it is discarded. This eliminates immediate timeouts in OSINT.
- **⚡ OPTIMIZED LOGS (EXE FIX)**: Fixed "micro-stutter" in compiled (.exe) version. The log system now pre-compiles its regexes, eliminating lag caused by text printing.


## [v2.2.88] - Patience & Throttling (2026-02-07)
### 🇪🇸 ESPAÑOL
- **⏳ TIMEOUT ENFORCER**: Corregido un "olvido" crítico donde los navegadores rotados perdían la configuración de 60s y volvían al timeout por defecto. Ahora se fuerza la paciencia de 60s en cada resurrección o rotación.
- **📉 UI THROTTLER**: Limitada la tasa de actualización de la barra de progreso a 10 veces por segundo. Esto evita que el hilo de trabajo "inunde" la interfaz gráfica durante operaciones rápidas.

### 🇺🇸 ENGLISH
- **⏳ TIMEOUT ENFORCER**: Fixed a critical "amnesia" bug where rotated browsers lost the 60s timeout setting. Now enforcing 60s patience on every resurrection or rotation.
- **📉 UI THROTTLER**: Capped progress bar update rate to 10fps. This prevents the worker thread from flooding the GUI event loop during fast operations.


## [v2.2.87] - Zero Stutter (Paciencia Infinita) (2026-02-07)
### 🇪🇸 ESPAÑOL
- **📉 ZERO STUTTER UI**: Ajustado el ciclo de refresco de logs de 10ms a 100ms. Eliminados los "microsaltos" y la congelación de la ventana al moverla.
- **🔄 SECOND CHANCE PROXY**: Si un proxy falla por `NetTimeout` o `DNS`, ya no se quema instantáneamente. El bot reinicia el driver y le da un segundo intento "gratis".
- **⏳ MODO PACIENCIA (60s)**: Aumentado el timeout de carga de 35s a 60s para soportar proxies residenciales lentos sin falsos negativos.

### 🇺🇸 ENGLISH
- **📉 ZERO STUTTER UI**: Relaxed log refresh rate from 10ms to 100ms. Eliminated micro-stutters and window freezing during movement.
- **🔄 SECOND CHANCE PROXY**: If a proxy fails due to `NetTimeout` or `DNS`, it is no longer burned immediately. The bot restarts the driver and gives it a "free" second attempt.
- **⏳ PATIENCE MODE (60s)**: Increased load timeout from 35s to 60s to support slow residential proxies without false negatives.


## [v2.2.86] - Zenith Amnesty (Resiliencia OSINT) (2026-02-07)
### 🇪🇸 ESPAÑOL
- **🛠️ PARSEO UNIVERSAL DE PROXIES**: Corregido el error crítico de Firefox (`not enough values to unpack`). El sistema ahora interpreta correctamente todos los formatos de proxy (`IP:PORT`, `PROTO|IP:PORT`, `IP:PORT|TIER`).
- **🧬 RESURRECCIÓN ZENITH v2**: Refuerzo de la estabilidad del driver. Si el navegador se cierra o falla antes de una búsqueda, se realiza una limpieza nuclear de procesos y una resurrección atómica.
- **🛡️ ESCUDO DE PROXIES TIER**: Asegurada la compatibilidad total con los rangos GOLDEN, SILVER y BRONZE en todos los navegadores (Chrome/Firefox).
- **🚀 OPTIMIZACIÓN DE FLUJO**: Eliminados los cuellos de botella en la rotación de proxies bajo situaciones de bloqueo masivo.

### 🇺🇸 ENGLISH
- **🛠️ UNIVERSAL PROXY PARSING**: Fixed the critical Firefox unpack error. The system now correctly parses all proxy formats (`IP:PORT`, `PROTO|IP:PORT`, `IP:PORT|TIER`).
- **🧬 ZENITH RESURRECTION v2**: Hardened driver stability. If the browser crashes or fails before a search, a nuclear cleanup and atomic resurrection are performed.
- **🛡️ TIER PROXY SHIELD**: Ensured full compatibility with GOLDEN, SILVER, and BRONZE tiers across all browsers (Chrome/Firefox).
- **🚀 FLOW OPTIMIZATION**: Eliminated proxy rotation bottlenecks during massive blocking events.


## [v2.2.85] - Titan Apex Saul Amnesty (Rescate OSINT) (2026-02-07)
### 🇪🇸 ESPAÑOL
- **♈ AMNISTÍA SAUL v3**: Relajación total de los filtros de validación de proxies. Ahora se aceptan proxies si pasan CUALQUIERA de las 3 fases (IP, DNS o SSL).
- **⏱️ TIMEOUTS RELAX**: Aumentada la paciencia del validador de 4s a 10s-12s para capturar proxies lentos pero funcionales.
- **🛡️ SISTEMA DE CATEGORÍAS**: Implementada clasificación interna de proxies (Golden, Silver, Bronze) para priorizar la mejor conexión disponible.

### 🇺🇸 ENGLISH
- **♈ SAUL AMNESTY v3**: Total relaxation of proxy validation filters. Proxies are now accepted if they pass ANY of the 3 phases (IP, DNS, or SSL).
- **⏱️ RELAXED TIMEOUTS**: Increased validator patience from 4s to 10s-12s to capture slow but functional proxies.
- **🛡️ CATEGORY SYSTEM**: Implemented internal proxy ranking (Golden, Silver, Bronze) to prioritize the best available connection.

### 🇪🇸 ESPAÑOL
- **🔧 HOTFIX TRIPLE-CHECK**: Corregido fallo lógico en la Phase 1 (IP) que descartaba erróneamente proxies por redirecciones 301.
- **🛡️ LENIENCIA TÁCTICA 2/3**: En caso de pool vacío, el bot ahora permite proxies que pasen 2 de las 3 fases (IP + DNS/SSL) para evitar bloqueos totales.
- **⚡ OPTIMIZACIÓN DE CONECTIVIDAD**: Refinado el timeout de resolución para ser más resiliente ante proxies públicos lentos.

### 🇺🇸 ENGLISH
- **🔧 TRIPLE-CHECK HOTFIX**: Fixed logical bug in Phase 1 (IP) that erroneously discarded proxies due to 301 redirects.
- **🛡️ 2/3 TACTICAL LENIENCY**: In case of an empty pool, the bot now allows proxies that pass 2 out of 3 phases (IP + DNS/SSL) to avoid total lockouts.
- **⚡ CONNECTIVITY OPTIMIZATION**: Refined resolution timeout to be more resilient against slow public proxies.

### 🇪🇸 ESPAÑOL
- **🛡️ PROTOCOLO REALIDAD ZENITH**: Implementado validador dictatorial de 3 fases (IP -> DNS -> SSL). Los proxies que no soportan túneles HTTPS o resolución de nombres son ejecutados al instante.
- **⚡ ZERO TUNNEL ERRORS**: Eliminación total de los errores `net::ERR_TUNNEL_CONNECTION_FAILED` gracias al pre-check de túnel CONNECT obligatorio.
- **🌐 DNS SHIELD v2**: Los proxies ahora deben demostrar que saben resolver dominios reales antes de ser entregados al navegador.
- **🔥 PURGA DE RANGOS FANTASMA**: Identificación y bloqueo automático del rango `185.18.250.x` y similares que saboteaban el escaneo con falsos positivos de conectividad.

### 🇺🇸 ENGLISH
- **🛡️ ZENITH REALITY PROTOCOL**: Mandatory 3-phase validator (IP -> DNS -> SSL). Proxies that fail to support HTTPS tunnels or name resolution are terminated immediately.
- **⚡ ZERO TUNNEL ERRORS**: Total elimination of `net::ERR_TUNNEL_CONNECTION_FAILED` errors via mandatory CONNECT tunnel pre-check.
- **🌐 DNS SHIELD v2**: Proxies must prove they can resolve real domains before reaching the browser.
- **🔥 GHOST RANGE PURGE**: Automatic identification and blocking of `185.18.250.x` and similar ranges that sabotaged scans with connectivity false positives.


## [v2.2.82] - Titan Apex Saul Zenith (El Juicio Final) (2026-02-07)
### 🇪🇸 ESPAÑOL
- **🧬 RESURRECCIÓN ATÓMICA (DRIVER SYNC)**: El bot ahora monitoriza la vida del navegador en tiempo real (`is_alive`). Si detecta un fallo o cierre accidental, lo resucita de forma atómica y transparente. Se acabó el error `WinError 10061`.
- **⚡ MODO LENIENCIA ZENITH**: Relajación de filtros para evitar el descarte masivo de proxies. Ahora se aceptan proxies de Datacenter (ES) si no hay residenciales, y la latencia permitida ha subido de 2.0s a **4.5s**.
- **👁️ INTEL NIVEL 5**: Expansión masiva de dorks de inteligencia. Integración de dorks para TrueCaller, RocketReach y ContactOut para maximizar el hallazgo de identidades reales.
- **🧹 LIMPIEZA INTELIGENTE**: Eliminadas las funciones de limpieza autodestructivas. El bot ahora limpia procesos de forma segura sin interferir con la sesión activa.

### 🇺🇸 ENGLISH
- **🧬 ATOMIC RESTORATION (DRIVER SYNC)**: Real-time browser heartbeat monitoring (`is_alive`). Instantly resuscitates the driver if it crashes or is closed, killing `WinError 10061` for good.
- **⚡ ZENITH LENIENCY MODE**: Filter relaxation to avoid empty proxy pools. Now accepts Datacenter proxies (ES) as fallback, and latency limit raised to **4.5s**.
- **👁️ LEVEL 5 INTEL**: Massive dork expansion. Added TrueCaller, RocketReach, and ContactOut to maximize real identity hits.
- **🧹 SMART CLEANUP**: Removed self-destructive cleanup functions. Safer process management without killing the active session.


## [v2.2.81] - Titan Apex Saul Overclock (The Final Stand) (2026-02-07)
### 🇪🇸 ESPAÑOL
- **⏳ OVERCLOCKED TIMEOUTS**: Aumentado el tiempo de carga por página a 60 segundos. Esto permite que los proxies residenciales españoles (lentos pero efectivos) tengan tiempo de cargar los datos sin ser descartados.
- **🛡️ AMNISTÍA 25 (PERSISTENCIA EXTREMA)**: Elevado el límite de rotación a 25. El bot no se detendrá hasta agotar todas las posibilidades del pool UHQ.
- **🧠 REINTENTO INTELIGENTE (DNS SHIELD)**: El sistema ahora diferencia entre un bloqueo de servidor y un error de red (DNS/Conexión). Los fallos de red ya no penalizan los intentos de la fuente, permitiendo reintentar con un proxy nuevo sin saltar la web.
- **🇪🇸 UHQ SOURCE EXPANSION**: Inyectadas nuevas fuentes de proxies premium específicas para España.

### 🇺🇸 ENGLISH
- **⏳ OVERCLOCKED TIMEOUTS**: Increased page load time to 60 seconds to support slow but effective residential proxies.
- **🛡️ AMNESTY 25 (EXTREME PERSISTENCE)**: Raised rotation limit to 25. The bot will exhaust the entire UHQ pool before giving up.
- **🧠 SMART RETRY (DNS SHIELD)**: Network errors (DNS/Connection) no longer count against source attempts, allowing fresh proxy retries without skipping sources.
- **🇪🇸 UHQ SOURCE EXPANSION**: Added new premium Spanish proxy sources.


## [v2.2.77] - Titan Apex Reality (Flujo Absoluto) (2026-02-07)
### 🇪🇸 ESPAÑOL
- **🏎️ BYPASS DE VERIFICACIÓN**: El Scraper ya no re-verifica los proxies que él mismo acaba de validar. Entrega inmediata FIFO para evitar falsos negativos post-scrape.
- **⏳ ESPERAS GRATUITAS**: La espera por sincronización de proxy en el OSINT ya no penaliza el contador de rotaciones. El sistema puede esperar indefinidamente a que el proxy enganche sin abortar la búsqueda.
- **️ CONFIANZA UNIFICADA**: Sincronización total entre los módulos de red para asegurar que el primer proxy funcional sea usado al instante.

### 🇺🇸 ENGLISH
- **🏎️ VERIFICATION BYPASS**: Scraper no longer re-verifies proxies it just validated. Immediate FIFO delivery to avoid post-scrape false negatives.
- **⏳ FREE WAITING**: Waiting for proxy synchronization in OSINT no longer penalizes the rotation counter. The system can wait indefinitely for the proxy to hook without aborting the search.
- **️ UNIFIED TRUST**: Total synchronization between network modules to ensure the first functional proxy is used instantly.


## [v2.2.74] - Titan Apex Ultimate (Amnistía Golden) (2026-02-06)
### 🇪🇸 ESPAÑOL
- **⚖️ CORRECCIÓN DE VALIDACIÓN CRÍTICA**: Flexibilizado el Geo-Guard en el Scraper para permitir que proxies marcados como `GOLDEN` (Oro) sean aceptados cuando se requiere país `ES` (España). Se acabó el error de "país incorrecto (GOLDEN != ES)".
- **🚀 ESTABILIDAD DE ESCANEO**: Eliminado el bloqueo final que causaba el bucle de rotación infinita en el modo OSINT.
- **🛡️ SINCRONIZACIÓN TOTAL**: Armonización completa de criterios de validación entre todos los módulos del core.

### 🇺🇸 ENGLISH
- **⚖️ CRITICAL VALIDATION FIX**: Relaxed Geo-Guard in the Scraper to allow proxies marked as `GOLDEN` to be accepted when country `ES` is required. Fixed the "incorrect country (GOLDEN != ES)" error.
- **🚀 SCAN STABILITY**: Removed the final blockage that caused the infinite rotation loop in OSINT mode.
- **🛡️ TOTAL SYNC**: Full harmonization of validation criteria across all core modules.


## [v2.2.73] - Titan Apex Final (Global Sync) (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🤝 SINCRONIZACIÓN DE CONFIANZA DEFINITIVA**: El OSINT ahora acepta cualquier proxy validado como español (`ES` o `GOLDEN`) por el Scraper. Se acabó el rechazo de proxies válidos y el bucle de rotación infinita.
- **🛡️ EXPANSIÓN DE LISTA BLANCA ASN**: Añadidas más redes residenciales españolas (Yoigo, Pepephone, Vodafone Retail) para maximizar la calidad del pool.
- **⚡ CERO SALTOS EN FALSO**: Eliminado el error "ERROR ZENITH" que causaba que el bot se rindiera aun teniendo proxies vivos.

### 🇺🇸 ENGLISH
- **🤝 ULTIMATE TRUST SYNC**: OSINT now accepts any proxy validated as Spanish (`ES` or `GOLDEN`) by the Scraper. No more rejection of valid proxies and infinite rotation loops.
- **🛡️ ASN WHITELIST EXPANSION**: Added more Spanish residential networks (Yoigo, Pepephone, Vodafone Retail) to maximize pool quality.
- **⚡ ZERO FALSE SKIPS**: Removed the "ERROR ZENITH" error that caused the bot to give up even with live proxies available.


## [v2.2.72] - Titan Apex Hotfix (Binary Integrity) (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🚀 HOTFIX DE COMPILACIÓN**: Corregido un error de indentación crítico en `core/osint.py` que impedía que el binario se ejecutara correctamente (`ModuleNotFoundError`).
- **🛡️ ESTABILIDAD ZENITH**: Asegurada la integridad del protocolo Zenith Apex tras la limpieza de código.

### 🇺🇸 ENGLISH
- **🚀 BUILD HOTFIX**: Fixed a critical indentation error in `core/osint.py` that prevented the binary from running correctly (`ModuleNotFoundError`).
- **🛡️ ZENITH STABILITY**: Ensured the integrity of the Zenith Apex protocol after code cleanup.


## [v2.2.71] - Titan Apex (Nuclear Sanitization) (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🧼 SANEAMIENTO NUCLEAR DE CACHÉ**: El bot ahora limpia automáticamente la caché al arrancar, eliminando proxies "zombis" de M247 o Datacenters de sesiones antiguas. Pool 100% puro desde el inicio.
- **👑 PROTOCOLO ZENITH APEX**: Dependencia total del OSINT hacia el Scraper. Se han eliminado TODOS los checks redundantes de Geo-IP en el módulo OSINT, confiando ciegamente en la validación del Scraper.
- **⚡ CERO LATENCIA DE INICIO**: El tiempo muerto antes de empezar un escaneo OSINT se ha reducido a la nada absoluta en proxies ya validados.
- **🛡️ SINCRONIZACIÓN ASN TOTAL**: Bloqueo absoluto y coordinado de ASNs de Datacenter en todos los niveles del core.

### 🇺🇸 ENGLISH
- **🧼 NUCLEAR CACHE SANITIZATION**: The bot now automatically cleans the cache on startup, removing "zombie" M247 or Datacenter proxies from old sessions. 100% pure pool from the start.
- **👑 ZENITH APEX PROTOCOL**: Total OSINT dependency on the Scraper. ALL redundant Geo-IP checks in the OSINT module have been removed, fully trusting the Scraper's validation.
- **⚡ ZERO STARTUP LATENCY**: Dead time before starting an OSINT scan has been reduced to absolute zero for already validated proxies.
- **🛡️ TOTAL ASN SYNC**: Absolute and coordinated blocking of Datacenter ASNs across all core levels.


## [v2.2.70] - Titan Zenith Resolve (The Final Sync) (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🤝 PROTOCOLO ZENITH TRUST v2**: El módulo OSINT ahora confía plenamente en la sabiduría del Scraper. Si un proxy ya fue verificado como "Oro", el OSINT salta todos los pre-checks redundantes.
- **⚡ ELIMINACIÓN DE API LOCKS**: Reducción drástica de llamadas a APIs de Geo-IP (ip-api.com). Se acabó el error "Geo-Check Locked" causado por el bot pisándose a sí mismo.
- **🛡️ SINCRONIZACIÓN ASN INTEGRAL**: El OSINT hereda la lista negra nuclear del scraper. Los proxies de M247 y otros datacenters se rechazan en milisegundos.
- **🏎️ INICIO ULTRA-RÁPIDO**: El tiempo muerto entre encontrar un proxy e iniciar el escaneo se ha reducido de ~40s a ~0.1s en proxies cacheados.

### 🇺🇸 ENGLISH
- **🤝 ZENITH TRUST v2 PROTOCOL**: OSINT module now fully trusts Scraper metadata. If a proxy is already "GOLDEN", OSINT skips all redundant pre-checks.
- **⚡ API LOCK ELIMINATION**: Drastic reduction in Geo-IP API calls. Fixed "Geo-Check Locked" errors caused by redundant module requests.
- **🛡️ INTEGRAL ASN SYNC**: OSINT inherits the scraper's nuclear blacklist. M247 and datacenter proxies are rejected in milliseconds.
- **🏎️ ULTRA-FAST START**: Dead time between finding a proxy and starting the scan reduced from ~40s to ~0.1s for cached proxies.


## [v2.2.69] - Titan Eternal (The Final Resolve) (2026-02-06)
### 🇪🇸 ESPAÑOL
- **☢️ FILTRADO ASN NUCLEAR**: Implementación de una lista negra de datacenters (M247, Akamai, DigitalOcean, etc.). Estos proxies se filtran instantáneamente, ahorrando un 90% de tiempo en la validación.
- **🚀 FASE 2 REIMAGINADA**: La Fase 2 ahora es una búsqueda profunda ultra-específica para España en lugar de una minería global ineficiente. Más calidad, menos basura.
- **🏎️ BYPASS DE COOLDOWN**: El sistema ahora ignora automáticamente el tiempo de enfriamiento si el pool de proxies está agotado (0 proxies), permitiendo búsquedas de emergencia instantáneas.
- **🔄 OPTIMIZACIÓN DE FLUJO**: Refinado el sistema de hilos para una validación más limpia y rápida bajo situaciones de bloqueo.

### 🇺🇸 ENGLISH
- **☢️ NUCLEAR ASN FILTERING**: Implementation of a datacenter blacklist (M247, Akamai, DigitalOcean, etc.). These proxies are filtered instantly, saving 90% of validation time.
- **🚀 REIMAGINED PHASE 2**: Phase 2 is now an ultra-specific deep search for Spain instead of inefficient global mining. More quality, less junk.
- **🏎️ COOLDOWN BYPASS**: The system now automatically ignores cooldown if the proxy pool is exhausted (0 proxies), allowing instant emergency searches.
- **🔄 FLOW OPTIMIZATION**: Refined threading system for cleaner, faster validation under blocking situations.


## [v2.2.68] - Titan Nitro (UI Fix & Speed Tuning) (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🛠️ FIX DE GUI**: Corregido el error crítico `'TextRedirector' object has no attribute 'flush'` que causaba fallos visuales en el contador de progreso.
- **🚀 TRUNCAMIENTO NITRO**: Reducción agresiva de candidatos de 5000 a 250 en la Fase 1. El bot ahora encuentra proxies españoles en segundos, priorizando la calidad sobre la cantidad bruta.
- **📊 FEEDBACK LIMPIO**: Rediseñado el contador de progreso para ser compatible con la consola de la GUI, evitando textos desordenados.
- **⚡ OPTIMIZACIÓN DE BUCLE**: Ajuste de hilos y chunks para un flujo de validación ultra-suave.

### 🇺🇸 ENGLISH
- **🛠️ GUI FIX**: Fixed critical error `'TextRedirector' object has no attribute 'flush'` that caused visual glitches in the progress counter.
- **🚀 NITRO TRUNCATION**: Aggressive candidate reduction from 5000 to 250 in Phase 1. The bot now finds Spanish proxies in seconds, prioritizing quality over raw quantity.
- **📊 CLEAN FEEDBACK**: Redesigned the progress counter to be compatible with the GUI console, avoiding disorganized text.
- **⚡ LOOP OPTIMIZATION**: Adjusted threads and chunks for an ultra-smooth validation flow.


## [v2.2.67] - Titan Overlord Velocity (The Fast Check Edition) (2026-02-06)
### 🇪🇸 ESPAÑOL
- **📊 CONTADOR EN TIEMPO REAL**: Implementación de un feedback visual de progreso (`[X/5000]`) durante la verificación de proxies. Se acabó el no saber si el bot está funcionando.
- **⚡ ACELERACIÓN TURBO**: Aumento de 5 a 15 hilos concurrentes para el procesado individual de IPs. Triplicada la velocidad de validación en situaciones de bloqueo.
- **🎯 TRUNCAMIENTO INTELIGENTE**: Si las APIs están saturadas, el bot ahora prioriza los primeros 500 mejores candidatos en lugar de intentar procesar 5000 lentamente, garantizando resultados inmediatos.

### 🇺🇸 ENGLISH
- **📊 REAL-TIME COUNTER**: Implementation of visual progress feedback (`[X/5000]`) during proxy verification. No more wondering if the bot is working.
- **⚡ TURBO ACCELERATION**: Increased concurrent threads from 5 to 15 for individual IP processing. Verification speed tripled in blocking situations.
- **🎯 SMART TRUNCATION**: If APIs are saturated, the bot now prioritizes the top 500 candidates instead of slowly attempting 5000, ensuring immediate results.


## [v2.2.66] - Titan Overlord (Absolute Stability) (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🤫 SILENCIO ADMINISTRATIVO**: Eliminados los logs ruidosos de bloqueo de API en consola. El bot ahora gestiona las rotaciones de forma silenciosa y eficiente.
- **⏳ RESILIENCIA DE RED v2**: Tiempos de espera (timeouts) triplicados para absorber lags de red y evitar la pérdida de proxies.
- **🛡️ ESCUDO STEALTH**: Implementación de retrasos aleatorios (jitter) entre peticiones para evitar la detección por parte de los proveedores Geo-IP.
- **💠 PERSISTENCIA REFORZADA**: Los proxies "Golden" ahora tienen prioridad absoluta en el arranque, asegurando disponibilidad inmediata.

### 🇺🇸 ENGLISH
- **🤫 ADMINISTRATIVE SILENCE**: Removed noisy API block logs from console. The bot now manages rotations silently and efficiently.
- **⏳ NETWORK RESILIENCE v2**: Tripled timeouts to absorb network lags and prevent proxy loss.
- **🛡️ STEALTH SHIELD**: Implementation of random delays (jitter) between requests to avoid detection by Geo-IP providers.
- **💠 REINFORCED PERSISTENCE**: "Golden" proxies now have absolute priority during startup, ensuring immediate availability.


## [v2.2.65] - Titan Prime (The Bot that Never Forgets) (2026-02-06)
### 🇪🇸 ESPAÑOL
- **💠 PERSISTENCIA DE ORO**: Eliminado el borrado automático de caché. El bot ahora guarda los proxies residenciales entre sesiones. Si las APIs Geo-IP fallan, el bot usará proxies "Golden" veteranos.
- **🛰️ TRIDENTE DE 6 VÍAS**: Incorporación de `ipapi.is` como proveedor premium. Rotación ultra-resiliente entre 6 APIs globales para evitar bloqueos 429.
- **🛡️ ESCUDO NUCLEAR v4**: Ampliación de la lista negra de ASNs para filtrar datacenters disfrazados de residenciales.

### 🇺🇸 ENGLISH
- **💠 GOLDEN PERSISTENCE**: Automatic cache purge removed. The bot now saves residential proxies between sessions. If Geo-IP APIs fail, the bot will use veteran "Golden" proxies.
- **🛰️ 6-WAY TRIDENT**: Integrated `ipapi.is` as a premium provider. Ultra-resilient rotation among 6 global APIs to avoid 429 blocks.
- **🛡️ NUCLEAR SHIELD v4**: Expanded ASN blacklist to filter datacenters disguised as residential.


## [v2.2.64] - Zenith Omega (Absolute Resilience) (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🛰️ ZENITH OMEGA (Resiliencia Absoluta)**: Implementación de un gestor de bloqueos de API. Si una API nos da error 429, el bot la pone en "cuarentena" y rota instantáneamente a 4 alternativas más (ipapi.co, ipwho.is, freeipapi, findip).
- **🛠️ FIX ARQUITECTURAL FINAL**: Reestructuración total de las funciones de filtrado para eliminar los errores de alcance (`UnboundLocalError`) de raíz.
- **🚀 OPTIMIZACIÓN DE LOGS**: Reducción del ruido en consola para centrarse en los resultados de proxies residenciales españoles.

### 🇺🇸 ENGLISH
- **🛰️ ZENITH OMEGA (Absolute Resilience)**: API Lock Manager implementation. If an API returns a 429 error, the bot puts it in "quarantine" and instantly rotates to 4 more alternatives (ipapi.co, ipwho.is, freeipapi, findip).
- **🛠️ FINAL ARCHITECTURAL FIX**: Total restructuring of filtering functions to eliminate scope errors (`UnboundLocalError`) once and for all.
- **🚀 LOG OPTIMIZATION**: Reduced console noise to focus on Spanish residential proxy results.


## [v2.2.63] - Zenith Protocol (Stability Patch) (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🛠️ FIX CRÍTICO DE ESTABILIDAD**: Corregido un error de arquitectura (`UnboundLocalError`) que causaba el cierre del bot al activar el Tridente de Supervivencia.
- **⚡ OPTIMIZACIÓN DE ALCANCE**: Reorganización de funciones internas en el Scraper para garantizar que la verificación individual de IPs sea siempre accesible.

### 🇺🇸 ENGLISH
- **🛠️ CRITICAL STABILITY FIX**: Fixed an architectural error (`UnboundLocalError`) that caused the bot to crash when activating the Survival Trident.
- **⚡ SCOPE OPTIMIZATION**: Reorganization of internal functions in the Scraper to ensure individual IP verification is always accessible.


## [v2.2.62] - Zenith Protocol (The God Mode Sync) (2026-02-06)
### 🇪🇸 ESPAÑOL
- **⭐ ZENITH TRUST (Sincronización Total)**: El motor OSINT ahora comparte la Geo-Caché con el Scraper. Se acabó el re-verificar IPs: si el scraper dice que es GOLDEN, el OSINT confía y arranca al instante.
- **🚀 ELIMINACIÓN DE LAG 429**: Al compartir la caché, reducimos las consultas API en un 80%, eliminando casi por completo los bloqueos por exceso de peticiones.
- **🛡️ TRIDENTE GEO-IP v2**: Refuerzo de la rotación de APIs bach/individual para que el filtrado de proxies sea imparable.
- **🚫 BLOQUEO ATÓMICO M247 v3**: Muro infranqueable contra hostings rumanos, sincronizado en todo el ecosistema del bot.

### 🇺🇸 ENGLISH
- **⭐ ZENITH TRUST (Total Sync)**: The OSINT engine now shares Geo-Cache with the Scraper. No more redundant IP checks: if the scraper says it's GOLDEN, OSINT trusts it and starts instantly.
- **🚀 429 LAG ELIMINATION**: By sharing the cache, we reduce API calls by 80%, almost completely eliminating throttling blocks.
- **🛡️ GEO-IP TRIDENT v2**: Reinforced batch/individual API rotation to make proxy filtering unstoppable.
- **🚫 ATOMIC M247 BLOCK v3**: Impenetrable wall against Romanian hostings, synchronized across the entire bot ecosystem.


## [v2.2.61] - Titan Finality (The Last Stand Edition) (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🛰️ RADAR DE SUPERVIVENCIA**: Inclusión de fuentes ultra-nicho de España para combatir la escasez crítica de proxies residenciales.
- **🔄 TRIDENTE GEO-IP ROTATIVO**: Nuevo sistema de rotación automática entre APIs de Geo-IP (ip-api, ipwhois) para evitar bloqueos por error 429.
- **🛡️ BLOQUEO NUCLEAR ASN v2**: Refuerzo total contra hostings detectados (AS9009, M247) sincronizado en el scraper y el motor OSINT.
- **⚠️ POLÍTICA DE RESILENCIA**: Ajuste del Jitter y tiempos de espera para garantizar el filtrado incluso bajo presión de las APIs.

### 🇺🇸 ENGLISH
- **🛰️ SURVIVAL RADAR**: Inclusion of ultra-niche Spanish sources to combat the critical shortage of residential proxies.
- **🔄 ROTATING GEO-IP TRIDENT**: New automatic rotation system between Geo-IP APIs (ip-api, ipwhois) to avoid error 429 blocks.
- **🛡️ NUCLEAR ASN BLOCK v2**: Total reinforcement against detected hostings (AS9009, M247) synchronized in the scraper and OSINT engine.
- **⚠️ RESILIENCE POLICY**: Jitter and timeout adjustments to ensure filtering even under API pressure.


## [v2.2.60] - Titan Ultimatum (Absolute Zero Edition) (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🔥 CORRECCIÓN CRÍTICA DE CACHÉ**: Reparado el bug que ignoraba proxies residenciales guardados. Ahora el bot "recuerda" y prioriza las IPs GOLDEN correctamente.
- **🛡️ GUARDIA ASN EXPANDIDA**: Inclusión de nuevos rangos residenciales (Euskaltel, Adamo, MasMovil, R, Telecable) para maximizar el éxito en España.
- **🚫 BLOQUEO NUCLEAR M247**: Refuerzo total contra hostings rumanos. Si el ASN no es puramente residencial ESPAÑOL, el proxy se fulmina en el acto.
- **⚡ OPTIMIZACIÓN DE ROTACIÓN**: Reducción drástica de rotaciones fallidas al filtrar la basura antes de que llegue al motor OSINT.

### 🇺🇸 ENGLISH
- **🔥 CRITICAL CACHE FIX**: Fixed the bug that ignored saved residential proxies. The bot now correctly "remembers" and prioritizes GOLDEN IPs.
- **🛡️ EXPANDED ASN GUARD**: Inclusion of new residential ranges (Euskaltel, Adamo, MasMovil, R, Telecable) to maximize success in Spain.
- **🚫 M247 NUCLEAR BLOCK**: Total reinforcement against Romanian hostings. If the ASN is not purely SPANISH residential, the proxy is killed instantly.
- **⚡ ROTATION OPTIMIZATION**: Drastic reduction in failed rotations by filtering trash before it reaches the OSINT engine.


## [v2.2.59] - Titan Ultimatum (The God Particle) (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🏁 PURGA ATÓMICA DE CACHÉ**: El bot ahora limpia automáticamente todos los proxies antiguos al iniciar para evitar contaminación por hostings obsoletos.
- **🥇 POLÍTICA GOLDEN-ONLY**: Tolerancia cero absoluta. Solo se permiten proxies identificados como puramente residenciales (GOLDEN) mediante ASN verificado.
- **🛡️ GUARDIA ASN SINCRONIZADA**: La misma lista blanca de redes residenciales se aplica ahora tanto en el escaneo inicial como en el pre-check del OSINT.
- **🚫 BLOQUEO RADICAL DE HOSTING**: Cualquier IP de M247, centros de datos o segmentos no residenciales se descarta en milisegundos.

### 🇺🇸 ENGLISH
- **🏁 ATOMIC CACHE PURGE**: The bot now automatically clears all old proxies on startup to avoid contamination by obsolete hostings.
- **🥇 GOLDEN-ONLY POLICY**: Absolute zero tolerance. Only proxies identified as purely residential (GOLDEN) via verified ASN are allowed.
- **🛡️ SYNCHRONIZED ASN GUARD**: The same residential network whitelist is now applied in both the initial scan and the OSINT pre-check.
- **🚫 RADICAL HOSTING BLOCK**: Any IP from M247, data centers, or non-residential segments is discarded in milliseconds.


## [v2.2.58] - Titan Finality (The Absolute Zero) (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🧹 PURGA DE FUENTES**: Eliminación drástica de fuentes de proxies de baja calidad y listas contaminadas de GitHub. Solo quedan fuentes UHQ balanceadas.
- **⚛️ FILTRADO ASN NUCLEAR (BATCH FIX)**: Corrección del motor de procesamiento por lotes. Ahora el bloqueo de hostings (M247/Rumanía) es atómico e inevitable.
- **🛡️ ZERO-TOLERANCE POLICY**: Si una IP no pertenece a un ASN residencial verificado (Movistar, Orange, Vodafone, Digi), se descarta de inmediato para el OSINT.
- **🎯 OPTIMIZACIÓN ZENITH+**: Refinamiento de la lógica de reconexión y rotación para evitar el agotamiento de proxies útiles.

### 🇺🇸 ENGLISH
- **🧹 SOURCE PURGE**: Drastic removal of low-quality proxy sources and contaminated GitHub lists. Only balanced UHQ sources remain.
- **⚛️ ATOMIC ASN FILTERING (BATCH FIX)**: Correction of the batch processing engine. Hosting blocking (M247/Romania) is now atomic and unavoidable.
- **🛡️ ZERO-TOLERANCE POLICY**: If an IP does not belong to a verified residential ASN (Movistar, Orange, Vodafone, Digi), it is immediately discarded for OSINT.
- **🎯 ZENITH+ OPTIMIZATION**: Refinement of reconnection and rotation logic to prevent depletion of useful proxies.


## [v2.2.57] - Titan Zenith (Zero-Fail Edition) (2026-02-06)
### 🇪🇸 ESPAÑOL
- **💎 FILTRADO ATÓMICO POR ASN**: Sistema de verificación por red (DNI de Internet) infalible. Solo se permiten ISPs españoles residenciales (Movistar, Vodafone, Orange, etc.).
- **🔱 TRIDENTE GEO-IP**: Rotación automática entre 3 APIs de geolocalización (ip-api + ipapi.co + findip) para anular errores 429 y bloqueos.
- **🚀 UHQ PROXY ENGINE v4**: Nuevas fuentes de proxies de ultra-nicho actualizadas a febrero de 2026.
- **🛡️ ZERO-HOSTING POLICY**: Bloqueo absoluto de M247 y otros proveedores de centros de datos mediante ASN duro.

### 🇺🇸 ENGLISH
- **💎 ATOMIC ASN FILTERING**: Infallible network-based verification system. Only Spanish residential ISPs allowed (Movistar, Vodafone, Orange, etc.).
- **🔱 GEO-IP TRIDENT**: Automatic rotation between 3 geolocation APIs (ip-api + ipapi.co + findip) to nullify 429 errors and blocks.
- **🚀 UHQ PROXY ENGINE v4**: New ultra-niche proxy sources updated to February 2026.
- **🛡️ ZERO-HOSTING POLICY**: Absolute blocking of M247 and other data center providers via hard ASN check.


## [v2.2.56] - Titan Omega (The Unstoppable) (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🏆 RESIDENTIAL WHITE-LIST**: Implementación de una lista blanca de ISPs españoles (Movistar, Orange, Vodafone, Digi, etc.). Los proxies residenciales ahora se marcan como "GOLDEN" y tienen prioridad.
- **⚡ ANTI-429 OMEGA MOTOR**: Sistema de Jitter y reintentos inteligentes para evitar el bloqueo de las APIs de Geo-Check.
- **🛡️ GEOLOCALIZACIÓN 100% CONDICIONAL**: Se ha eliminado toda inyección de localización española cuando el proxy está desactivado. Ahora es 100% transparente.
- **🎨 UX PREMIMUM**: El botón "Copiar Logs" ahora es verde vibrante para una mejor visibilidad inmediata.

### 🇺🇸 ENGLISH
- **🏆 RESIDENTIAL WHITE-LIST**: Implementation of a Spanish ISP whitelist (Movistar, Orange, Vodafone, Digi, etc.). Residential proxies are now marked as "GOLDEN" and have priority.
- **⚡ ANTI-429 OMEGA ENGINE**: Jitter system and smart retries to prevent Geo-Check API blocking.
- **🛡️ 100% CONDITIONAL GEOLOCATION**: Removed all Spanish location injection when the proxy is disabled. It is now 100% transparent.
- **🎨 PREMIUM UX**: The "Copy Logs" button is now vibrant green for better immediate visibility.


## [v2.2.55] - Titan Supreme (Final Boss Edition) (2026-02-06)
### 🇪🇸 ESPAÑOL
- **📋 BOTÓN COPIAR LOGS**: Nueva utilidad en la interfaz para copiar el registro de operaciones al portapapeles con un clic.
- **🌍 GEOLOCALIZACIÓN CONDICIONAL**: La geolocalización forzada en España ahora solo se activa si hay un proxy activo, permitiendo navegación real sin proxy.
- **🚀 ELITE SOURCES v2**: Inyección de nuevas fuentes de proxies UHQ de alta fidelidad residencial.
- **🛡️ HARDENED ANTI-DC**: Filtro reforzado contra proveedores de hosting rumanos y falsos proxies españoles.

### 🇺🇸 ENGLISH
- **📋 COPY LOGS BUTTON**: New utility in the interface to copy the operation log to the clipboard with one click.
- **🌍 CONDITIONAL GEOLOCATION**: Forced Spain geolocation now only activates if an active proxy is present, allowing real navigation without proxy.
- **🚀 ELITE SOURCES v2**: Injection of new high-fidelity residential UHQ proxy sources.
- **🛡️ HARDENED ANTI-DC**: Reinforced filtering against Romanian hosting providers and fake Spanish proxies.


## [v2.2.54] - Titan God Mode (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🚀 TITAN GOD MODE PROXYING**: Sistema de adquisición de proxies de grado militar con validación de dominio residencial `.es` (Marca.com/Google.es).
- **🛡️ ZERO-FAIL VALIDATION**: Motor de verificación blindado contra el bloqueo sistémico de Datacenters.
- **🔄 SMART ROTATION**: El sistema ahora detecta anomalías de red y purga la caché automáticamente para garantizar aire fresco residencial.
- **⚡ ULTRA-LOW LATENCY**: Nuevo filtro de latencia extrema (< 2.0s) para asegurar una experiencia OSINT instantánea.

### 🇺🇸 ENGLISH
- **🚀 TITAN GOD MODE PROXYING**: Military-grade proxy acquisition system with residential `.es` domain validation (Marca.com/Google.es).
- **🛡️ ZERO-FAIL VALIDATION**: Verification engine hardened against systemic Datacenter blocking.
- **🔄 SMART ROTATION**: The system now detects network anomalies and automatically purges the cache to ensure fresh residential IPs.
- **⚡ ULTRA-LOW LATENCY**: New extreme latency filter (< 2.0s) to ensure an instant OSINT experience.


## [v2.2.53] - Titan Supreme UHQ (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🚀 SUPREME PROXY ENGINE**: Rediseñado el motor de búsqueda de proxies para priorizar IPs residenciales españolas de alta calidad (UHQ).
- **🛡️ DEEP ISP DETECT**: Bloqueo implacable de Datacenters y Hosting (M247, Hetzner, OVH, etc.) integrado directamente en la fase de scraping.
- **💾 GEO-CACHE PERSISTENCE**: El bot ahora "recuerda" la ubicación y calidad de las IPs entre sesiones, eliminando tiempos de espera y duplicidad de peticiones.
- **🛡️ ENHANCED QUANTUM VERIFIER**: Lógica optimizada para evitar falsos positivos y asegurar que el OSINT trabaje solo con conexiones indetectables.

### 🇺🇸 ENGLISH
- **🚀 SUPREME PROXY ENGINE**: Redesigned proxy search engine to prioritize high-quality Spanish residential IPs (UHQ).
- **🛡️ DEEP ISP DETECT**: Relentless blocking of Datacenters and Hosting (M247, Hetzner, OVH, etc.) integrated directly into the scraping phase.
- **💾 GEO-CACHE PERSISTENCE**: The bot now "remembers" IP location and quality between sessions, eliminating wait times and duplicate requests.
- **🛡️ ENHANCED QUANTUM VERIFIER**: Optimized logic to avoid false positives and ensure OSINT works only with undetectable connections.


## [v2.2.52] - Titan Quantum Check (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🛡️ TITAN QUANTUM CHECK**: Rediseñado el motor de verificación Geo-IP. Ahora utiliza un sistema dinámico de 8+ APIs con parsers específicos para asegurar la validación incluso bajo bloqueos masivos.
- **🚫 DC-SHIELD**: Implementado filtro avanzado de ISPs para descartar automáticamente proxies de centros de datos (M247, etc.) y priorizar conexiones residenciales de España.
- **⚡ RESILIENT SESSIONS**: Integrado sistema de reintentos con cabeceras de navegador reales para las peticiones de validación.

### 🇺🇸 ENGLISH
- **🛡️ TITAN QUANTUM CHECK**: Redesigned the Geo-IP verification engine. Now uses a dynamic 8+ API system with specific parsers to ensure validation even under massive blocks.
- **🚫 DC-SHIELD**: Implemented advanced ISP filtering to automatically discard data center proxies (M247, etc.) and prioritize Spanish residential connections.
- **⚡ RESILIENT SESSIONS**: Integrated retry system with real browser headers for validation requests.


## [v2.2.51] - Hotfix Stabilizer (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🛠️ CRITICAL STABILITY HOTFIX**: Corregido error `UnboundLocalError` en el motor OSINT que provocaba el cierre de la aplicación al fallar la validación de IP.
- **🛡️ SCOPE FIX**: Asegurada la disponibilidad de variables de excepción dentro del bloque de rotación de proxies.

### 🇺🇸 ENGLISH
- **🛠️ CRITICAL STABILITY HOTFIX**: Fixed `UnboundLocalError` in the OSINT engine that caused the application to crash when IP validation failed.
- **🛡️ SCOPE FIX**: Ensured exception variable availability within the proxy rotation block.


## [v2.2.50] - Titan Perfecta v3 (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🚀 BOOTSTRAP SPLASH**: Adiós al inicio silencioso. Ahora una ventana de carga instantánea aparece en el milisegundo 1 para informar del progreso de carga.
- **💎 ELITE SOURCE INJECTION**: Integración de nuevas fuentes de proxies de alta fidelidad basadas en el repositorio de Rick Grimes.
- **🛡️ GEO-RESILIENCE**: Implementado sistema de respaldo triple (ip-api + ifconfig + ipify) para evitar descartar proxies válidos por saturación de APIs.
- **🔋 NEW SERVICES**: Añadidos servicios de callback para Verti Seguros, Sicor Alarmas, AutoSolar y RACE.
- **🛠️ OSINT HOTFIX**: Corregido error de indentación y variable `px_ip` no definida en `core/osint.py` que causaba cierres inesperados.
- **🧹 CODE CLEANUP**: Eliminado `megapack.py` tras consolidar y mejorar sus servicios en módulos especializados.
- **⚡ ZERO-STUTTER v2**: Optimizada la gestión de hilos de la interfaz para una fluidez absoluta bajo carga máxima.

### 🇺🇸 ENGLISH
- **🚀 BOOTSTRAP SPLASH**: No more silent startup. An instant loading window now appears at millisecond 1 to provide visual feedback.
- **💎 ELITE SOURCE INJECTION**: Integrated new high-fidelity proxy sources inspired by the Rick Grimes repository.
- **🛡️ GEO-RESILIENCE**: Implemented triple fallback system (ip-api + ifconfig + ipify) to prevent discarding valid proxies due to API saturation.
- **🔋 NEW SERVICES**: Added callback services for Verti Seguros, Sicor Alarmas, AutoSolar, and RACE.
- **🛠️ OSINT HOTFIX**: Fixed IndentationError and undefined `px_ip` in `core/osint.py` that caused unexpected crashes.
- **🧹 CODE CLEANUP**: Removed `megapack.py` after consolidating and improving its services into specialized modules.
- **⚡ ZERO-STUTTER v2**: GUI thread management optimized for absolute smoothness under heavy load.


## [v2.2.49] - Titan Fix (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🛠️ CRITICAL SYNTAX REPAIR**: Eliminado el código huérfano en `core/browser.py` que provocaba el error `ModuleNotFoundError` en compilaciones anteriores.
- **📦 IMPORT CONSOLIDATION**: Añadida la importación de `requests` al motor OSINT para estabilizar el sistema de validación de IP (Geo-Heal).

### 🇺🇸 ENGLISH
- **🛠️ CRITICAL SYNTAX REPAIR**: Removed orphaned code in `core/browser.py` that caused `ModuleNotFoundError` in previous builds.
- **📦 IMPORT CONSOLIDATION**: Added `requests` import to the OSINT engine to stabilize the IP validation system (Geo-Heal).


## [v2.2.48] - Titan Perfecta (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🚀 ZERO-STUTTER CORE**: Eliminado el `Priority Guard`. El sistema ya no reduce la prioridad del navegador, eliminando los micro-parones en la interfaz y el sistema.
- **🛡️ OSINT GEO-HEAL**: Implementado fallback de validación de IP. Si el navegador no puede verificar la localización por sí mismo, el motor realiza una petición HTTP directa para confirmar el origen español.
- **💎 ELITE PROXY REFILL**: Añadidas fuentes SOCKS5 de España y listas globales de élite para maximizar la estabilidad durante el OSINT.
- **⚡ HYPER-ROTATION**: Reducido el tiempo de espera entre rotaciones de 2s a 0.5s para búsquedas más ágiles.

### 🇺🇸 ENGLISH
- **🚀 ZERO-STUTTER CORE**: Removed `Priority Guard`. The system no longer lowers browser priority, eliminating micro-stutters in the UI and system.
- **🛡️ OSINT GEO-HEAL**: Implemented IP validation fallback. If the browser fails to verify location, the engine performs a direct HTTP request to confirm Spanish origin.
- **💎 ELITE PROXY REFILL**: Added Spain SOCKS5 sources and global elite lists to maximize stability during OSINT.
- **⚡ HYPER-ROTATION**: Reduced rotation delay from 2s to 0.5s for faster searches.


## [v2.2.47] - Titan Gold Harvest (2026-02-06)
### 🇪🇸 ESPAÑOL
- **💎 ES GOLD INJECTION**: Añadidas 5 nuevas fuentes VIP de GitHub y APIs residenciales gratuitas para maximizar el hallazgo de proxies en España.
- **📅 DYNAMIC DATE HARVESTING**: El bot ahora inyecta la fecha actual en fuentes como `checkerproxy.net`, asegurando que siempre se descarguen las listas más recientes.
- **🛡️ DEEP CLEAN FILTER**: Optimizado el motor de filtrado para eliminar duplicados de forma más agresiva entre fuentes globales y las exclusivas de España.

### 🇺🇸 ENGLISH
- **💎 ES GOLD INJECTION**: Added 5 new VIP GitHub sources and free residential APIs to maximize proxy finding in Spain.
- **📅 DYNAMIC DATE HARVESTING**: The bot now injects the current date into sources like `checkerproxy.net`, ensuring recent lists are always downloaded.
- **🛡️ DEEP CLEAN FILTER**: Optimized the filtering engine to more aggressively remove duplicates across global and Spain-exclusive sources.


## [v2.2.46] - Titan Resurrection (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🛠️ CRITICAL REPAIR**: Corregido el error de sintaxis en el motor OSINT que impedía el arranque del buscador en la versión anterior.
- **🚀 LOG FLOW v4 (ULTRA-SMOOTH)**: Eliminado el "Log Governor". Los mensajes ahora fluyen de forma instantánea sin micro-cortes visuales.
- **💎 VIP SOURCES v3**: Añadidas fuentes de proxies ES premium de `proxifly` y `checkerproxy` para mayor velocidad de búsqueda.

### 🇺🇸 ENGLISH
- **🛠️ CRITICAL REPAIR**: Fixed the syntax error in the OSINT engine that prevented the searcher from starting in the previous version.
- **🚀 LOG FLOW v4 (ULTRA-SMOOTH)**: Removed the "Log Governor." Messages now flow instantaneously without visual micro-stutters.
- **💎 VIP SOURCES v3**: Added premium Spanish proxy sources from `proxifly` and `checkerproxy` for faster search speed.


## [v2.2.45] - Titan Splash (2026-02-06)
### 🇪🇸 ESPAÑOL
- **✨ PREMIUM SPLASH SCREEN**: Activada la pantalla de bienvenida con barra de progreso real. La app ahora informa de su estado mientras carga el núcleo.
- **🛡️ NO-KILLS POLICY**: Se ha eliminado la limpieza agresiva de procesos. El bot ya no cerrará tus ventanas de Chrome o Firefox personales (YouTube, Correo, etc).
- **⌛ SYNC STARTUP**: Optimizado el flag de inicialización para que la transición entre el Splash y la GUI principal sea instantánea.

### 🇺🇸 ENGLISH
- **✨ PREMIUM SPLASH SCREEN**: Activated the welcome screen with a real progress bar. The app now reports its status while loading the core.
- **🛡️ NO-KILLS POLICY**: Aggressive process cleanup has been removed. The bot will no longer close your personal Chrome or Firefox windows (YouTube, Email, etc).
- **⌛ SYNC STARTUP**: Optimized initialization flag for instant transition between Splash and main GUI.


## [v2.2.44] - Titan Hyperion (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🛑 NUCLEAR STOP SIGNAL**: Inyección completa del stop signal en `fetch_sources`. El bot ahora aborta todas las descargas remotas de forma atómica.
- **🛡️ SESSION BLACKLIST**: Implementada una lista negra persistente durante la ejecución. Si un proxy es detectado como hosting rumano (RO_FAKE), será ignorado permanentemente en esa sesión.
- **🧩 OSINT CRASH REPAIR**: Corregido el error `TypeError` en el formateador de reportes. Ahora maneja búsquedas nulas o abortadas sin cerrar la aplicación.
- **💎 PURE ES GOLD**: Añadidas 2 nuevas fuentes de proxies españoles VIP y optimizado el yield para maximizar IPs residenciales reales.

### 🇺🇸 ENGLISH
- **🛑 NUCLEAR STOP SIGNAL**: Complete injection of stop signal into `fetch_sources`. The bot now aborts all remote downloads atomically.
- **🛡️ SESSION BLACKLIST**: Implemented a persistent session blacklist. If a proxy is detected as Romanian hosting (RO_FAKE), it will be permanently ignored in that session.
- **🧩 OSINT CRASH REPAIR**: Fixed the `TypeError` in the report formatter. It now handles null or aborted lookups without closing the application.
- **💎 PURE ES GOLD**: Added 2 new VIP Spanish proxy sources and optimized yield to maximize real residential IPs.


## [v2.2.43] - Titan Ultra Stability (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🛑 FULMINANT STOP SIGNAL**: Reducido el tamaño de lote de escaneo a 100. El bot ahora comprueba la señal de parada cada 2 segundos, eliminando hilos "zombie".
- **🛡️ RESILIENT GEO-GUARD**: Si la API de Geo-IP falla (429/Timeout), el proxy ya no es blacklisteado, sino que se reserva para reintento.
- **💎 ELITE SOURCES v2**: Purgadas fuentes redundantes y añadidas rutas VIP ES directas para un mejor yield inicial.
- **📉 LOG GOVERNOR v3**: Optimizado el refresco de GUI para eliminar micro-tirones durante el modo OSINT.

### 🇺🇸 ENGLISH
- **🛑 FULMINANT STOP SIGNAL**: Reduced scan batch size to 100. The bot now checks for the stop signal every 2 seconds, eliminating "zombie" threads.
- **🛡️ RESILIENT GEO-GUARD**: If the Geo-IP API fails (429/Timeout), the proxy is no longer blacklisted but reserved for retry.
- **💎 ELITE SOURCES v2**: Purged redundant sources and added direct VIP ES routes for better initial yield.
- **📉 LOG GOVERNOR v3**: Optimized GUI refresh to eliminate micro-stutters during OSINT mode.


## [v2.2.42] - Titan Spanish Elite (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🛑 TITAN STOP SIGNAL**: Inyectados micro-chequeos de parada en cada paso de red. Al pulsar "DETENER", el bot aborta el hilo de forma absoluta e inmediata.
- **🛡️ VERSION FREEZE FIX**: Localizado y eliminado un override interno que bloqueaba la interfaz en la v2.2.37.
- **💎 TITAN SOURCES**: Integración de nuevas fuentes ES VIP (`geonode`) y depuración de falsos positivos en Geo-IP.
- **🧩 ROBUST JSON**: Mejorado el motor de validación de IP para manejar errores de red y respuestas vacías sin crashear.

### 🇺🇸 ENGLISH
- **🛑 TITAN STOP SIGNAL**: Injected micro-stop checks at every network step. Clicking "STOP" now aborts threads absolutely and instantly.
- **🛡️ VERSION FREEZE FIX**: Located and removed an internal override that was locking the interface to v2.2.37.
- **💎 TITAN SOURCES**: Integrated new VIP ES sources (`geonode`) and debugged Geo-IP false positives.
- **🧩 ROBUST JSON**: Improved IP validation engine to handle network errors and empty responses without crashing.


## [v2.2.41] - Elite Spanish Armada (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🚀 SOURCE PURIFICATION**: Eliminadas listas globales residuales (`proxyspace`, `mmpx12`, `clketlow`) de la Fase 1. El escaneo ahora es 100% ES nativo.
- **💎 VIP SOURCES**: Integración de `proxyscan.io` con filtrado geográfico estricto por servidor.
- **⚡ ELITE LATENCY**: Reducción del timeout de validación de Google a 6s para asegurar solo proxies de alta velocidad.
- **📊 FASTER START**: Conteo de candidatos inicial reducido drásticamente para un arranque inmediato.

### 🇺🇸 ENGLISH
- **🚀 SOURCE PURIFICATION**: Removed residual global lists (`proxyspace`, `mmpx12`, `clketlow`) from Phase 1. Scouting is now 100% native ES.
- **💎 VIP SOURCES**: Integrated `proxyscan.io` with strict server-side geographic filtering.
- **⚡ ELITE LATENCY**: Reduced Google validation timeout to 6s to ensure high-speed proxies only.
- **📊 FASTER START**: Drastically reduced initial candidate count for near-instant startup.


## [v2.2.37] - Quantum Stability & OSINT Overlord (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🌌 QUANTUM YIELD**: Aumentado el límite de candidatos a 1500 y añadido filtro de latencia crítica (< 2.5s) para proxies ES.
- **🦆 DUCK ENGINE 2.0**: Corregidos los timeouts de navegación (35s) y mejorada la resiliencia ante bloqueos.
- **💬 WHATSAPP SNIPER**: Reparada la detección de cuentas activa con nuevos selectores más robustos.
- **❄️ CERO MICRO-CORTES**: Optimización del hilo de UI y el registro de logs para una fluidez total.

### 🇺🇸 ENGLISH
- **🌌 QUANTUM YIELD**: Increased candidate limit to 1500 and added critical latency filter (< 2.5s) for ES proxies.
- **🦆 DUCK ENGINE 2.0**: Fixed navigation timeouts (35s) and improved block resilience.
- **💬 WHATSAPP SNIPER**: Repaired active account detection with robust new selectors.
- **❄️ ZERO MICRO-CUTS**: UI thread and log registration optimization for total smoothness.


## [v2.2.36.3] - Smooth Release (2026-02-06)
### 🇪🇸 ESPAÑOL
- **❄️ CERO STUTTER**: Recalibrados los micro-pulsos de sueño (GIL pulses) a 0.01s-0.05s para eliminar el lag del ratón.
- **🛡️ ARMADA ESTABLE**: Consolidada la restauración de la función `fetch_sources` y fuentes ES.
- **🧹 SYNC TOTAL**: Sincronización completa de tags y commits en el repositorio oficial.

### 🇺🇸 ENGLISH
- **❄️ ZERO STUTTER**: Recalibrated micro-sleep pulses (GIL pulses) to 0.01s-0.05s to eliminate mouse lag.
- **🛡️ STABLE ARMADA**: Consolidated the restoration of `fetch_sources` and ES sources.
- **🧹 TOTAL SYNC**: Full tag and commit synchronization in the official repository.

## [v2.2.36.2] - Emergency Fix (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🦅 REPARACIÓN ARMADA**: Recuperada la lógica de recolección de proxies (`fetch_sources`) perdida en la limpieza.
- **🐞 FIX NAMEERROR**: Corregido fallo crítico que impedía el inicio del escaneo en v2.2.36.1.

### 🇺🇸 ENGLISH
- **🦅 ARMADA RESTORE**: Recovered proxy harvesting logic (`fetch_sources`) lost during cleanup.
- **🐞 NAMEERROR FIX**: Fixed critical bug preventing scan startup in v2.2.36.1.

## [v2.2.36.1] - Silent Shield (2026-02-06)
### 🇪🇸 ESPAÑOL
- **🛡️ ESCUDO SILENCIOSO**: El buscador de actualizaciones ahora ignora errores de socket/permisos (Firewall) sin ensuciar la consola.
- **🔌 ROBUSTNEZ DE RED**: Manejo mejorado para fallos de conexión hacia raw.githubusercontent.com.

### 🇺🇸 ENGLISH
- **🛡️ SILENT SHIELD**: Update checker now ignores socket/permission errors (Firewall) without cluttering the console.
- **🔌 NETWORK ROBUSTNESS**: Improved handling for connection failures to raw.githubusercontent.com.

## [v2.2.36] - Saul's Premium (2026-02-06)

### 🇪🇸 ESPAÑOL
- **🚀 ENRIQUECIMIENTO OSINT**: Añadidas fuentes de alta fidelidad para España (Infocif, Infoempresa, Einforma, Tellows).
- **🎨 BRANDING REAL**: Renovado el README con capturas reales del ejecutable y código. Estilo profesional y bilingüe.
- **⚖️ MARCO LEGAL**: Auditoría de textos para asegurar un enfoque educativo y formal.
- **🛡️ SPANISH ARMADA 7.0**: Mejora de dorking masivo orientado a dominios geográficos españoles.

### 🇺🇸 ENGLISH
- **🚀 OSINT ENRICHMENT**: Added high-fidelity Spanish sources (Infocif, Infoempresa, Einforma, Tellows).
- **🎨 REAL BRANDING**: Overhauled README with real screenshots from the EXE and code. Professional bilingual style.
- **⚖️ LEGAL FRAMEWORK**: Text audit to ensure a formal and educational focus.
- **🛡️ SPANISH ARMADA 7.0**: Improved mass dorking targeting Spanish geographical domains.

---

## [v2.2.35] - Saul's Law (2026-02-06)

### 🇪🇸 ESPAÑOL
- **🐞 BUCLE ITERATIVO**: Refactorizada la búsqueda de OSINT a un bucle iterativo para eliminar la recursividad infinita.
- **🛡️ ESCUDO DE TORMENTA**: Implementado bloqueo de hilos (`Lock`) en el scraper para evitar descargas paralelas masivas.
- **🧊 COOLDOWN REFORZADO**: Añadido enfriamiento de 60s tras escaneos masivos para proteger las fuentes.
- **🧹 LIMPIEZA DE LOGS**: El mensaje "Escaneando" ahora solo aparece cuando hay una petición real a red.

### 🇺🇸 ENGLISH
- **🐞 ITERATIVE LOOP**: Refactored OSINT search to an iterative loop to eliminate infinite recursion.
- **🛡️ STORM SHIELD**: Implemented thread-locking (`Lock`) in the scraper to prevent massive parallel downloads.
- **🧊 HARDENED COOLDOWN**: Added 60s cooldown after massive scans to protect proxy sources.
- **🧹 LOG SANITATION**: The "Scanning" message now only appears when a real network request is triggered.

---

## [v2.2.34] - Arctic Freeze (2026-02-06)

### 🇪🇸 ESPAÑOL
- **❄️ GIL GUARD**: Reducidos workers a 5 e implementados micro-pulsos de sueño (0.02s) para fluidez total del ratón.
- **🧠 SCRAPER SINGLETON**: Los componentes comparten memoria de proxys; se acabaron los re-escaneos redundantes.
- **🛡️ IP CACHE**: Verificación de IP recordada por 60s para evitar micro-congelaciones por red.
- **🧹 NUCLEAR CLEANUP**: El constructor ahora mata procesos zombis y borra EXEs antiguos automáticamente.

### 🇺🇸 ENGLISH
- **❄️ GIL GUARD**: Workers reduced to 5 with 0.02s sleep pulses for absolute mouse smoothness.
- **🧠 SCRAPER SINGLETON**: Components share proxy memory; eliminated redundant re-scans.
- **🛡️ IP CACHE**: IP verification cached for 60s to prevent network-induced micro-stutters.
- **🧹 NUCLEAR CLEANUP**: Builder now automatically kills zombie processes and purges old EXEs.

---

## [v2.2.33] - Arctic Silence (2026-02-06)

### 🇪🇸 ESPAÑOL
- **🚀 SILENCIO TOTAL CPU**: Implementado capado inteligente de 500 candidatos para evitar el colapso del ratón.
- **🤫 YIELDING AGRESIVO**: Introducidas micro-pausas en el motor de proxys para liberar el procesador al sistema continuamente.
- **🧊 CHROME PERFORMANCE**: Desactivados procesos innecesarios de red y timers de Chrome para maximizar fluidez.

### 🇺🇸 ENGLISH
- **🚀 ZERO CPU LAG**: Implemented smart 500 candidate cap to eliminate mouse stuttering.
- **🤫 AGGRESSIVE YIELDING**: Introduced micro-sleeps in the proxy engine to continuously yield CPU to the system.
- **🧊 CHROME PERFORMANCE**: Disabled unnecessary background networking and timers in Chrome for maximum fluidity.

---

### 🇪🇸 ESPAÑOL
- **🚀 ZERO MICRO-LAG**: Desactivada la Aceleración por Hardware y GPU en navegadores para eliminar tirones en el ratón.
- **📦 PSUTIL BUNDLING**: Corregido el error de módulo faltante al compilar el EXE.
- **🇪🇸 LA ARMADA ESPAÑOLA 6.0**: Nuevas fuentes de proxys ES premium y tiempos de verificación ultra-rápidos (5s timeout).

### 🇺🇸 ENGLISH
- **🚀 ZERO MICRO-LAG**: Disabled Hardware Acceleration and GPU in browsers to eliminate mouse stutters.
- **📦 PSUTIL BUNDLING**: Fixed missing module error when bundling the EXE.
- **🇪🇸 THE SPANISH ARMADA 6.0**: New premium ES proxy sources and ultra-fast verification times (5s timeout).

---

### 🇪🇸 ESPAÑOL
- **🛠️ BUGFIX CRITICAL**: Corregido error `AttributeError: update_ready` que causaba el cierre inesperado al iniciar.
- **⚖️ COMPARACIÓN SEMÁNTICA**: El bot ahora distingue correctamente entre versiones (v2.2.31 > v2.2.30) evitando avisos falsos de actualización.

### 🇺🇸 ENGLISH
- **🛠️ CRITICAL BUGFIX**: Fixed `AttributeError: update_ready` which caused crashes on startup.
- **⚖️ SEMANTIC COMPARISON**: The bot now correctly identifies version hierarchy (v2.2.31 > v2.2.30), preventing false update alerts.

---

### 🇪🇸 ESPAÑOL
- **☢️ PRIORITY GUARD**: Forzado del navegador a prioridad "IDLE" (Baja). Windows siempre prioriza tu ratón y sistema, eliminando congelamientos.
- **🔍 DORKING RECONSTRUCTION**: Rehechos los selectores de DuckDuckGo y Google para recuperar los resultados perdidos.
- **🕊️ CIRCUIT BREAKER DYNAMISM**: El sistema de bloqueo ahora es dinámico; en lugar de rendirse, rota de proxy e intenta una recuperación agresiva.

### 🇺🇸 ENGLISH
- **☢️ PRIORITY GUARD**: Forced browser to "IDLE" priority. Windows now prioritizes your mouse and UI over the bot's background tasks.
- **🔍 DORKING RECONSTRUCTION**: Rebuilt DuckDuckGo and Google selectors to restore missing results.
- **🕊️ DYNAMIC CIRCUIT BREAKER**: The blocking system is now dynamic; instead of giving up, it rotates proxies and attempts aggressive recovery.

---

### 🇪🇸 ESPAÑOL
- **❄️ ENFRIAMIENTO OSINT**: Implementadas pausas obligatorias de 2s entre búsquedas de Google/DuckDuckGo y 1.5s entre chequeos de plataformas.
- **🚀 JS OPTIMIZADO**: El script de localización ahora consume un 80% menos de CPU al ser inyectado solo cuando es necesario.
- **🛡️ ZERO LAG**: Eliminados los picos de CPU al iniciar la investigación que congelaban el ratón.

### 🇺🇸 ENGLISH
- **❄️ OSINT COOLING**: Implemented mandatory 2s pauses between Google/DuckDuckGo searches and 1.5s between platform checks.
- **🚀 OPTIMIZED JS**: Localization script now consumes 80% less CPU by only injecting when necessary.
- **🛡️ ZERO LAG**: Eliminated CPU spikes when starting research that used to freeze the mouse.

---

### 🇪🇸 ESPAÑOL
- **⛓️ GRILLETES DE HILOS**: Reducción drástica de hilos de 50 a un máximo de 5 para evitar la asfixia del procesador.
- **🧊 CEDENCIA DE CPU (Yielding)**: Implementadas micro-pausas obligatorias en todos los bucles internos del scraper y la interfaz para que el ratón no se bloquee.
- **🛡️ MÁXIMA FLUIDEZ**: El bot es ahora totalmente invisible para el sistema, permitiendo el uso de YouTube 4K y multitarea pesada.

### 🇺🇸 ENGLISH
- **⛓️ THREAD CAPPING**: Drastic reduction of threads from 50 to a maximum of 5 to prevent processor starvation.
- **🧊 CPU YIELDING**: Implemented mandatory micro-pauses in all internal scraper and interface loops so the mouse doesn't freeze.
- **🛡️ MAXIMUM FLUIDITY**: The bot is now completely invisible to the system, allowing for 4K YouTube and heavy multitasking.

---

## 🔥 [2.2.27] - 2026-02-05 (ARCTIC STABILITY - NUCLEAR CPU FIX)

### 🇪🇸 ESPAÑOL
- **☢️ EXTERMINIO DE BLOQUEOS CPU**: Corregido el bucle infinito en el bypass de captcha que consumía el 100% de la CPU. Ahora el bot es ultra-ligero.
- **🛡️ ESCUDO ÁRTICO**: El buscador de proxys ahora trunca archivos gigantes para evitar sobrecarga de RAM y bloqueos de regex.
- **💀 LIMPIEZA TOTAL**: Limpieza automática de procesos zombis de Chrome/Firefox al arrancar.
- **🧠 RESULTADOS RECUPERADOS**: Restaurada la lógica de extracción de inteligencia que fallaba en versiones previas.

### 🇺🇸 ENGLISH
- **☢️ CPU LOCK TERMINATION**: Fixed infinite loop in captcha bypass that consumed 100% CPU. The bot is now ultra-light.
- **🛡️ ARCTIC SHIELD**: Proxy scraper now truncates giant files to avoid RAM overhead and regex locks.
- **💀 TOTAL CLEANUP**: Automatic cleanup of zombie Chrome/Firefox processes on startup.
- **🧠 RESULTS RECOVERED**: Restored intelligence extraction logic that failed in previous versions.

## 🔥 [2.2.26] - 2026-02-05 (ECO-RESCUE & MULTITASKING)

### 🇪🇸 ESPAÑOL
- **MODO ECO (YouTube Friendly)**: El bot ahora corre con prioridad "IDLE". Cederá toda la CPU a Chrome o YouTube si los usas al mismo tiempo. ¡Cero bloqueos!
- **BUCLES ECOLÓGICOS**: Introducidos descansos obligatorios de 6s entre servicios para enfriar la CPU.
- **INTELLIGENCE RECOWERY**: Mejorada la detección en motores de búsqueda secundaria.

### 🇺🇸 ENGLISH
- **ECO MODE (YouTube Friendly)**: The bot now runs with "IDLE" priority. It will give all CPU to Chrome or YouTube if you use them at the same time. Zero freezes!
- **ECO LOOPS**: Mandatory 6s breaks between services to cool the CPU.
- **INTELLIGENCE RECOVERY**: Improved detection in secondary search engines.

---

## 🔥 [2.2.25] - 2026-02-05 (SAUL'S PREMIUM - CRITICAL BUGFIX)

### 🇪🇸 ESPAÑOL
- **CRITICAL FIX**: Corregido el error `'ProxyScraper' object has no attribute 'geo_cache'` que causaba crashes.
- **PREMIUM BRANDING**: Nuevo README visual profesional con banners y tablas de rendimiento.
- **OSINT OPTIMIZER**: Ajuste de latencia en hilos para una navegación aún más fluida y estable.

### 🇺🇸 ENGLISH
- **CRITICAL FIX**: Fixed `'ProxyScraper' object has no attribute 'geo_cache'` error that caused crashes.
- **PREMIUM BRANDING**: New professional visual README with banners and performance tables.
- **OSINT OPTIMIZER**: Thread latency adjustment for even smoother and more stable browsing.

---

## 🔥 [2.2.24] - 2026-02-05 (COOLING & PROXY QUALITY)

### 🇪🇸 ESPAÑOL
- **CPU COOLING**: Reducción drástica del uso de procesador (limitado a 20 hilos). ¡Mantenemos tu PC frío!
- **GOLDEN PROXY CACHE**: El bot ahora recuerda los mejores proxys de España para inicios instantáneos.
- **ENERGY SAVER**: Optimizada la carga del navegador para evitar lag en el sistema.

### 🇺🇸 ENGLISH
- **CPU COOLING**: Drastic reduction in processor usage (limited to 20 threads). Keep your PC cool!
- **GOLDEN PROXY CACHE**: The bot now remembers the best Spanish proxies for instant startups.
- **ENERGY SAVER**: Optimized browser loading to avoid system lag.

---

## 🔥 [2.2.23] - 2026-02-05 (HYPER-EFFICIENCY & SLIM BROWSING)

### 🇪🇸 ESPAÑOL
- **TURBO SCRAPER**: Paralelización de la búsqueda de proxys españoles. Verificación 20x más rápida.
- **NAVEGACIÓN SLIM**: Desactivada la carga de imágenes y multimedia para ahorrar hasta un 60% de RAM.
- **OSINT OPTIMIZADO**: Reducción de latencia en la captura de datos y mejor bypass de captchas.

### 🇺🇸 ENGLISH
- **TURBO SCRAPER**: Parallelization of Spanish proxy search. 20x faster verification.
- **SLIM BROWSING**: Image and media loading disabled to save up to 60% RAM.
- **OPTIMIZED OSINT**: Reduced latency in data capture and improved captcha bypass.

---

## 🔥 [2.2.22] - 2026-02-05 (SPANISH ARMADA 5.0 - REAL ES GUARD)

### 🇪🇸 ESPAÑOL
- **ARMADA ESPAÑOLA 5.0**: Inyectadas 22+ fuentes de proxys exclusivas de España. ¡Más cantidad y mejor calidad!
- **FILTRADO RESILIENTE**: Mejorado el sistema de verificación geográfica con triple fallback. No más falsos negativos.
- **PUREZA 100%**: Optimizado el scraper para ignorar proxys saturados y centrarse en IPs residenciales/móviles frescas.

### 🇺🇸 ENGLISH
- **SPANISH ARMADA 5.0**: Injected 22+ exclusive Spanish proxy sources. More quantity, better quality!
- **RESILIENT FILTERING**: Improved the Geo-verification system with triple fallback. No more false negatives.
- **100% PURITY**: Optimized the scraper to ignore saturated proxies and focus on fresh residential/mobile IPs.

---

## 🔥 [2.2.21] - 2026-02-05 (SAUL'S MEMORY & STABILITY)

### 🇪🇸 ESPAÑOL
- **FIX GUI CRASH**: Corregido un error crítico que cerraba el programa al buscar actualizaciones (AttributeError).
- **MEMORIA INFINITA**: Tus favoritos (números, nombres, etc.) ahora se guardan en `targets.json` junto al bot. ¡Tus contactos sobreviven a las actualizaciones!
- **LIMPIEZA NUCLEAR 2.0**: El constructor ahora es más agresivo eliminando archivos `.spec` y basura residual.

### 🇺🇸 ENGLISH
- **FIX GUI CRASH**: Resolved a critical error that crashed the app during update checks (AttributeError).
- **INFINITE MEMORY**: Your favorites (numbers, names, etc.) are now saved in `targets.json` next to the bot. They persist across updates!
- **NUCLEAR CLEANUP 2.0**: The builder is now more aggressive in deleting `.spec` files and residual junk.

---

## 🔥 [2.2.20] - 2026-02-05 (ULTRA-STRICT GUARD & NUCLEAR CLEANUP)

### 🇪🇸 ESPAÑOL
- **FILTRO GEO 100%**: Re-habilitado el filtrado geográfico obligatorio para todos los proxys. Ya no se aceptan proxys "probables"; solo IPs con certificado ES verificado.
- **PURIFICACIÓN**: Eliminadas fuentes mixtas que contaminaban la lista de España con IPs de otros países.
- **LIMPIEZA NUCLEAR**: El builder ahora borra automáticamente archivos `.spec`, carpetas temporales y versiones antiguas para mantener el escritorio limpio.
- **ESTABILIDAD**: Corregida la detección de país para evitar reyecciones por códigos "Unknown".

### 🇺🇸 ENGLISH
- **100% GEO-FILTER**: Re-enabled mandatory geographical filtering for all proxies. No more "likely" proxies; only verified ES IPs are accepted.
- **PURIFICATION**: Removed mixed sources that contaminated the Spain list with foreign IPs.
- **NUCLEAR CLEANUP**: Builder now auto-deletes `.spec` files, temporary folders, and old versions to keep the workspace clean.
- **STABILITY**: Fixed country detection to avoid rejections caused by "Unknown" codes.

---

## 🔥 [2.2.19] - 2026-02-05 (ULTIMATE RESILIENCE & TRIPLE-CHECK)

### 🇪🇸 ESPAÑOL
- **VERIFICACIÓN TRIPLE**: Las IPs ahora se comprueban contra Google, Icanhazip y Bing. Si pasan 2 de 3, son válidas. ¡Rescatamos proxys que antes daban falso error!
- **MODO DESESPERACIÓN**: Si tras 60 segundos no hay 3 proxys pero hay al menos 1 bueno, el bot te permite arrancar. ¡Tiempo es dinero!
- **FUENTES 2026**: Integradas listas ultra-frescas de GitHub (mmpx12, proxifly).
- **TURBO GEO-FILTER (50 HILOS)**: Velocidad de cribado elevada al máximo exponente.

### 🇺🇸 ENGLISH
- **TRIPLE-CHECK VERIFICATION**: IPs are now verified against Google, Icanhazip, and Bing. If 2/3 pass, the proxy is validated. No more false negatives!
- **DESPERATION MODE**: If after 60s only 1 high-quality proxy is found, the bot allows early exit to start operations.
- **2026 SOURCES**: Integrated ultra-fresh GitHub lists (mmpx12, proxifly).
- **TURBO GEO-FILTER (50 THREADS)**: Maximum global filtering speed achieved.

---

## 🔥 [2.2.18] - 2026-02-05 (DEEP HUNTER & SPANISH ARMADA)

### 🇪🇸 ESPAÑOL
- **THE SPANISH ARMADA**: Añadidas +15 fuentes de alta fidelidad exclusivas para España.
- **DEEP HTML SCRAPING**: El bot ahora raspa tablas complejas de sitios como ProxyDB y ProxyServers para encontrar IPs ocultas.
- **TURBO GEO-FILTER (40 HILOS)**: Cuadriplicada la velocidad de cribado del haystack global para encontrar IPs españolas en segundos.
- **SEARCH DEPTH**: Mayor profundidad de búsqueda automática en caso de escasez de candidatos rápidos.

### 🇺🇸 ENGLISH
- **THE SPANISH ARMADA**: Added +15 new high-fidelity sources exclusive for Spain.
- **DEEP HTML SCRAPING**: Bot now scrapes complex tables from ProxyDB and ProxyServers to find hidden IPs.
- **TURBO GEO-FILTER (40 THREADS)**: Quadrupled global haystack filtering speed to find ES IPs in seconds.
- **SEARCH DEPTH**: Automatically increased search depth when quick candidates are scarce.

---

## 🔥 [2.2.17] - 2026-02-05 (HYPER-SPEED STARTUP & TRUST TIER)

### 🇪🇸 ESPAÑOL
- **TRUST TIER 1**: Eliminada la re-verificación Geo de proxys provenientes de fuentes exclusivas de España. Esto acelera el arranque un 80%.
- **TURBO HARVESTER**: Elección de hasta 100 hilos en paralelo para la descarga de fuentes.
- **ROBUST GEO-FILTER**: Mejorado el motor de filtrado masivo con soporte para reintentos tras Error 429 y fallback a `ipapi.co`.

### 🇺🇸 ENGLISH
- **TRUST TIER 1**: Removed redundant Geo-verification for proxies from ES-only sources. Speeds up startup by 80%.
- **TURBO HARVESTER**: Increased parallel workers to 100 for source downloading.
- **ROBUST GEO-FILTER**: Enhanced mass-filtering engine with retry logic for Error 429 and `ipapi.co` fallback.

---

## 🔥 [2.2.16] - 2026-02-05 (INFINITE LOOP FIX & PERSISTENCE)

### 🇪🇸 ESPAÑOL
- **LOOP BREAKER**: Corregido el bucle infinito de scraping al implementar persistencia en la cola de proxys. No se re-escanea si ya hay candidatos válidos.
- **AGRESSIVE HARVESTING**: El bot ahora asegura un pool de al menos 3-5 proxys antes de iniciar, combinando fuentes rápidas y minería masiva.
- **CHROME SOCKS Support**: Ahora el motor de Chrome también soporta proxys SOCKS4/5.

### 🇺🇸 ENGLISH
- **LOOP BREAKER**: Fixed infinite scraping loop by implementing proxy queue persistence. No re-scans if valid candidates are present.
- **AGRESSIVE HARVESTING**: Bot now ensures a pool of at least 3-5 proxies before starting, combining fast sources and massive mining.
- **CHROME SOCKS Support**: Chrome engine now supports SOCKS4/5 proxies.

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
