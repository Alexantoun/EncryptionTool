#!/usr/bin/env python3
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from lib.FileController import GetDirectoryContents
import lib.Constants as const

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
            store.append([str(file[const.NAME_INDEX]), str(file[const.SIZE_INDEX]), str(file[const.MODIFIED_INDEX])])
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
            self.alertLabel.set_markup(const.FOLDER_SELECTED(path)) 
            self.populateListView(path)

        elif response == gtk.ResponseType.CANCEL:
            print(f'\tFolder navigation cancelled')
        
        navBox.hide()

    def onFindClick(self, button):
        print('Find button clicked')
        searchStr = self.filterSearch.get_text()
        if searchStr != '':
            print(f'\t{searchStr} Was entered')             
            self.filterTreeViewByInput(searchStr)
            self.alertLabel.set_text('Displaying contents that match \''+searchStr+ '\' in name')
        else:
            print('\tfind button clicked with no input, removing filters')
            self.alertLabel.set_markup(const.ERROR_NO_INPUT_IN_SEARCH_BAR)
            self.contentsView.set_model(self.unfilteredStore)

    def prepareListView(self):
        store = gtk.ListStore(str, str, str)
        self.contentsView.set_model(store)
        # Here, text=0 means that the CellRendererText (renderer) should retrieve the text to display from the first column (index 0) of the TreeStore model.
        self.contentsView.append_column(gtk.TreeViewColumn('File Name', gtk.CellRendererText(),  text=const.NAME_INDEX))
        self.contentsView.append_column(gtk.TreeViewColumn('Size', gtk.CellRendererText(), text=const.SIZE_INDEX))
        self.contentsView.append_column(gtk.TreeViewColumn('Last Modified', gtk.CellRendererText(), text=const.MODIFIED_INDEX))
        #Setting UI behavior of columns
        column = self.contentsView.get_column(const.NAME_INDEX)
        column.set_sort_column_id(const.NAME_INDEX)
        column.set_expand(True)

        column = self.contentsView.get_column(const.SIZE_INDEX)
        column.set_min_width(80)
        column.set_max_width(200)
        
        column = self.contentsView.get_column(const.MODIFIED_INDEX)
        column.set_max_width(200)
        self.unfilteredStore = store        

    def filterTreeViewByInput(self, searchStr:str):
        filterStore = self.unfilteredStore.filter_new() 
        filterStore.set_visible_func(self.getRowsWithSubstringInName, data=searchStr)            
        self.contentsView.set_model(filterStore)

        #Need to define a function to filter the treeview by.
        #parameters are (self, treeViewModel, rowIterator, dataToMatch). Method must match the signature
    def getRowsWithSubstringInName(self, model, iter, data):#<-- signature
        stringToMatch = data
        rowIterator = iter
        treeViewModel = model
        nameInRow = treeViewModel[rowIterator][const.NAME_INDEX] 
        return model[iter][const.NAME_INDEX].find(stringToMatch) != -1

    def __init__(self): 
        builder = gtk.Builder()
        builder.add_from_file('./forms/MainWindow.glade')
        builder.connect_signals(self)
        self.getObjects(builder)
        self.prepareListView()
        self.window.set_default_size(680, 420)
        self.window.show()

    def getObjects(self, builder):
        self.window = builder.get_object('MainWindow')
        self.radioButton1 = builder.get_object('Algo1')
        self.radioButton2 = builder.get_object('Algo2')
        self.radioButton3 = builder.get_object('Algo3')
        self.openButton = builder.get_object('OpenButton')
        self.findButton = builder.get_object('FindButton')
        self.encryptButton = builder.get_object('EncryptButton')
        self.alertLabel = builder.get_object('AlertLabel')
        self.contentsView = builder.get_object('FileView')
        
        self.filterSearch = builder.get_object('SearchEntry')
        EnterKeyPressedInSearchBar = "activate"
        self.filterSearch.connect(EnterKeyPressedInSearchBar, self.onFindClick)

if __name__ == '__main__':
    print('Running encryptor application')
    main = EncryptionControl()
    gtk.main()