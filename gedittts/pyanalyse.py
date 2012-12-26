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

    def analyse(self, depth, line_text, lineno, lineoffset, body, uri):
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
        elif depth == 2:
            text, self._repeat = self._position(self._repeat, line_text, lineno,
                                                lineoffset)
        elif depth == 3:
            text, self._repeat = self._line(self._repeat, line_text)

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
        return text, repeat

    def _position(self, repeat, line_text, lineno, lineoffset):
        text = ""
        leading_ws = len(line_text) - len(line_text.lstrip())
        if repeat == 0:
            if leading_ws == 0:
                text = "Line {0}, char {1}".format(lineno + 1, lineoffset)
            else:
                lineoffset -= leading_ws
                text = "Line {0}, indent {1}, char {2}".format(lineno + 1,
                                                               leading_ws,
                                                               lineoffset)
            repeat = -1
        return text, repeat

    def _line(self, repeat, line_text):
        text = "Blank Line"
        if line_text.strip() != "":
            text = line_text
        return text, -1