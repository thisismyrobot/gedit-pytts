import os.path


class PyAnalyser(object):
    """ Analyses python.
    """
    def __init__(self, indent=4):
        self._indent = 4
        self._lineno = -1
        self._lineoffset = -1
        self._lastdepth = -1
        self._repeat = 0 # set to -1 to change between modes in depth

    def analyse(self, depth, line, lineno, lineoffset, body, uri):
        text = ""

        # cancel repeat recording between depth changes
        if self._lastdepth != depth:
            self._repeat = 0
        else:
            # if we are still in the same location, increment repeat counter
            if self._lineno == lineno and self._lineoffset == lineoffset:
                self._repeat += 1
            # if we move, reset repeat too
            else:
                self._repeat = 0

        # filename/path enquiry
        if depth == 1:
            text, self._repeat = self._filename(self._repeat, uri)

        self._lineno = lineno
        self._lineoffset = lineoffset
        self._lastdepth = depth
        return text

    def _filename(self, repeat, uri):
        text = ""
        if uri is None:
            text = "Unsaved file"
            repeat = -1
        else:
            if repeat == 0:
                text = os.path.basename(uri)
            elif repeat == 1:
                text = "Inside {0}".format(os.path.dirname(uri))
                repeat = -1
            elif repeat > 1:
                repeat = 0
        return text, repeat