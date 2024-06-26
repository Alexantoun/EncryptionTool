#!/usr/bin/env python3
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

from lib.DirectoryInterface import GetDirectoryContents
import lib.Constants as const
import lib.Restyle as widgetStyler
import lib.EncryptionManager as encryptionManager
from lib.EncryptionManager import Algorithms_E as encryptionAlgorithms

###########################################################################    
class EncryptionControl:
    def onWindowDestroy(self, widget):
        print('Closing application')
        gtk.main_quit()
        print('Tasks still required: ')
        print('\tNeed to have the color of encrypt button be determined by whethor or not its an encrypted file')
        print('\tConstants.py needs renaming as there are methods in there to return a string')
        print('\tDirectoryInterface should get renamed to something else')
        print('\tAdd Encryption key instructions into the Encryption prompt module')
        
###########################################################################
    def onToggle(self, button): #maybe loop through all three and use a dict to associate a button with an algorithm flag
        if self.RSAButton.get_active():
            self.encryptionManager.setAlgorithm(encryptionAlgorithms.RSA)
        elif self.AESButton.get_active():
            self.encryptionManager.setAlgorithm(encryptionAlgorithms.AES_CBC)
        elif self.BlowfishButton.get_active():
            self.encryptionManager.setAlgorithm(encryptionAlgorithms.B_FISH)
        else:
            print('Error selecting algorithm')        

########################################################################### 
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

            self.unfilteredStore.clear()
            self.selectedFile = None
            self.encryptionManager.pathToFile = path
            self.alertLabel.set_markup(const.FOLDER_SELECTED(path))
            self.populateListView(path)            

        elif response == gtk.ResponseType.CANCEL:
            print(f'\tFolder navigation cancelled')

        navBox.hide()

###########################################################################
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
            self.selectedFile = None
            widgetStyler.disableButton(self.encryptButton)

###########################################################################
    def onCipherButtonClick(self, button):
        print('cipher button clicked')
        if self.selectedFile != None:
            print(f'\t{self.selectedFile} chosen for encryption')
            self.encryptionManager.onCipherButtonClick(self.selectedFile)        

###########################################################################
    def onContentSelectionChanged(self, treeViewSelection):
        model, treeItr = treeViewSelection.get_selected()
        if treeItr != None:
            self.selectedFile = model[treeItr][const.NAME_INDEX]
            self.alertLabel.set_text('You selected \''+ self.selectedFile +'\'')
            
            # if not self.encryptButton.get_sensitive():
            self.encryptButton.set_sensitive(True)

            #Change button color based on if the file is encrypted or not
            if self.encryptionManager.checkSelectedFileEncryptionStatus(self.selectedFile):
                widgetStyler.makeButtonRed(self.encryptButton)
            else:
                widgetStyler.makeButtonGreen(self.encryptButton)            

        else:
            widgetStyler.disableButton(self.encryptButton)
            self.selectedFile = None

###########################################################################
    def prepareListView(self):
        store = gtk.ListStore(str, str, str)
        self.contentsView.set_model(store)
        # Here, text=n means that the CellRendererText should retrieve the text to display from the nth column of the TreeStore model.
        self.contentsView.append_column(gtk.TreeViewColumn('File Name', gtk.CellRendererText(),  text=const.NAME_INDEX))
        self.contentsView.append_column(gtk.TreeViewColumn('Size (kB)', gtk.CellRendererText(), text=const.SIZE_INDEX))
        self.contentsView.append_column(gtk.TreeViewColumn('Last Modified', gtk.CellRendererText(), text=const.MODIFIED_INDEX))
        #Setting UI behavior of columns
        nameColumn = self.contentsView.get_column(const.NAME_INDEX)
        nameColumn.set_sort_column_id(const.NAME_INDEX)
        nameColumn.set_min_width(200)        
        nameColumn.set_expand(True)

        sizeColumn = self.contentsView.get_column(const.SIZE_INDEX)
        sizeColumn.set_min_width(80)
        sizeColumn.set_max_width(200)
        
        dateColumn = self.contentsView.get_column(const.MODIFIED_INDEX)
        dateColumn.set_min_width(200)
        dateColumn.set_max_width(200)
        
        self.unfilteredStore = store
        self.contentSelection = self.contentsView.get_selection()
        self.contentSelection.connect("changed", self.onContentSelectionChanged)
        self.selectedFile = None

###########################################################################
    def populateListView(self, path):
        print('Populating list view with:\n\t')
        directoryContents = GetDirectoryContents(path)

        store = self.contentsView.get_model()
        for file in directoryContents:
            store.append([str(file[const.NAME_INDEX]), str(file[const.SIZE_INDEX]), str(file[const.MODIFIED_INDEX])])
            
        self.contentsView.set_model(store)
        
###########################################################################
    def filterTreeViewByInput(self, searchStr : str):
        filterStore = self.unfilteredStore.filter_new() 
        #Need to define a function to filter the treeview by.
        filterStore.set_visible_func(self.getRowsWithSubstringInName, data=searchStr)            
        self.contentsView.set_model(filterStore)

###########################################################################
        #parameters are (self, treeViewModel, rowIterator, dataToMatch). Method must match the signature
    def getRowsWithSubstringInName(self, model, iter, data):
        stringToMatch = data
        return model[iter][const.NAME_INDEX].lower().find(stringToMatch.lower()) != -1 
    
###########################################################################
    def __init__(self): 
        builder = gtk.Builder()
        builder.add_from_file('./forms/MainWindow.glade')
        builder.connect_signals(self)
        self.getObjects(builder)        
        self.encryptionManager = encryptionManager.Manager(self.window)
        self.encryptButton.set_label('Encrypt')
        self.onToggle(None)
        self.prepareListView()
        self.window.set_default_size(680, 420)      
        self.openedDirectoryPath = ''
        self.window.set_title('File Security')
        self.window.show_all()

###########################################################################
    def getObjects(self, builder):
        self.window = builder.get_object('MainWindow')
        self.RSAButton = builder.get_object('Algo1')
        self.AESButton = builder.get_object('Algo2')
        self.BlowfishButton = builder.get_object('Algo3')
        self.openButton = builder.get_object('OpenButton')
        self.findButton = builder.get_object('FindButton')
        self.alertLabel = builder.get_object('AlertLabel')
        self.contentsView = builder.get_object('FileView')
        self.filterSearch = builder.get_object('SearchEntry')

        self.encryptButton = builder.get_object('EncryptButton')
        self.encryptButton.set_sensitive(False)
        
        enterKeyPressedInSearchBar = "activate"
        self.filterSearch.connect(enterKeyPressedInSearchBar, self.onFindClick)

if __name__ == '__main__':
    print('Running encryptor application')
    main = EncryptionControl()
    gtk.main()