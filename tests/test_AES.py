import pytest
from unittest.mock import MagicMock, mock_open, patch, call
import random, string
import lib.EncryptionMethods.AES as AES_METHODS
from Crypto.Util.Padding import unpad, pad

FIRST_KEY = 0
SECOND_KEY = 1
THRID_KEY = 2

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

@pytest.fixture
def MockCipher(mocker):
    mock_aes_new = mocker.patch('lib.EncryptionMethods.AES.AES.new', return_value = MagicMock())  
    mock_random_bytes = mocker.patch('lib.EncryptionMethods.AES.get_random_bytes', return_value = RANDOM_BYTES)  
    return mock_aes_new

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
    newMock = MockCipher
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
