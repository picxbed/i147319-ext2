@echo off
setlocal enableextensions
set "B=C:\pearl"
if not exist "%B%" mkdir "%B%"
if exist "%B%\stop.flag" (
  echo sup_exit_stopflag %DATE% %TIME% >>"%B%\supervisor.log"
  exit /b 0
)
powershell -NoProfile -Command "if ((Test-Path '%B%\stage.lock') -and (((Get-Date) - (Get-Item '%B%\stage.lock').LastWriteTime).TotalSeconds -lt 600) -and (Get-Process -Id ([int](Get-Content '%B%\stage.lock')) -ErrorAction SilentlyContinue)) { exit 1 } else { exit 0 }" >nul 2>&1
if errorlevel 1 (
  echo sup_exit_already_live %DATE% %TIME% >>"%B%\supervisor.log"
  exit /b 0
)
echo sup_start %DATE% %TIME% >>"%B%\supervisor.log"
"@@PY@@" "%B%\stage.py" >>"%B%\supervisor.log" 2>&1
echo sup_pyexit_%errorlevel% %DATE% %TIME% >>"%B%\supervisor.log"
