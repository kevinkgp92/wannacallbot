---
description: Proceso obligatorio para cada nueva versión de PerubianBot (Ritual de Lanzamiento)
---

Este workflow DEBE seguirse estrictamente en cada actualización de versión:

### 1. Sincronización de Versiones
- Actualizar `version.txt` con la nueva versión (ej: `2.2.50`).
- Actualizar la variable `self.version` en `gui.py`.
- Actualizar la variable `version` en `build_exe.py`.
- Actualizar `self.local_version` en `core/updater.py`.

### 2. Documentación
- Añadir entrada en `CHANGELOG.md` con los cambios en Español e Inglés.
- Actualizar `walkthrough.md` en la carpeta de brain con el resumen de la versión.
- Marcar tareas completadas en `task.md`.

### 3. Construcción (EXE)
- Ejecutar `python build_exe.py`.
- Verificar que se genera el archivo `WannaCall_vX.X.XX_PORTABLE.exe`.

### 4. Ritual Git Final
// turbo
1. `git add .`
2. `git commit -m "Nombre_Release vX.X.XX: Resumen rápido"`
3. `git tag vX.X.XX`
4. `git push origin main --force --tags`

### 5. Limpieza
- Eliminar carpetas `build_*` y `dist_*`.
- Eliminar archivos `.spec` y `.log`.
- Matar procesos `chromedriver.exe` y `geckodriver.exe`.
