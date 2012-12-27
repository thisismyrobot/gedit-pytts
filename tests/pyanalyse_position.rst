Position identification
=======================

Helpers to give the user an idea where they are in the document.

Setup
-----

We need an analyser.

    >>> import pyanalyse
    >>> pa = pyanalyse.PyAnalyser()

And a helper to just return the text component from this method.

    >>> papos = lambda repeat, l_txt, l_no, l_offset: pa._position(repeat, l_txt, l_no, l_offset)[0]

Usage
-----

Lines that are left-aligned return just the position. The line number is 1-based
based on convention, but the character position is zero-based.

    >>> papos(0, "def hello:", 2, 3)
    'Line 3, char 3'

Lines that are indented have that noted, with the char being _after_ the indent.

    >>> papos(0, '    print "hello world"', 5, 9)
    'Line 6, indent 4, char 5'

Being in part of the indented area returns a negative char, showing how far you
are from the first char.

    >>> papos(0, '    print "hello world"', 5, 2)
    'Line 6, indent 4, char -2'

    >>> papos(0, '    print "hello world"', 5, 4)
    'Line 6, indent 4, char 0'
