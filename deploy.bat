:: This is working on Win7 64bit, try at own risk
:: Oh, and because of all sorts of reasons, this must be ran as administrator...

@echo off

taskkill /F /IM gedit.exe

copy src\geditpytts.gedit-plugin "C:\Program Files (x86)\gedit\lib\gedit-2\plugins"
copy src\geditpytts.py "C:\Program Files (x86)\gedit\lib\gedit-2\plugins"
copy src\ttshelper.py "C:\Program Files (x86)\gedit\lib\gedit-2\plugins"
copy src\pyanalyse.py "C:\Program Files (x86)\gedit\lib\gedit-2\plugins"
xcopy /Y /Q /s /I src\pyttsx\* "C:\Program Files (x86)\gedit\lib\gedit-2\plugins\pyttsx"

start "gedit" "c:\Program Files (x86)\gedit\bin\gedit.exe"
