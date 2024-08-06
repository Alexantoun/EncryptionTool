import pytest
from unittest.mock import MagicMock, patch, mock_open, call
import lib.EncryptionMethods.Blowfish as Blowfish
from Crypto.Util.Padding import pad
import Crypto.Cipher.Blowfish

RANDOM_BYTES = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F\x10'
DECRYPTED_DATA = b'Decrypted data'
ENCRYPTED_DATA = b'encrypted data'

def readSideEffect(param = -1):
    if -1 == param:
        return RANDOM_BYTES + b'someData'
    else:
        return RANDOM_BYTES

@pytest.fixture
def MockCipherEncrypt(mocker):
    mock_cipher = MagicMock()
    mock_cipher.encrypt.return_value = ENCRYPTED_DATA
    mock_blowfish_new = mocker.patch('lib.EncryptionMethods.Blowfish.Blowfish.new', return_value=mock_cipher)
    mock_random = mocker.patch('lib.EncryptionMethods.Blowfish.get_random_bytes', return_value = RANDOM_BYTES)
    return mock_blowfish_new, mock_cipher.encrypt

@pytest.fixture
def MockCipherDecrypt(mocker):
    mock_cipher = MagicMock()
    mock_cipher.decrypt.return_value = DECRYPTED_DATA
    mock_blowfish_new = mocker.patch('lib.EncryptionMethods.Blowfish.Blowfish.new', return_value= mock_cipher)
    return mock_blowfish_new, mock_cipher.decrypt

@patch("builtins.open", new_callable=mock_open, read_data=b"mocked file data")
def test_OnBlowfishEncryptExpectEncryptedCopyOfSelectedFile(mock_open, MockCipherEncrypt):
    newMock, encryptMock = MockCipherEncrypt
    fileHandler = mock_open.return_value

    result = Blowfish.get_random_bytes(16)
    assert result == RANDOM_BYTES

    Blowfish.Encrypt('test_file.txt', 'someKey')

    newMock.assert_called_once_with(
        b'someKey',
        Blowfish.Blowfish.MODE_CBC,
        RANDOM_BYTES
    )

    fileData = pad(b'mocked file data', Crypto.Cipher.Blowfish.block_size)
    encryptMock.assert_called_once_with(fileData)
    
    mock_open.assert_any_call('test_file.txt', 'rb')
    mock_open.assert_any_call('test_file.txt.enc', 'wb')
    fileHandler.read.assert_called_once()
    fileHandler.write.assert_called_once_with(RANDOM_BYTES + ENCRYPTED_DATA)

@patch("builtins.open", new_callable=mock_open, read_data=b"mocked file data")
def test_OnBlowfishDecryptExpectDecryptedCopyOfSelectedFile(mock_open, MockCipherDecrypt):
    newMock, decryptMock = MockCipherDecrypt
    fileHandler = mock_open.return_value
    fileHandler.read.side_effect = readSideEffect

    with patch('lib.EncryptionMethods.Blowfish.unpad', return_value = DECRYPTED_DATA):
        
        Blowfish.Decrypt('test_file.txt.enc', 'someKey')
        
        newMock.assert_called_once_with(
        b'someKey',
        Blowfish.Blowfish.MODE_CBC,
        RANDOM_BYTES
        )

        decryptMock.assert_called_once_with(RANDOM_BYTES + b'someData')
        
        mock_open.assert_any_call('test_file.txt', 'wb')
        mock_open.assert_any_call('test_file.txt.enc', 'rb')
        fileHandler.write.assert_called_once_with(DECRYPTED_DATA)
        fileHandler.read.assert_has_calls([call(Blowfish.BLOCK_SIZE), call()])
