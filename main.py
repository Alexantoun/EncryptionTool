#!/usr/bin/env python3
import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from lib.FileController import GetDirectoryContents

NAME_INDEX = 0
SIZE_INDEX = 1
MODIFIED_INDEX = 2

class LabelText: #Move to another file
    ERROR_NO_INPUT_IN_SEARCH_BAR = '<span foreground="#ff1a1a" weight="normal">No text was entered to search for</span>'

    def FOLDER_SELECTED(path:str) -> str:
        string = '<span foreground="#000000" weight="normal">Displaying content in '+path+'</span>'
        return string
    
    def ERROR_INPUT_NOT_FOUND(input:str) -> str:
        string = '<span foreground="red" weight="Bold">No text was entered to search for</span>'
        return string

######################################################################################################
        
class EncryptionControl:
    def onWindowDestroy(self, widget):
        print('Closing application')
        gtk.main_quit()

    def populateListView(self, path):
        print('Populating list view with:\n\t')  
        directoryContents = GetDirectoryContents(path)
        store = self.contentsView.get_model()
        for file in directoryContents:
            store.append([str(file[NAME_INDEX]), str(file[SIZE_INDEX]), str(file[MODIFIED_INDEX])])
        self.contentsView.set_model(store)
    

    def onToggle(self, button): #maybe loop through all three and use a dict to associate a button with an algorithm flag
        if self.radioButton1.get_active():
            self.Algorithm = 'RSA'
        elif self.radioButton2.get_active():
            self.Algorithm = 'AES'
        elif self.radioButton3.get_active():
            self.Algorithm = 'Blowfish'
        else:
            print('Error selecting algorithm')
        print(f'{self.Algorithm} was selected')
        
    def onOpenClicked(self, button):
        print('Open button clicked')
        navBox = gtk.FileChooserDialog(title = "Navigate to directory", parent = None, action = gtk.FileChooserAction.SELECT_FOLDER)
        navBox.set_default_size(150, 150)
        navBox.add_buttons(gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL, 'Select Folder', gtk.ResponseType.OK)
        navBox.set_current_folder(os.path.expanduser('~'))
        response = navBox.run()

        if response == gtk.ResponseType.OK:
            path = navBox.get_current_folder()
            print(f'\tFolder selected: {path}')
            self.alertLabel.set_markup(LabelText.FOLDER_SELECTED(path)) 
            self.populateListView(path)

        elif response == gtk.ResponseType.CANCEL:
            print(f'\tFolder navigation cancelled')
        
        navBox.hide()

    def onFindClick(self, button):
        print('Find button clicked')
        searchStr = self.findBar.get_text()
        if searchStr != '':
            print(f'\t{searchStr} Was entered')
            self.alertLabel.set_text('')
        else:
            print('\tfind button clicked with no input')
            self.alertLabel.set_markup(LabelText.ERROR_NO_INPUT_IN_SEARCH_BAR)

    def getObjects(self, builder):
        self.window = builder.get_object('MainWindow')
        self.radioButton1 = builder.get_object('Algo1')
        self.radioButton2 = builder.get_object('Algo2')
        self.radioButton3 = builder.get_object('Algo3')
        self.openButton = builder.get_object('OpenButton')
        self.findButton = builder.get_object('FindButton')
        self.encryptButton = builder.get_object('EncryptButton')
        self.alertLabel = builder.get_object('AlertLabel')
        self.findBar = builder.get_object('SearchEntry')
        self.contentsView = builder.get_object('FileView')

    def prepareListView(self):
        store = gtk.ListStore(str, str, str)
        self.contentsView.set_model(store)
        self.contentsView.append_column(gtk.TreeViewColumn('File Name', gtk.CellRendererText(),  text=NAME_INDEX))
        self.contentsView.append_column(gtk.TreeViewColumn('Size', gtk.CellRendererText(), text=SIZE_INDEX))
        self.contentsView.append_column(gtk.TreeViewColumn('Last Modified', gtk.CellRendererText(), text=MODIFIED_INDEX))
        
        column = self.contentsView.get_column(NAME_INDEX)
        column.set_expand(True)

        column = self.contentsView.get_column(SIZE_INDEX)
        column.set_min_width(80)
        column.set_max_width(200)
        
        column = self.contentsView.get_column(MODIFIED_INDEX)
        column.set_max_width(200)

    def __init__(self): 
        builder = gtk.Builder()
        builder.add_from_file('./forms/MainWindow.glade')
        builder.connect_signals(self)
        self.getObjects(builder)
        self.prepareListView()
        self.window.set_default_size(680, 420)
        self.window.show()

if __name__ == '__main__':
    print('Running encryptor application')
    main = EncryptionControl()
    gtk.main()