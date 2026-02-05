@echo off
title PerubianBot - Manual Build Shield
echo ===================================================
echo    SHIELDED BUILD SYSTEM - MANUAL FALLBACK
echo ===================================================
echo.
echo ℹ️ Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python no esta en el PATH.
    pause
    exit /b 1
)

echo ℹ️ Iniciando build_pro.py...
python -u build_pro.py
echo.
echo ===================================================
if %errorlevel% equ 0 (
    echo ✅ PROCESO FINALIZADO CON EXITO.
    echo 📂 Revisa la carpeta 'dist' para tu EXE.
) else (
    echo ❌ EL PROCESO FALLO CON CODIGO %errorlevel%.
    echo 📄 Revisa build_log.txt para mas detalles.
)
echo ===================================================
pause
