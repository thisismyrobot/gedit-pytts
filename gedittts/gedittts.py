from gettext import gettext as _

import gtk
import gedit
import pyanalyse
import ttshelper

# Menu item example, insert a new item in the Tools menu
ui_str = """<ui>
  <menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
      <placeholder name="ToolsOps_2">
        <menuitem name="GeditTTS" action="GeditTTS"/>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""

class GeditTTSWindowHelper:
    def __init__(self, plugin, window):
        self._window = window
        self._plugin = plugin

        # fire up tts
        self._tts = ttshelper.TTSHelper(rate=150)

        # build a txt analyser
        self._pa = pyanalyse.PyAnalyser(indent=4)

    def deactivate(self):
        self._window = None
        self._plugin = None

    def analyse_line(self, window, depth):
        doc = window.get_active_document()
        lineno = doc.get_iter_at_mark(doc.get_insert()).get_line()
        lineoffset = doc.get_iter_at_mark(doc.get_insert()).get_line_offset()
        line_start = doc.get_iter_at_line(lineno)
        
        line_end = line_start.copy()
        line_end.forward_to_line_end()
        line_text = doc.get_text(line_start, line_end)
        body = doc.get_text(doc.get_start_iter(), doc.get_end_iter())

        result = self._pa.analyse(depth, line_text, lineno, lineoffset, body,
                                  doc.get_uri())
        self._tts.say(result)

    def on_key_press_event(self, window, event):
        # trap Alt + * combinations
        if event.state & (gtk.gdk.MOD1_MASK):
            # trap analyse text by looking for integer pressed
            i = None
            try:
                i = int(event.string)
            except ValueError:
                pass
            if i is not None and 1 <= i <= 9:
                self.analyse_line(window, i)


class GeditTTS(gedit.Plugin):
    def __init__(self):
        gedit.Plugin.__init__(self)
        self._instances = {}
        self._handlers = [None]

    def activate(self, window):
        gttsh = GeditTTSWindowHelper(self, window)
        self._instances[window] = gttsh

        # set up key handler
        if self._handlers[0] is None:
            self._handlers[0] = window.connect('key-press-event',
                                               gttsh.on_key_press_event)

    def deactivate(self, window):
        self._instances[window].deactivate()
        del self._instances[window]