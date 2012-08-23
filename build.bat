:: Folder preperation and old cleanup.
cd D:\Jordan\Programming\Python\Projects\Renamer
rmdir dist /S /Q

:: Build the exe.
set PIP=C:\Python27\pyinstaller\
python %PIP%Makespec.py --upx --tk -w src/renamer.py
python %PIP%Build.py renamer.spec

:: Cleanup extra unnecessary files.
ECHO Y | DEL warnrenamer.txt
ECHO Y | DEL tk.pkg
ECHO Y | DEL *.log
ECHO Y | DEL renamer.spec
ECHO Y | DEL dist\renamer\*.manifest
rmdir dist\renamer\_MEI /S /Q
rmdir build /S /Q

:: Make the files and directories look nicer.
ren dist\renamer\renamer.exe Renamer.exe
copy readme.txt dist\renamer
ren dist\renamer Renamer

:: Create a RAR file to distribute.
cd D:\Jordan\Programming\Python\Projects\Renamer\dist\
D:\Programs\Applications\WinRAR\Rar.exe a D:\Jordan\Programming\Python\Projects\Renamer\dist\Renamer.rar -m5 -r
