import pytest
from unittest.mock import MagicMock, mock_open, patch, call
import random, string
import lib.EncryptionMethods.AES as AES_METHODS
import Crypto.Cipher.AES

RANDOM_BYTES = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F\x10'

def generateRandomKey(lowerBound, upperBound) -> str:
    chars = string.ascii_letters + string.digits + string.punctuation
    length = random.randint(lowerBound + 1, upperBound - 1)
    key = ''.join(random.choice(chars) for _ in range(length))
    assert len(key) < upperBound
    assert len(key) > lowerBound

    return key.encode('utf-8')

def getPaddingString(length) -> str:    
    padding = ''.encode('utf-8').ljust(length, b'\0')
    return padding

def readSideEffect(param=-1):
    if param == -1:
        return RANDOM_BYTES + b'someData'
    else:
        return RANDOM_BYTES

@pytest.fixture
def MockCipher(mocker):
    mock_cipher = MagicMock()
    mock_cipher.decrypt.return_value = b'decrypted_data'  # Set return value for decrypt
    mock_aes_new = mocker.patch('lib.EncryptionMethods.AES.AES.new', return_value=mock_cipher)
    mocker.patch('lib.EncryptionMethods.AES.get_random_bytes', return_value=RANDOM_BYTES)
    
    return mock_aes_new, mock_cipher

def test_GivenKeyOfArbitraryLengthExpectPadKeyToReturnPaddedKeyUpToTheNextAcceptableKeyLength():
    key = generateRandomKey(0, 16)
    keyLengthDelta = 16 - len(key)    
    paddedKey = AES_METHODS.PadKey(key)

    assert len(paddedKey) == 16
    assert paddedKey[:-keyLengthDelta] == key
    assert paddedKey[len(key):] == getPaddingString(keyLengthDelta)

    key = generateRandomKey(16, 24)        
    keyLengthDelta = 24 - len(key)    
    paddedKey = AES_METHODS.PadKey(key)

    assert len(paddedKey) == 24
    assert paddedKey[:-keyLengthDelta] == key
    assert paddedKey[len(key):] == getPaddingString(keyLengthDelta)

    key = generateRandomKey(24, 32)        
    keyLengthDelta = 32 - len(key)    
    paddedKey = AES_METHODS.PadKey(key)

    assert len(paddedKey) == 32
    assert paddedKey[:-keyLengthDelta] == key
    assert paddedKey[len(key):] == getPaddingString(keyLengthDelta)

@patch("builtins.open", new_callable=mock_open, read_data=b"mocked file data")
def test_OnAESEncryptExpectEncryptedCopyOfSelectedFile(mock_open, MockCipher):
    newMock, unused = MockCipher
    result = AES_METHODS.get_random_bytes(16)
    assert result == RANDOM_BYTES 

    AES_METHODS.Encrypt('test_file.txt', 'someKey')
    
    newMock.assert_called_once_with(
        AES_METHODS.PadKey(b'someKey'), 
        AES_METHODS.AES.MODE_CBC, 
        RANDOM_BYTES
    )

    mock_open.assert_any_call('test_file.txt', 'rb')
    mock_open.assert_any_call('test_file.txt.enc', 'wb')
    
@patch("builtins.open", new_callable=mock_open, read_data=b"mocked file data")
def test_OnEASDecryptExpectDecryptedCopyOfSelectedFile(mock_open, MockCipher):
    newMock, decryptMock = MockCipher
    fileHandler = mock_open()
    fileHandler.read.side_effect = readSideEffect
    AES_METHODS.Decrypt('test_file.txt.enc', 'someKey')

    newMock.assert_called_once_with(
        AES_METHODS.PadKey(b'someKey'),
        AES_METHODS.AES.MODE_CBC,
        RANDOM_BYTES
    )

    fileHandler.read.assert_has_calls([call(AES_METHODS.BLOCK_SIZE), call()])
    decryptMock.decrypt.assert_called_once_with(RANDOM_BYTES + b'someData')
    fileHandler.write.assert_called_once()
