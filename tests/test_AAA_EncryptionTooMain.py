#!/usr/bin/env python3

import pytest
from unittest.mock import MagicMock, patch
from src.AAA_EncryptionToolMain import EncryptionTool  # Adjust this import as necessary
import src.lib.Constants as const
from gi.repository import Gtk as gtk

@pytest.fixture
def MockGTK(mocker):
    gi_repo = 'gi.repository.Gtk.'
    mocker.patch(gi_repo+'FileChooserDialog')
    mocker.patch(gi_repo+'TreeView')
    mocker.patch(gi_repo+'ListStore')
    mocker.patch(gi_repo+'CellRendererText')
    mocker.patch(gi_repo+'TreeViewColumn')
    mocker.patch(gi_repo+'Window')
    mocker.patch(gi_repo+'Builder')
    return mocker

@pytest.fixture
def MockEncryptionManager(mocker):
    mock_manager = mocker.Mock()
    mocker.patch('src.lib.EncryptionManager.Manager', return_value=mock_manager)
    return mock_manager

@pytest.fixture
def MockConstants(mocker):
    mocker.patch('src.lib.Constants.NAME_INDEX', 0)
    mocker.patch('src.lib.Constants.SIZE_INDEX', 1)
    mocker.patch('src.lib.Constants.MODIFIED_INDEX', 2)
    return mocker

@pytest.fixture
def EncryptionTool(MockGTK, MockEncryptionManager, MockConstants):
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

def test_GivenNoFileSelectedThenEncryptButtonShouldBeInsensitive(EncryptionTool):
    treeSelectionMock = MagicMock()
    treeSelectionMock.get_selected.return_value = (None, None)

    with patch('lib.Restyle.disableButton') as disableButtonMock:
        EncryptionTool.onContentSelectionChanged(treeSelectionMock)
        disableButtonMock.assert_called_once()