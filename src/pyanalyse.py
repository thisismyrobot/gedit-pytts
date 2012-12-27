import os.path
import StringIO
import tokenize


class PyAnalyser(object):
    """ Analyses a location amongst python text.
    """
    def __init__(self, indent=4):
        self._indent = 4
        self._lineno = -1
        self._lineoffset = -1
        self._lastdepth = -1
        self._repeat = 0 # set to -1 to change between modes in depth

    def analyse(self, depth, line_text, lineno, lineoffset, body, uri):
        """ Chooses the correct handler based on the type of analysis (depth)
            required.
        """
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
        """ Returns filename/path information.
        """
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
        """ Returns positional information including indent.
        """
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
        """ Just returns lines, but will soon have contextual information too.
        """
        text = ""

        # tokenize the line (makes for sane matching of components)
        line_tokens = list(tokenize.generate_tokens(
                                StringIO.StringIO(line_text.strip()).readline))

        for i, (type, val, _, _, _) in enumerate(line_tokens):

            # things we don't want
            if val in (":",):
                continue

            # blank lines on their own
            if type == tokenize.ENDMARKER and len(line_tokens) == 1:
                text += "Blank Line"

            # single line comment
            elif type == tokenize.COMMENT:
                text += "Comment: {0}".format(val[1:].strip())

            # function definition
            elif type == tokenize.NAME and val == "def":
                text += "Function definition: def {0}:".format(line_tokens[i+1][1])
                del line_tokens[i+1]

            # catch-all
            else:
                text += val

            text += ". "

        # clean up string having lots of full stops at end
        text = text.strip()
        while text[-1] == ".":
            text = text[:-1].strip()

        return text.strip(), -1