#! /usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
import lib.Constants as const

###########################################################################
class EncryptionPrompt(gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title=const.ENCRYPTION_PROMPT_TITLE, transient_for=parent, flags=0)
        self.set_default_size(250, 100)
        self.firstEntry = gtk.Entry()
        self.firstEntry.set_visibility(False)
        self.firstEntry.grab_focus()
        self.secondEntry = gtk.Entry()
        self.secondEntry.connect("changed", self.OnTextEntryChanged)
        self.secondEntry.connect("activate", self.EnterKeyPressed)
        self.secondEntry.set_visibility(False)
        self.secondEntry.set_placeholder_text("Repeat Password")
        
        #To style the dialog window, need to create a vBox with 3 sections, section 1 for password box 1, section 2 for password box 2
        #and section 3 that has a hBox to hold the cancel and ok buttons
        self.add_buttons(gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL, gtk.STOCK_OK, gtk.ResponseType.OK)

        self.box = self.get_content_area()
        self.box.add(self.firstEntry)
        self.box.add(self.secondEntry)
        
        self.OKButton = self.get_widget_for_response(gtk.ResponseType.OK)
        self.OKButton.set_sensitive(False)
        self.show_all()

###########################################################################
    def EnterKeyPressed(self, button):
        self.response(gtk.ResponseType.OK)
        
###########################################################################
    #Whenever a key is pressed inside the 2nd entry line, check if both strings match
    def OnTextEntryChanged(self, entry):
        self.OKButton.set_sensitive(len(entry.get_text()) > 0 and 
                                    self.firstEntry.get_text() == self.secondEntry.get_text())        

###########################################################################
    def get_entry(self) -> str:
        return self.secondEntry.get_text()

###########################################################################
if __name__ == "__main__":
    win = EncryptionPrompt(None)
    response = win.run()
        