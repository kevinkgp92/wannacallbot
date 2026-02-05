@echo off
title WANNA CALL? - REPARACION TOTAL v2.2.6
echo ===================================================
echo    REPARACION TOTAL: ELIMINANDO VERSIONES VIEJAS
echo ===================================================
echo.
echo [1/6] Cerrando TODOS los procesos del bot...
taskkill /f /im WannaCall* /t 2>nul
taskkill /f /im Perubian* /t 2>nul
taskkill /f /im python.exe /t 2>nul
timeout /t 2 /nobreak >nul

echo.
echo [2/6] Eliminando archivos que causan confusion...
:: Borramos el python.exe local que pesa 103MB (es el bot viejo camuflado)
if exist "python.exe" (
    echo ℹ️ Detectado python.exe falso (bot antiguo). Eliminando...
    del /f /q "python.exe"
)
del /f /q "WannaCall_Update.exe" 2>nul
del /f /q "WannaCall_Pro.exe" 2>nul
if exist dist rmdir /s /q dist 2>nul
if exist build rmdir /s /q build 2>nul

echo.
echo [3/6] Descargando codigo real v2.2.6 desde GitHub...
git fetch --all
git reset --hard origin/main
git pull origin main

echo.
echo [4/6] Limpiando cache persistente...
rmdir /s /q __pycache__ 2>nul
rmdir /s /q core\__pycache__ 2>nul
rmdir /s /q services\__pycache__ 2>nul

echo.
echo [5/6] Verificando version...
type version.txt

echo.
echo [6/6] LANZANDO VERSION v2.2.6 (USANDO PYTHON DEL SISTEMA)...
echo.
echo ℹ️ Si se abre el viejo, es que tu 'python' aun apunta al archivo antiguo.
echo.
:: Intentamos usar el lanzador oficial de Windows primero
py -3 -u gui.py
if %errorlevel% neq 0 (
    python -u gui.py
)
pause
