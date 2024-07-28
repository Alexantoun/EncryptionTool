import pytest
from unittest.mock import MagicMock, patch
import lib.EncryptionManager
import lib.FileCipher
import lib.KeyPrompts

TEST_FILE_PATH = 'some/directory/path/'
TEST_FILE = 'arbitraryFile.txt'
TEST_KEY = 'SecurePassword'

DEFAULT_ALGORITHM = lib.EncryptionManager.Algorithms_E.AES_CBC
OK_REPONSE = lib.EncryptionManager.RESPONSE_TYPE_OK

@pytest.fixture
def MockPrompts(mocker):
    mocker.patch('lib.KeyPrompts.EncryptionPrompt')
    mocker.patch('lib.KeyPrompts.DecryptionPrompt')
    return mocker

@pytest.fixture
def EncryptionManager(MockPrompts):
    from lib.EncryptionManager import Manager as mgr
    return mgr(None)

def test_OnEncryptClickedAndValidKeysEnteredExpectCipherToEncryptChosenFile(EncryptionManager):
    promptMock = lib.KeyPrompts.EncryptionPrompt.return_value
    promptMock.get_entry.return_value = TEST_KEY
    promptMock.run.return_value = OK_REPONSE

    EncryptionManager.pathToFile = TEST_FILE_PATH
    EncryptionManager.selectedFile = TEST_FILE
    EncryptionManager.fileCipher = MagicMock()
    EncryptionManager.fileCipher.Encrypt = MagicMock()
    EncryptionManager.algorithm = DEFAULT_ALGORITHM

    EncryptionManager.encryptClicked()
    EncryptionManager.fileCipher.Encrypt.assert_called_once_with(f'{TEST_FILE_PATH}/{TEST_FILE}', TEST_KEY)
    promptMock.destroy.assert_called_once()

def test_OnDecryptClickedAndKeyEnteredExpectCipherToDecryptChosenFile(EncryptionManager):
    promptMock = lib.KeyPrompts.DecryptionPrompt.return_value
    promptMock.get_entry.return_value = TEST_KEY
    promptMock.run.return_value = OK_REPONSE
    
    EncryptionManager.pathToFile = TEST_FILE_PATH
    EncryptionManager.selectedFile = TEST_FILE
    EncryptionManager.fileCipher = MagicMock()
    EncryptionManager.fileCipher.Decrypt = MagicMock()
    EncryptionManager.algorithm = DEFAULT_ALGORITHM

    EncryptionManager.decryptClicked()
    EncryptionManager.fileCipher.Decrypt.assert_called_once_with(f'{TEST_FILE_PATH}/{TEST_FILE}', TEST_KEY)
    promptMock.destroy.assert_called_once()

def test_OnAlgorithmSelectedExpectFileCipherToBeAssignedCorrectly(EncryptionManager):
    EncryptionManager.setAlgorithm(DEFAULT_ALGORITHM)
    assert lib.FileCipher.AES_CBC == EncryptionManager.fileCipher

    EncryptionManager.setAlgorithm(lib.EncryptionManager.Algorithms_E.B_FISH)
    assert lib.FileCipher.BLOWFISH_CBC == EncryptionManager.fileCipher

def test_OnCipherButtonClickHandlerThatsCalledBasedOnFileEncryptedStatus(EncryptionManager):    
    with patch.object(EncryptionManager, 'encryptClicked') as encryptClickedMock, \
         patch.object(EncryptionManager, 'decryptClicked') as decryptClickedMock:
        
        EncryptionManager.fileIsEncrypted = False
        EncryptionManager.onCipherButtonClick()
        encryptClickedMock.assert_called_once()
        decryptClickedMock.assert_not_called()

        encryptClickedMock.reset_mock()
        decryptClickedMock.reset_mock()

        EncryptionManager.fileIsEncrypted = True
        EncryptionManager.onCipherButtonClick()
        encryptClickedMock.assert_not_called()
        decryptClickedMock.assert_called_once()

def test_CheckFileEncryptionStatusReturnsCorrectEncryptedStatusAndUpdatesSelectedFile(EncryptionManager):    
    EncryptionManager.pathToFile = TEST_FILE_PATH
    
    assert False == EncryptionManager.checkSelectedFileEncryptionStatus(TEST_FILE)
    assert TEST_FILE == EncryptionManager.selectedFile

    assert True == EncryptionManager.checkSelectedFileEncryptionStatus(TEST_FILE + '.enc')
    assert TEST_FILE + '.enc' == EncryptionManager.selectedFile
    



