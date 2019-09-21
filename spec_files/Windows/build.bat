ECHO OFF
ECHO Building Artemis executable...
RMDIR /s /q output
MKDIR output
CALL pyinstaller artemis.spec
ECHO Remove directories
MOVE dist\Artemis.exe .\output\Artemis.exe
RMDIR /s /q dist
RMDIR /s /q build
ECHO *************
ECHO *************
ECHO Building updater...
CALL pyinstaller updater.spec
ECHO Remove directories
MOVE dist\_ArtemisUpdater.exe .\output\_ArtemisUpdater.exe
RMDIR /s /q dist
RMDIR /s /q build
CD output
ECHO "Compress files themes+Artemis.exe -> Artemis.zip"
CALL "C:\Program Files\7-Zip\7z.exe" a -r Artemis_win.zip Artemis.exe ..\..\..\src\themes
CALL "C:\Program Files\7-Zip\7z.exe" a _ArtemisUpdater_win.zip _ArtemisUpdater.exe
ECHO "Compress all files for website download"
MKDIR Artemis
XCOPY /y Artemis.exe Artemis\
XCOPY /e /k /y ..\..\..\src\themes Artemis\themes\ /EXCLUDE:..\excluded_files.txt
XCOPY /y _ArtemisUpdater.exe Artemis\
CALL "C:\Program Files\7-Zip\7z.exe" a ArtemisWebsite_win.zip Artemis\
CALL python ..\..\__get_hash_code.py Artemis_win.zip _ArtemisUpdater_win.zip ArtemisWebsite_win.zip
CD ..
ECHO Done.