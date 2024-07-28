import pytest
from unittest.mock import MagicMock, patch
from src.lib.FileCipher import AES_CBC as AES, BLOWFISH_CBC as Blowfish

FILE_PATH = '/arbitrary/path'
FILE_NAME = 'arbitrary_Name'
MODULE_PATH_PATCH = 'src.lib.FileCipher.'

AES_ENCRYPT = 0
AES_DECRYPT = 1
BLOWFISH_ENCRYPT = 2
BLOWFISH_DECRYPT = 3

@pytest.fixture
def MockCiphers(mocker):
    modulePath = 'src.lib.FileCipher.'

    aesEncryptMock = mocker.patch(modulePath + 'AES.Encrypt')
    aesDecryptMock = mocker.patch(modulePath + 'AES.Decrypt')
    blowfishEncryptMock = mocker.patch(modulePath + 'Blowfish.Encrypt')
    blowfishDecryptMock = mocker.patch(modulePath + 'Blowfish.Decrypt')

    return {
        AES_ENCRYPT       : aesEncryptMock,
        AES_DECRYPT       : aesDecryptMock,
        BLOWFISH_ENCRYPT  : blowfishEncryptMock,
        BLOWFISH_DECRYPT  : blowfishDecryptMock
    }

#<<<<<<<<<<<<<<<<<<<< Begin AES FileCipher >>>>>>>>>>>>>>>>>>>>
def test_GivenAESSelectedEncryptInvokesAESEncryptMethod(MockCiphers):
    encryptMock = MockCiphers[AES_ENCRYPT]
    cipher = AES()
    cipher.Encrypt(FILE_PATH, FILE_NAME)

    encryptMock.assert_called_once_with(FILE_PATH, FILE_NAME)

###########################################################################
def test_GivenAESSelectedDecryptInvokesAESDecryptMethod(MockCiphers):
    decryptMock = MockCiphers[AES_DECRYPT]
    cipher = AES()
    cipher.Decrypt(FILE_PATH, FILE_NAME)

    decryptMock.assert_called_once_with(FILE_PATH, FILE_NAME)

#<<<<<<<<<<<<<<<<<<<< Begin Blowfish FileCipher >>>>>>>>>>>>>>>>>>>>
def test_GivenBlowfishSelectedEncryptInvokesBlowfishEncryptMethod(MockCiphers):
    encryptMock = MockCiphers[BLOWFISH_ENCRYPT]
    cipher = Blowfish()
    cipher.Encrypt(FILE_PATH, FILE_NAME)

    encryptMock.assert_called_once_with(FILE_PATH, FILE_NAME)

###########################################################################
def test_GivenBlowfishSelectedDecryptInvokesBlowfishDecryptMethod(MockCiphers):
    decryptMock = MockCiphers[BLOWFISH_DECRYPT]
    cipher = Blowfish()
    cipher.Decrypt(FILE_PATH, FILE_NAME)
    
    decryptMock.assert_called_once_with(FILE_PATH, FILE_NAME)

