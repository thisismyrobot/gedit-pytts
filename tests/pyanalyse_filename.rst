Filename/path analysis
======================

Setup
-----

We need an analyser.

    >>> import pyanalyse
    >>> pa = pyanalyse.PyAnalyser()

And a helper to just return the text component from this method

    >>> pafn = lambda repeat, uri: pa._filename(repeat, uri)[0]

Unsaved files
-------------

Are treated as such (the uri passed in is None).

    >>> pafn(0, None)
    'Unsaved file'

And calling it multiple times has the same result

    >>> pafn(1, None)
    'Unsaved file'

Filenames/paths
---------------

The first call brings up the filename

    >>> pafn(0, 'file:///C:/coding/test.txt')
    'test.txt'

The second brings up the path

    >>> pafn(1, 'file:///C:/coding/test.txt')
    'Inside file:///C:/coding'
