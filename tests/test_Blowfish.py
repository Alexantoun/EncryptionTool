import pytest
from unittest.mock import MagicMock, patch, mock_open
import lib.EncryptionMethods.Blowfish as Blowfish

RANDOM_BYTES = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F\x10'

@pytest.fixture
def MockCipher(mocker):
    mock_blowfish_new = mocker.patch('lib.EncryptionMethods.Blowfish.Blowfish.new', return_value=MagicMock())
    mock_random = mocker.patch('lib.EncryptionMethods.Blowfish.get_random_bytes', return_value = RANDOM_BYTES)
    return mock_blowfish_new

@patch("builtins.open", new_callable=mock_open, read_data=b"mocked file data")
def test_OnBlowfishEncryptExpectEncryptedCopyOfSelectedFile(mock_open, MockCipher):
    newMock = MockCipher
    result = Blowfish.get_random_bytes(16)
    
    assert result == RANDOM_BYTES

    Blowfish.Encrypt('test_file.txt', 'someKey')

    newMock.assert_called_once_with(
        b'someKey',
        Blowfish.Blowfish.MODE_CBC,
        RANDOM_BYTES
    )

    mock_open.assert_any_call('test_file.txt', 'rb')
    mock_open.assert_any_call('test_file.txt.enc', 'wb')

    