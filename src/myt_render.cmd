@echo off
:: Call `myt_renderHarmonyScenes` using mayapy if Python is not available

SETLOCAL
set /A MAYA_VER=2023
set "mayapy=C:\Program Files\Autodesk\Maya%MAYA_VER%\bin\mayapy"
ENDLOCAL

"%mayapy%" "%~dp0\myt_renderHarmonyScenes" "%*"
