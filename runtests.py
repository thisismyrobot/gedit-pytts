import doctest
import glob
import os
import sys


sys.path.append(".\src")
opts = doctest.REPORT_ONLY_FIRST_FAILURE|doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE


files = glob.glob('tests\*.rst')
failure = False
for f in files:
    failed, tested = doctest.testfile(f, optionflags=opts)
    if failed > 0:
        failure = True

if not failure:
    print "All tests passed!"

print "\nPress enter to re-run...",
raw_input()
os.system(['clear','cls'][os.name == 'nt'])

# restart myself
python = sys.executable
os.execl(python, python, * sys.argv)