@echo off

:: Define python exe path
set PYTHON_EXE_PATH="C:\Users\Administrator\PycharmProjects\manager\venv\Scripts\python.exe"

:: Define python script path
set SCRIPT_PATH="G:\Stock\pairs_trade\pair_trade"

if exist "%PYTHON_EXE_PATH%" goto :start
echo Please edit the BAT file and change the value of PYTHON_EXE_PATH 
goto :end

if exist "%SCRIPT_PATH%" goto :start
echo Please edit the BAT file and change the value of SCRIPT_PATH
goto :end

:start
echo progrom start!

cd %SCRIPT_PATH%"
%PYTHON_EXE_PATH% %SCRIPT_PATH%\Sayatori_Main.py

:end
echo progrom end! 
exit /b