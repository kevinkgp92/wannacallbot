@echo off
title REPARANDO DEPENDENCIAS...
color 0E

echo ---------------------------------------------------
echo    REPARANDO LIBRERIAS FALTANTES (PYTHON 3.11)
echo ---------------------------------------------------
"C:\Users\kevin\AppData\Local\Programs\Python\Python311\python.exe" tools\install_deps.py

echo.
echo ---------------------------------------------------
echo    REPARACION COMPLETADA
echo ---------------------------------------------------
echo Ahora vuelve a ejecutar GOD_MODE_UPLOAD.bat
pause
