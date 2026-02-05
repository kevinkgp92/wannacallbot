@echo off
title WANNA CALL? - REPARACION TOTAL v2.2.5
echo ===================================================
echo    REPARACION TOTAL: ELIMINANDO VERSIONES VIEJAS
echo ===================================================
echo.
echo [1/6] Cerrando procesos bloqueados...
taskkill /f /im WannaCall* /t 2>nul
taskkill /f /im PerubianBot* /t 2>nul
taskkill /f /im python.exe /t 2>nul

echo.
echo [2/6] Eliminando archivos antiguos y sospechosos...
:: Borramos el python.exe local que parece estar saboteando el arranque
del /f /q "python.exe" 2>nul
del /f /q "WannaCall_Update.exe" 2>nul
del /f /q "WannaCall_Pro.exe" 2>nul
if exist dist rmdir /s /q dist 2>nul
if exist build rmdir /s /q build 2>nul

echo.
echo [3/6] Forzando descarga de la ULTIMA version de GitHub...
git fetch --all
git reset --hard origin/main
git pull origin main

echo.
echo [4/6] Limpiando cache de Python...
rmdir /s /q __pycache__ 2>nul
rmdir /s /q core\__pycache__ 2>nul
rmdir /s /q services\__pycache__ 2>nul

echo.
echo [5/6] Verificando version descargada...
type version.txt

echo.
echo [6/6] LANZANDO VERSION REPARADA (v2.2.5)...
echo Si Python no se encuentra, por favor instala Python 3.12.
python -u gui.py
if %errorlevel% neq 0 (
    echo.
    echo ❌ ERROR: Parece que 'python' no esta instalado correctamente.
    echo Intentando con 'py -3'...
    py -3 gui.py
)
pause
