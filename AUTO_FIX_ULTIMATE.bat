@echo off
title WANNA CALL - REPARACION TOTAL v2.2.6
echo ===================================================
echo    REPARACION TOTAL - ELIMINANDO VERSIONES VIEJAS
echo ===================================================
echo.
echo [1/6] Cerrando procesos antiguos...
taskkill /f /im WannaCall* /t 2>nul
taskkill /f /im Perubian* /t 2>nul
taskkill /f /im python.exe /t 2>nul
echo.

echo [2/6] Eliminando basura antigua...
if exist "python.exe" del /f /q "python.exe"
if exist "WannaCall_Update.exe" del /f /q "WannaCall_Update.exe"
if exist "WannaCall_Pro.exe" del /f /q "WannaCall_Pro.exe"
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

echo [3/6] Actualizando desde GitHub...
git fetch --all
git reset --hard origin/main
git pull origin main

echo [4/6] Limpiando cache...
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "core\__pycache__" rmdir /s /q "core\__pycache__"
if exist "services\__pycache__" rmdir /s /q "services\__pycache__"

echo [5/6] Verificando version...
if exist "version.txt" type version.txt
echo.

echo [6/6] LANZANDO VERSION v2.2.6 - BOTON VERDE
echo Si se cierra la ventana, es que falta instalar Python 3.12.
echo.
py -3 -u gui.py
if %errorlevel% neq 0 python -u gui.py

echo.
echo ===================================================
echo    REPARACION COMPLETADA.
echo ===================================================
pause
