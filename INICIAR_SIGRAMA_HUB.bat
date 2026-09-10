@echo off
title SIGRAMA - Concentrador de Aplicaciones (Hub)
color 0B
echo =======================================================================
echo          SIGRAMA - PORTAL CONCENTRADOR DE APLICACIONES (ODOO STYLE)
echo =======================================================================
echo.
echo [INFO] Iniciando el servidor del Concentrador SIGRAMA en el puerto 8080...
echo [INFO] Presione Ctrl+C en esta ventana si desea detener el portal.
echo.

cd /d "%~dp0"

:: Abrir navegador en 2 segundos en segundo plano
start "" powershell -WindowStyle Hidden -Command "Start-Sleep -Seconds 2; Start-Process http://localhost:8080"

:: Iniciar servidor Flask con Python
py server.py
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ADVERTENCIA] Fallo al iniciar con 'py'. Probando con 'python'...
    python server.py
)

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] No se pudo iniciar el servidor.
    echo Verifique que Python y Flask esten instalados ejecutando:
    echo pip install flask psutil
    echo.
    pause
)
