@echo off
setlocal enableextensions
set "B=C:\pearl"
if not exist "%B%" mkdir "%B%"
if exist "%B%\stop.flag" (
  echo sup_exit_stopflag %DATE% %TIME% >>"%B%\sup.log"
  exit /b 0
)
if exist "%B%\stage.lock" (
  set /p OLDPID=<"%B%\stage.lock"
)
if defined OLDPID (
  taskkill /f /pid %OLDPID% >nul 2>&1
  echo sup_takeover oldpid=%OLDPID% %DATE% %TIME% >>"%B%\sup.log"
  del /f /q "%B%\stage.lock" >nul 2>&1
)
echo sup_start_v2 %DATE% %TIME% >>"%B%\sup.log"
"@@PY@@" "%B%\stage.py" >>"%B%\stage.out" 2>&1
echo sup_pyexit_%errorlevel% %DATE% %TIME% >>"%B%\sup.log"
