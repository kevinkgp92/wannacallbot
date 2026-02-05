@echo off
title WANNA CALL? - AUTO-REPAIR v2.2.5 [NUCLEAR]
echo ===================================================
echo    WANNA CALL? - REPARACION Y ACTUALIZACION
echo ===================================================
echo.
echo [1/5] Cerrando procesos antiguos...
taskkill /f /im WannaCall* /t 2>nul
taskkill /f /im PerubianBot* /t 2>nul
taskkill /f /im python.exe /t 2>nul

echo.
echo [2/5] Eliminando versiones compiladas antiguas para evitar confusion...
ren "WannaCall_Update.exe" "OLD_WannaCall.exe.bak" 2>nul
ren "dist\PerubianBot_Ultimate.exe" "OLD_Perubian.exe.bak" 2>nul

echo.
echo [3/5] Forzando descarga de la ULTIMA VERSION (v2.2.5)...
git fetch --all
git reset --hard origin/main
git pull origin main

echo.
echo [4/5] Limpiando residuos...
rmdir /s /q __pycache__ 2>nul
rmdir /s /q core\__pycache__ 2>nul
rmdir /s /q services\__pycache__ 2>nul
del /f /q DEBUG_BOOT.txt 2>nul

echo.
echo [5/5] INICIANDO VERSION REPARADA (v2.2.5)...
echo.
python gui.py
pause
