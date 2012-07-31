cd D:\Jordan\Programming\Python\Projects\Renamer
rmdir dist /S /Q

set PIP=C:\Python27\pyinstaller\
python %PIP%Makespec.py --onefile --upx --tk -w renamer.py
python %PIP%Build.py renamer.spec

ECHO Y | DEL warnrenamer.txt
ECHO Y | DEL tk.pkg
ECHO Y | DEL *.log
ECHO Y | DEL renamer.spec
rmdir build /S /Q

ren dist\renamer.exe Renamer.exe
copy readme.txt dist