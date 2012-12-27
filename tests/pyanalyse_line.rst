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

Usage
-----

Blank lines are noted as such.

    >>> paline(0, "")
    'Blank Line'

Other lines are returned verbatim

    >>> paline(0, "def hello:")
    'def hello:'

Repeated calls have no effect (yet)

    >>> paline(1, "def hello:")
    'def hello:'
