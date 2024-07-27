import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
import pytest
from unittest.mock import MagicMock, patch, call
from src.lib.KeyPrompts import EncryptionPrompt, DecryptionPrompt  # Adjust import as necessary

gi_repo = 'gi.repository.Gtk.'

#<<<<<<<<<<<<<<<<<<<< Begin Encryption Prompt >>>>>>>>>>>>>>>>>>>>
@pytest.fixture
def EPrompt():
    prompt = EncryptionPrompt(None)
    return prompt

#<<<<<<<<<<<<<<<<<<<< Begin Tests >>>>>>>>>>>>>>>>>>>>
def test_OnEncryptionPromptCreationExpectCorrectSettingsOnWidgets():    
    #gtk.Entry will return a mock
    with patch(gi_repo + 'Entry') as gtk_entry_MOCK, \
         patch(gi_repo + 'Dialog.get_content_area'): 
    
        firstEntryMock = MagicMock(spec=gtk.Entry)
        firstEntryMock.set_visibility = MagicMock()
        firstEntryMock.grab_focus = MagicMock()

        secondEntryMock = MagicMock(spec=gtk.Entry)
        secondEntryMock.connect = MagicMock()
        secondEntryMock.set_visibility = MagicMock()
        secondEntryMock.set_placeholder_text = MagicMock()

        #every time gtk.Entry is made, it will instead return an element of the list in order
        gtk_entry_MOCK.side_effect = [firstEntryMock, secondEntryMock]
    
        prompt = EncryptionPrompt(None)
        
        firstEntryMock.set_visibility.assert_called_once_with(False)
        firstEntryMock.grab_focus.assert_called_once()
        
        second_entry_connect_expected_calls = [
                call("changed", prompt.OnTextEntryChanged),  # Call to connect "changed" to OnTextEntryChanged
                call("activate", prompt.EnterKeyPressed)  # Call to connect "activate" to OnEnterKeyPressed
            ]

        secondEntryMock.set_visibility.assert_called_once_with(False)
        secondEntryMock.set_placeholder_text.assert_called_once_with("Repeat Password")
        secondEntryMock.connect.assert_has_calls(second_entry_connect_expected_calls, any_order=False) #items in 'expected_calls' are invoked in the order they appear
        assert secondEntryMock.connect.call_count == 2        

        assert prompt.entriesMatch == False
        assert prompt.OKButton.get_sensitive() == False        

###########################################################################
def test_WhenTextInSecondEntryIsChangedToMatchFirstEntryTextThenEnableOKButton(EPrompt):
    with patch.object(EPrompt.OKButton, 'set_sensitive') as set_sensitive_MOCK, \
         patch.object(EPrompt.firstEntry, 'get_text', return_value='ArbitraryPassword'), \
         patch.object(EPrompt.secondEntry, 'get_text', return_value='ArbitraryPassword'):
                
        entry = MagicMock()
        entry.get_text.return_value ='ArbitraryPassword'
        EPrompt.OnTextEntryChanged(entry)

        set_sensitive_MOCK.assert_called_once_with(True)
        assert EPrompt.entriesMatch == True

###########################################################################
def test_WhenTextInSecondEntryIsChangedAndDoesntMatchFirstEntryTextThenOKButtonRemainsDisabled(EPrompt):
    with patch.object(EPrompt.OKButton, 'set_sensitive') as set_sensitive_MOCK, \
         patch.object(EPrompt.firstEntry, 'get_text', return_value='ArbitraryPassword'), \
         patch.object(EPrompt.secondEntry, 'get_text', return_value='WrongPassword'):
                
        entry = MagicMock()
        entry.get_text.return_value ='WrongPassword'
        EPrompt.OnTextEntryChanged(entry)

        set_sensitive_MOCK.assert_called_once_with(False)
        assert EPrompt.entriesMatch == False

###########################################################################
def test_EncryptionPromptGetEntryMethodReturnsWhateverIsInTheSecondInputField(EPrompt):
    with patch.object(EPrompt.secondEntry, 'get_text', return_value='ArbitraryPassword') as second_entry_get_text_MOCK:
        assert EPrompt.get_entry() == 'ArbitraryPassword'

###########################################################################    
#Bug found on pressing 'Enter' key will cause ResponseType.OK to be returned, regardless of passwords matching
def test_OnEnterKeyPressedAndPasswordsMatchExpectPromptToReturnOK(EPrompt):
    assert EPrompt.entriesMatch == False
    with patch.object(EPrompt.firstEntry, 'get_text', return_value="ArbitraryPassword"), \
         patch.object(EPrompt.secondEntry, 'get_text', return_value="ArbitraryPassword"), \
         patch(gi_repo + 'Dialog.response') as response_MOCK:
        
        EPrompt.OnTextEntryChanged(EPrompt.secondEntry)
        assert EPrompt.entriesMatch == True

        EPrompt.EnterKeyPressed(None)
        response_MOCK.assert_called_once_with(gtk.ResponseType.OK)

###########################################################################
#Bug found on pressing 'Enter' key will cause ResponseType.OK to be returned, regardless of passwords matching
def test_OnEnterKeyPressedAndPasswordsDontMatchExpectPromptToDisregard(EPrompt):
    assert EPrompt.entriesMatch == False
    with patch.object(EPrompt.firstEntry, 'get_text', return_value="ArbitraryPassword1"), \
         patch.object(EPrompt.secondEntry, 'get_text', return_value="ArbitraryPassword2"), \
         patch(gi_repo + 'Dialog.response') as response_MOCK, \
         patch.object(EPrompt.OKButton, 'set_sensitive') as set_sensitive_MOCK:

        
        EPrompt.OnTextEntryChanged(EPrompt.secondEntry)
        assert EPrompt.entriesMatch == False
        set_sensitive_MOCK.assert_called_once_with(False) #Implicit testing passwords of equal length still need to match

        EPrompt.EnterKeyPressed(None)
        response_MOCK.assert_not_called()

#<<<<<<<<<<<<<<<<<<<< End Encryption Prompt >>>>>>>>>>>>>>>>>>>>

#<<<<<<<<<<<<<<<<<<<< Begin Decryption Prompt >>>>>>>>>>>>>>>>>>>>
@pytest.fixture
def DPrompt():
    prompt = DecryptionPrompt(None)
    return prompt

#<<<<<<<<<<<<<<<<<<<< Begin Tests >>>>>>>>>>>>>>>>>>>>
def test_OnDecryptionPromptCreationExpectCorrectSettingsOnWidgets():
    with patch(gi_repo + 'Entry') as gtk_entry_MOCK, \
         patch(gi_repo + 'Dialog.get_content_area'):
         
        entryMock = MagicMock()
        entryMock.set_visibility = MagicMock()
        entryMock.grab_focus = MagicMock()
        entryMock.connect = MagicMock()
        gtk_entry_MOCK.return_value = entryMock
        
        prompt = DecryptionPrompt(None)
        entryMock.set_visibility.assert_called_once_with(False)
        entryMock.grab_focus.assert_called_once()

        entry_connect_expected_calls = [
            call("activate", prompt.OnEnterKeyPressed), 
            call("changed", prompt.OnTextEntryChanged)
        ]

        entryMock.connect.assert_has_calls(entry_connect_expected_calls, any_order=False)
        assert entryMock.connect.call_count == 2        
        
        assert prompt.OKButton.get_sensitive() == False

###########################################################################
def test_OnTextEntryChangedExpectOKButtonToBetSensitiveWhenTextEntryGreaterThanZero(DPrompt):    
    assert DPrompt.OKButton.get_sensitive() == False
    
    entry = MagicMock()
    entry.get_text = MagicMock()
    firstPasswordEntry = ''
    secondPasswordEntry = 'ArbitraryPassword'
    entry.get_text.side_effect = [firstPasswordEntry, secondPasswordEntry]    
    
    DPrompt.OnTextEntryChanged(entry)
    assert DPrompt.OKButton.get_sensitive() == False

    DPrompt.OnTextEntryChanged(entry)
    assert DPrompt.OKButton.get_sensitive() == True

###########################################################################
def test_DecryptionPromptGetEntryMethodReturnsWhateverIsInTheInputField(DPrompt):
    with patch.object(DPrompt.entry, 'get_text', return_value='ArbitraryPassword'):
        assert DPrompt.get_entry() == 'ArbitraryPassword'

    with patch.object(DPrompt.entry, 'get_text', return_value='AnotherPassword'):
        assert DPrompt.get_entry() == 'AnotherPassword'

###########################################################################
def test_OnEnterKeyPressedAndEntryHasInputExpectResponseTypeOK(DPrompt):
    PasswordEntries = ['', 'ArbitraryPassword']
    with patch.object(DPrompt.entry, 'get_text', side_effect=PasswordEntries), \
         patch(gi_repo + 'Dialog.response') as response_MOCK:
        
        DPrompt.OnEnterKeyPressed(DPrompt.entry)
        assert DPrompt.entry.get_text.call_count == 1
        response_MOCK.assert_not_called()

        DPrompt.OnEnterKeyPressed(DPrompt.entry)
        assert DPrompt.entry.get_text.call_count == 2
        response_MOCK.assert_called_once_with(gtk.ResponseType.OK)

#<<<<<<<<<<<<<<<<<<<< End Decryption Prompt >>>>>>>>>>>>>>>>>>>>
