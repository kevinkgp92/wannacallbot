@echo off
title WANNA CALL - REPARACION TOTAL v2.2.6
echo ===================================================
echo    REPARACION TOTAL - ELIMINANDO VERSIONES VIEJAS
echo ===================================================
echo.
echo [1/7] Cerrando procesos antiguos...
taskkill /f /im WannaCall* /t 2>nul
taskkill /f /im Perubian* /t 2>nul
taskkill /f /im python.exe /t 2>nul
echo.

echo [2/7] Eliminando basura antigua...
:: Intentamos borrar o renombrar archivos sospechosos
if exist "python.exe" del /f /q "python.exe" 2>nul
if exist "python.exe" ren "python.exe" "python.exe.OLD" 2>nul
if exist "WannaCall_Update.exe" del /f /q "WannaCall_Update.exe" 2>nul
if exist "WannaCall_Update.exe" ren "WannaCall_Update.exe" "WannaCall_Update.OLD" 2>nul
if exist "dist" rmdir /s /q "dist" 2>nul
if exist "build" rmdir /s /q "build" 2>nul

echo [3/7] Actualizando desde GitHub...
git fetch --all
git reset --hard origin/main
git pull origin main

echo [4/7] Instalando librerias necesarias...
:: Usamos python -m pip para maxima compatibilidad
python -m pip install -r requirements.txt --user --quiet
echo.

echo [5/7] Limpiando cache...
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "core\__pycache__" rmdir /s /q "core\__pycache__"
if exist "services\__pycache__" rmdir /s /q "services\__pycache__"

echo [6/7] Verificando version...
if exist "version.txt" type version.txt
echo.

echo [7/7] LANZANDO VERSION v2.2.6 - BOTON VERDE
echo.
:: El lanzador py -3 es el mas fiable en Windows
py -3 -u gui.py
if %errorlevel% neq 0 python -u gui.py

echo.
echo ===================================================
echo    REPARACION COMPLETADA CON EXITO.
echo ===================================================
pause
