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
if exist "python.exe" del /f /q "python.exe"
if exist "WannaCall_Update.exe" del /f /q "WannaCall_Update.exe"
if exist "WannaCall_Pro.exe" del /f /q "WannaCall_Pro.exe"
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

echo [3/7] Actualizando desde GitHub...
git fetch --all
git reset --hard origin/main
git pull origin main

echo [4/7] Instalando librerias necesarias...
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
py -3 -u gui.py
if %errorlevel% neq 0 python -u gui.py

echo.
echo ===================================================
echo    REPARACION COMPLETADA.
echo ===================================================
pause
