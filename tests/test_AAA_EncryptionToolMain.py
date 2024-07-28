import pytest
from unittest.mock import MagicMock, patch
from gi.repository import Gtk as gtk

@pytest.fixture
def MockGTK(mocker):
    gi_repo = 'gi.repository.Gtk.'
    mocker.patch(gi_repo+'FileChooserDialog')
    mocker.patch(gi_repo+'Builder')
    return mocker

@pytest.fixture
def EncryptionTool(MockGTK):
    from src.AAA_EncryptionToolMain import EncryptionTool
    return EncryptionTool()

#<<<<<<<<<<<<<<<<<<<< Begin Tests >>>>>>>>>>>>>>>>>>>>
def test_GivenAESToggleClickedThenEncryptionManagerSetToUseAES(EncryptionTool):
    EncryptionTool.AESButton = MagicMock()
    EncryptionTool.blowFishButton = MagicMock()
    EncryptionTool.encryptionManager.setAlgorithm = MagicMock()
    #sets what the objects will return when invoked by the test
    EncryptionTool.AESButton.get_active.return_value = True
    EncryptionTool.blowFishButton.get_active.return_value = False
    
    EncryptionTool.onToggle(None)
    EncryptionTool.encryptionManager.setAlgorithm.assert_called_once_with(EncryptionTool.encryptionManager.algorithm.AES_CBC)

###########################################################################
def test_GivenBlowfishToggleClickedThenEncryptionManagerSetToUseBlowfish(EncryptionTool):
    EncryptionTool.AESButton = MagicMock()
    EncryptionTool.blowFishButton = MagicMock()
    EncryptionTool.encryptionManager.setAlgorithm = MagicMock()
    #sets what the objects will return when invoked by the test
    EncryptionTool.AESButton.get_active.return_value = False
    EncryptionTool.blowfishButton.get_active.return_value = True
    
    EncryptionTool.onToggle(None)
    EncryptionTool.encryptionManager.setAlgorithm.assert_called_once_with(EncryptionTool.encryptionManager.algorithm.B_FISH)

###########################################################################
def test_GivenEncryptedFiledSelectedThenEncryptButtonShouldBeRestyledRedAndSensitive(EncryptionTool):    
    treeSelectionMock = MagicMock()
    treeModelMock = MagicMock()
    treeIterMock = MagicMock()
    EncryptionTool.encryptionManager = MagicMock()

    treeSelectionMock.get_selected.return_value = (treeModelMock, treeIterMock)

    EncryptionTool.encryptionManager.checkSelectedFileEncryptionStatus.return_value = True

    #patch Restyle's makeButtonRed method 
    with patch('lib.Restyle.makeButtonRed') as makeButtonRedMock:
        EncryptionTool.onContentSelectionChanged(treeSelectionMock)
        makeButtonRedMock.assert_called_once()

###########################################################################
def test_GivenPlainTextFileSelectedThenEncryptButtonShouldBeRestyledGreenAndSensitive(EncryptionTool):
    treeSelectionMock = MagicMock()
    treeModelMock = MagicMock()
    treeIterMock = MagicMock()
    EncryptionTool.encryptionManager = MagicMock()

    treeSelectionMock.get_selected.return_value = (treeModelMock, treeIterMock)
    EncryptionTool.encryptionManager.checkSelectedFileEncryptionStatus.return_value = False

    with patch('lib.Restyle.makeButtonGreen') as makeButtonGreenMock:
        EncryptionTool.onContentSelectionChanged(treeSelectionMock)
        makeButtonGreenMock.assert_called_once()

###########################################################################
def test_GivenNoFileSelectedThenEncryptButtonShouldBeInsensitive(EncryptionTool):
    treeSelectionMock = MagicMock()
    treeSelectionMock.get_selected.return_value = (None, None)

    with patch('lib.Restyle.disableButton') as disableButtonMock:
        EncryptionTool.onContentSelectionChanged(treeSelectionMock)
        disableButtonMock.assert_called_once()

###########################################################################
def test_OnFolderSelectedThenPopulateListViewIsCalledAndEncryptionManagerUpdated(EncryptionTool):    
    expectedPath = '/arbitrary/path'
    EncryptionTool.populateListView = MagicMock()

    #Dont need to patch FileChooserDialog because its handled in MockGTK()
    fileChooserDialogMock = gtk.FileChooserDialog.return_value
    fileChooserDialogMock.run.return_value = gtk.ResponseType.OK
    fileChooserDialogMock.get_current_folder.return_value = expectedPath

    EncryptionTool.onOpenClicked(None)
    EncryptionTool.populateListView.assert_called_once_with(expectedPath)
    assert EncryptionTool.encryptionManager.pathToFile == expectedPath

###########################################################################
def test_OnRefreshClickedThenInvokePopulateListView(EncryptionTool):    
    EncryptionTool.unfilteredStore.clear = MagicMock()
    EncryptionTool.filterSearch.set_text = MagicMock()
    EncryptionTool.populateListView = MagicMock()
    EncryptionTool.SelectedFolder = MagicMock()

    EncryptionTool.onRefreshClicked(None)
    EncryptionTool.unfilteredStore.clear.assert_called_once()
    EncryptionTool.filterSearch.set_text.assert_called_once_with('')
    EncryptionTool.populateListView.assert_called_once()

###########################################################################
def test_OnCipherButtonClickedThenEncryptionManagerReceivesCorrectFile(EncryptionTool):
    EncryptionTool.selectedFile = 'ArbitraryFile'
    EncryptionTool.encryptionManager.onCipherButtonClick = MagicMock()

    EncryptionTool.onCipherButtonClick(None)
    EncryptionTool.encryptionManager.onCipherButtonClick.assert_called_once_with('ArbitraryFile')