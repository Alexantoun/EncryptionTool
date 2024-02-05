#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

class EncryptionControl:
    def onWindowDestroy(self, widget):
        print('Closing application')
        gtk.main_quit()

    def onToggle(self, button): #maybe loop through all three and use a dict to associate a button with a algorithm flag
        if self.radioButton1.get_active():
            self.Algorithm = 'RSA'
        elif self.radioButton2.get_active():
            self.Algorithm = 'AES'
        elif self.radioButton3.get_active():
            self.Algorithm = 'Blowfish'
        else:
            print('Error selecting algorithm')
        print(self.Algorithm + ' was selected')

    def onFindClick(self, button):
        print('Find button clicked')
        searchStr = self.searchBar.get_text()
        if searchStr != '':
            print(searchStr + ' Was entered')
            self.errorLabel.set_text('')
        else:
            print('Search button clicked with no string')
            self.errorLabel.set_text('No text was entered to search for')

    def getObjects(self, builder):
        self.window = builder.get_object('MainWindow')
        self.radioButton1 = builder.get_object('Algo1')
        self.radioButton2 = builder.get_object('Algo2')
        self.radioButton3 = builder.get_object('Algo3')
        self.navButton = builder.get_object('NavigateButton')
        self.searchButton = builder.get_object('SearchButton')
        self.encryptButton = builder.get_object('EncryptButton')
        self.errorLabel = builder.get_object('ErrorLabel')
        self.searchBar = builder.get_object('SearchEntry')

    def __init__(self): 
        builder = gtk.Builder()
        builder.add_from_file('./forms/MainWindow.glade')
        builder.connect_signals(self)
        self.getObjects(builder)
        self.window.set_default_size(425, 250)
        self.window.show()

if __name__ == '__main__':
    print('Running encryptor application')
    main = EncryptionControl()
    gtk.main()