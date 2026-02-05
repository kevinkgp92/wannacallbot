@echo off
title Wanna Call? - Rescue System
echo ===================================================
echo    RESCUE SYSTEM: ACTIVATING WANNA CALL?
echo ===================================================
echo.
echo [1/3] Verificando entorno...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python no esta instalado o no esta en el PATH.
    echo Por favor, instala Python 3.12 y marca 'Add to PATH'.
    pause
    exit /b 1
)

echo [2/3] Limpiando residuos antiguos...
if exist dist\PerubianBot_Ultimate.exe (
    echo ℹ️ Borrando ejecutable antiguo para evitar confusiones...
    del /f /q "dist\PerubianBot_Ultimate.exe" >nul 2>&1
)

echo [3/3] LANZANDO VERSION FUENTE (Wanna Call?)...
echo.
echo ℹ️ IMPORTANTE: Cuando se abra el bot, veras el nuevo banner.
echo ℹ️ Pulsa 'GENERAR INSTALADOR EXE' para crear tu nueva version.
echo.
python gui.py
pause
