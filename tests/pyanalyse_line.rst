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