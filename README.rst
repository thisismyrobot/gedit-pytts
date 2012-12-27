Python-dev-specific TTS support for Gedit
=========================================

Overarching idea
----------------

Wishful-thinking bigger-picture is to allow flexible development with python for
the blind/vision impared.

Currently
---------

Just testing stuff out on Windows 7 with Gedit 2.30.1 and the built-in SAPI5
TTS.

Modules
-------

I've included some modules in the src as can't easily (and don't really want to)
just polute Gedit's site-packages etc. I've tried to keep in all the
README/LICENCE docs to maintain the goodwill :)

 * pyttsx - from http://pypi.python.org/pypi/pyttsx
   * LICENCE is in __init__.py, I've copied in the README.rst from GitHub and
     the README from the tar.gz.

Win32 requirements
------------------
On windows requires w32com for Gedit's Python. I am using
pywin32-218.win32-py2.6.exe for this version of Gedit (2.30.1).

You need to use a version of python installed on your computer (in my instance,
2.7) to run easy_install, to install the correct version of win32 into Gedit's
version of Python.

How-to:
 1. Open Admin cmd prompt
 2. cd to your pywin install (where pywin32-218.win32-py2.6.exe is)
 3. run:
        set PYTHONPATH-C:\Program Files (x86)\gedit\bin\Lib\site-packages
        c:\Python27\Scripts\easy_install.exe --install-dir="C:\Program Files (x86)\gedit\bin\Lib\site-packages" pywin32-218.win32-py2.6.exe
