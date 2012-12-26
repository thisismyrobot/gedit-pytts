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
        print "Plugin created for", window
        
        self._window = window
        self._plugin = plugin

        # fire up tts
        self._tts = ttshelper.TTSHelper(rate=150)

        # build a txt analyser
        self._pa = pyanalyse.PyAnalyser()

    def deactivate(self):
        print "Plugin stopped for", self._window
        
        self._window = None
        self._plugin = None
        self._action_group = None

    def say_line(self, window):
        doc = window.get_active_document()
        lineno = doc.get_iter_at_mark(doc.get_insert()).get_line()
        lineoffset = doc.get_iter_at_mark(doc.get_insert()).get_line_offset()
        line_start = doc.get_iter_at_line(lineno)
        line_end = line_start.copy()
        line_end.forward_to_line_end()
        line_text = doc.get_text(line_start, line_end)
        body = doc.get_text(doc.get_start_iter(), doc.get_end_iter())
        result = self._pa.analyse(1, line_text, lineno, lineoffset, body)
        self._tts.say(result)

    def on_key_press_event(self, window, event):
        if event.state & (gtk.gdk.CONTROL_MASK):
            self.say_line(window)


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