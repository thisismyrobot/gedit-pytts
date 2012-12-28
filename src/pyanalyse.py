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

        for i, (type, val, _, _, line) in enumerate(line_tokens):

            # things we don't want
            if val.lower() in (":",):
                continue

            # blank lines on their own
            if type == tokenize.ENDMARKER and len(line_tokens) == 1:
                text += "Blank Line"

            # single line comment
            elif type == tokenize.COMMENT:
                text += "Comment: {0}".format(val[1:].strip())

            # function definition
            elif type == tokenize.NAME and val.lower() == "def":
                text += "Function definition: def {0}:".format(line_tokens[i+1][1])
                del line_tokens[i+1]

            # class definition
            elif type == tokenize.NAME and val.lower() == "class":
                # see if has inheritance
                inherits = None
                end = 0
                if line_tokens[i+2][1] == "(":
                    end = i+3
                    while line_tokens[end][1] != ")":
                        end += 1
                    # read in the inheritance
                    inherits = " ".join([t[1]
                                        for t
                                        in line_tokens[i+3:end]])
                if repeat == 0:
                    # return the def without the inheritance
                    text += "Class definition: class {0}:".format(line_tokens[i+1][1])
                    del line_tokens[i+1]
                    # need to delete the inheritance
                    if inherits is not None:
                        for j in range(end - i - 1):
                            del line_tokens[i + 1]
                elif repeat == 1:
                    # return the inheritance only, if there is any
                    if inherits is not None:
                        text += "Inherits {0}".format(inherits.replace(".", "dot"))
                    else:
                        text += "No inheritance"
                    # we don't process any more tokens from here
                    break

            # catch-all
            else:
                text += val

            text += ". "

        # clean up string having lots of full stops at end
        text = text.strip()
        if len(text) > 2:
            while text[-1] == ".":
                text = text[:-1].strip()

        if repeat == 1:
            repeat = -1

        return text.strip(), repeat