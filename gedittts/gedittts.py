from gettext import gettext as _

import gtk
import gedit
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

        # Insert menu items
        self._insert_menu()

    def deactivate(self):
        print "Plugin stopped for", self._window
        
        # Remove any installed menu items
        self._remove_menu()
        
        self._window = None
        self._plugin = None
        self._action_group = None

    def _insert_menu(self):
        # Get the GtkUIManager
        manager = self._window.get_ui_manager()

        # Create a new action group
        self._action_group = gtk.ActionGroup("GeditTTSPluginActions")
        self._action_group.add_actions([("GeditTTS", None, _("Clear document"),
                                         None, _("Clear the document"),
                                         self.on_clear_document_activate)])

        # Insert the action group
        manager.insert_action_group(self._action_group, -1)

        # Merge the UI
        self._ui_id = manager.add_ui_from_string(ui_str)

    def _remove_menu(self):
        # Get the GtkUIManager
        manager = self._window.get_ui_manager()

        # Remove the ui
        manager.remove_ui(self._ui_id)

        # Remove the action group
        manager.remove_action_group(self._action_group)

        # Make sure the manager updates
        manager.ensure_update()

    def update_ui(self):
        self._action_group.set_sensitive(self._window.get_active_document() != None)

    # Menu activate handlers
    def on_clear_document_activate(self, action):
        doc = self._window.get_active_document()
        if not doc:
            return

        doc.set_text('')

    def fix_line(self, line):
        line = line.replace(' "', " . Start string literal. ")
        return line

    def say_line(self, window):
        doc = window.get_active_document()
        row = doc.get_iter_at_mark(doc.get_insert()).get_line() + 1
        line_start = doc.get_iter_at_line(row - 1)
        line_end = line_start.copy()
        line_end.forward_to_line_end()
        line_text = doc.get_text(line_start, line_end)
        line_text = self.fix_line(line_text)
        if line_text.strip() == "":
            self._tts.say("Line {0}. Blank line".format(row))
        else:
            # get indent
            indent = len(line_text) - len(line_text.lstrip())
            if indent == 0:
                self._tts.say("Line {0}. {1}".format(row, line_text))
            else:
                self._tts.say("Line {0}, indent {1}. {2}".format(row, indent, line_text))
 
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

    def update_ui(self, window):
        self._instances[window].update_ui()