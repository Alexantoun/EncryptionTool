import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
import lib.Constants as const

class DecryptionPrompt(gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title=const.DECRYPTION_PROMPT_TITLE, transient_for=parent, flags = 0)
        self.set_default_size(250, 80)
        self.entry = gtk.Entry()
        self.entry.set_visibility(False)
        self.entry.grab_focus()
        self.entry.connect("activate", self.OnEnterKeyPressed)
        self.entry.connect("changed", self.OnTextEntryChanged)

        self.add_buttons(gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL, gtk.STOCK_OK, gtk.ResponseType.OK)
        self.box = self.get_content_area()
        self.box.add(self.entry)

        self.OKButton = self.get_widget_for_response(gtk.ResponseType.OK)
        self.OKButton.set_sensitive(False)
        self.show_all()

    def OnEnterKeyPressed(self, button):
        self.response(gtk.ResponseType.OK)
    
    def OnTextEntryChanged(self, entry):
        self.OKButton.set_sensitive(len(entry.get_text()) > 0)

    def get_entry(self) -> str:
        return self.entry.get_text()
    
if __name__ == "__main__":
    win = DecryptionPrompt(None)
    response = win.run()
