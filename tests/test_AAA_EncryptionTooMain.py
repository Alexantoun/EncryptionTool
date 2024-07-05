#!/usr/bin/env python3

import pytest
from unittest.mock import MagicMock, patch
from src.AAA_EncryptionToolMain import EncryptionTool  # Adjust this import as necessary


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
def mock_encryption_manager(mocker):
    mocker.patch('src.lib.EncryptionManager.Manager')
    return mocker

@pytest.fixture
def MockConstants(mocker):
    mocker.patch('src.lib.Constants.NAME_INDEX', 0)
    mocker.patch('src.lib.Constants.SIZE_INDEX', 1)
    mocker.patch('src.lib.Constants.MODIFIED_INDEX', 2)
    return mocker

@pytest.fixture
def EncryptionTool(MockGTK, mock_encryption_manager, MockConstants):
    from src.AAA_EncryptionToolMain import EncryptionTool
    return EncryptionTool()

#<<<<<<<<<<<<<<<<<<<< Begin Tests >>>>>>>>>>>>>>>>>>>>
def test_OnAESToggleClickedThenAESAlgorithmShouldSelectedByEncryptionManager(EncryptionTool):
    EncryptionTool.AESButton = MagicMock()
    EncryptionTool.BlowFishButton = MagicMock()
    #sets what the objects will return when invoked by the test
    EncryptionTool.AESButton.get_active.return_value = True
    EncryptionTool.BlowfishButton.get_active.return_value = False
    
    EncryptionTool.onToggle(None)

    EncryptionTool.encryptionManager.setAlgorithm.assert_called_with(EncryptionTool.encryptionManager.algorithm.AES_CBC)    


