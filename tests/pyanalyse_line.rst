Line printing
=============

This will become _much_ bigger, but is curretly just printing the line.

The aim is to have lots more context - like turning "def hello:" into "function
definition hello".

Setup
-----

We need an analyser.

    >>> import pyanalyse
    >>> pa = pyanalyse.PyAnalyser()

And a helper to just return the text component from this method.

    >>> paline = lambda repeat, line: pa._line(repeat, line)[0]

Blank lines
-----------

Blank lines are noted as such.

    >>> paline(0, "")
    'Blank Line'

Functions
---------

Are identified as such

    >>> paline(0, "def hello:")
    'Function definition: def hello:'

Repeated calls have no effect (yet)

    >>> paline(1, "def hello:")
    'Function definition: def hello:'

Classes
-------

Work like functions

    >>> paline(0, "class testclass:")
    'Class definition: class testclass:'

And repeated calls show inheritance (or lack thereof)

    >>> paline(1, "class testclass:")
    'No inheritance'

    >>> paline(0, "class testclass(object, yucky.mixin): # comment (with arg test, )")
    'Class definition: class testclass:. Comment: comment (with arg test, )'

Extra multi-part info is ignored if describing inheritance

    >>> paline(1, "class testclass(object, yucky.mixin): # comment (with arg test, )")
    'Inherits object , yucky dot mixin'

Comments
--------

Single line comments are identified

    >>> paline(0, "# Here's a comment")
    "Comment: Here's a comment"

Even it they are indented

    >>> paline(0, "    # Here's another comment")
    "Comment: Here's another comment"

Combinations
------------

Multiple entries are appended together on a line, with a full stop and space
between.

    >>> paline(0, "def funct:  # Wow, I made a function")
    'Function definition: def funct:. Comment: Wow, I made a function'