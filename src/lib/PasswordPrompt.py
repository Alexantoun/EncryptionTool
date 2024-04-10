#! /usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

class PasswordPrompt(gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="My Dialog", transient_for=parent, flags=0)
        self.set_default_size(250, 100)
        self.firstEntry = gtk.Entry()
        self.secondEntry = gtk.Entry()
        self.secondEntry.connect("changed", self.OnTextEntryChanged)

        #To style the dialog window, need to create a vBox with 3 sections, section 1 for password box 1, section 2 for password box 2
        #and section 3 that has a hBox to hold the cancel and ok buttons
        self.add_buttons(gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL, gtk.STOCK_OK, gtk.ResponseType.OK)

        self.box = self.get_content_area()
        self.box.add(self.firstEntry)
        self.box.add(self.secondEntry)
        
        self.OKButton = self.get_widget_for_response(gtk.ResponseType.OK)
        self.OKButton.set_sensitive(False)

        self.show_all()

    #Whenever a key is pressed inside the 2nd entry line, check if both strings match
    def OnTextEntryChanged(self, entry):
        self.OKButton.set_sensitive(len(entry.get_text()) > 0 and 
                                    self.firstEntry.get_text() == self.secondEntry.get_text())        

    def get_entry(self, entry):
        return self.secondEntry.get_text()

if __name__ == "__main__":
    win = PasswordPrompt(None)
    response = win.run()
        