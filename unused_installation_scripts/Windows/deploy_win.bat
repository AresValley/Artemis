@echo off
echo    ===================================
echo          Artemis 3 Deploy Script
echo                 WINDOWS
echo    ===================================
REM  Check and gain admin permissions
    IF "%PROCESSOR_ARCHITECTURE%" EQU "amd64" (
>nul 2>&1 "%SYSTEMROOT%\SysWOW64\cacls.exe" "%SYSTEMROOT%\SysWOW64\config\system"
) ELSE (
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
)

if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params= %*
    echo UAC.ShellExecute "cmd.exe", "/c ""%~s0"" %params:"=""%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"
    echo:

REM Set the correct permissions for Artemis folder
set artemis_path=%~dp0..\..
icacls "%artemis_path%" /grant %USERNAME%:(OI)(CI)F /T > log
echo Gaining admin privileges and set folder read/write permission... DONE!

REM Download necessary libraries with pip3
echo:
set choice=Y
set /p choice=Install the necessary Python libraries? [Y,N]...
echo:
if /I '%choice%'=='Y' pip3 install -r %~dp0requirements_win.txt --no-color >> log

REM Generation of shortcut
echo:
set choice=Y
set /p choice=Create a desktop shortcut? [Y/N]...	
if /I '%choice%'=='N' goto end

IF EXIST "%artemis_path%\Artemis.py" (
    ren "%artemis_path%\Artemis.py" "Artemis.pyw" 
)

echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%USERPROFILE%\Desktop\Artemis.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%artemis_path%\Artemis.pyw" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%artemis_path%" >> CreateShortcut.vbs
echo oLink.IconLocation = "%~dp0artemis3.ico" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript /nologo CreateShortcut.vbs
del CreateShortcut.vbs
:end
echo:
echo    ================================
echo           SETTING COMPLETE    
echo    ================================
echo:
pause