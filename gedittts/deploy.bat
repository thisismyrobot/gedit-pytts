:: This is working on Win7 64bit, try at own risk
:: Oh, and because of all sorts of reasons, this must be ran as administrator...

@echo off

taskkill /F /IM gedit.exe

copy gedittts.gedit-plugin "C:\Program Files (x86)\gedit\lib\gedit-2\plugins"
copy gedittts.py "C:\Program Files (x86)\gedit\lib\gedit-2\plugins"
xcopy /Y /Q /s /I pyttsx\* "C:\Program Files (x86)\gedit\lib\gedit-2\plugins\pyttsx"

timeout /NOBREAK 3

start "gedit" "c:\Program Files (x86)\gedit\bin\gedit.exe" 2> %tmp%\output.txt
