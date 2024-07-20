import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
import pytest
from unittest.mock import MagicMock, patch, call
from src.lib.KeyPrompts import EncryptionPrompt  # Adjust import as necessary

@pytest.fixture
def Prompt(): #cant mock out the init method simply but realistically speaking, I'd just be unit testing gtk methods
    prompt = EncryptionPrompt(None)
    return prompt

#<<<<<<<<<<<<<<<<<<<< Begin Tests >>>>>>>>>>>>>>>>>>>>
def test_OnEncryptionPromptCreationExpectCorrectSettingsOnWidgets():    
    #gtk.Entry will return a mock
    with patch('gi.repository.Gtk.Entry') as gtk_entry_MOCK, \
         patch('gi.repository.Gtk.Dialog.get_content_area'): 
    
        firstEntryMock = MagicMock(spec=gtk.Entry)
        firstEntryMock.set_visibility = MagicMock()
        firstEntryMock.grab_focus = MagicMock()

        secondEntryMock = MagicMock(spec=gtk.Entry)
        secondEntryMock.connect = MagicMock()
        secondEntryMock.set_visibility = MagicMock()
        secondEntryMock.set_placeholder_text = MagicMock()

        #every time gtk.Entry is made, it will return an element of the list in the lists order
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

def test_WhenTextInSecondEntryIsChangedToMatchFirstEntryTextThenEnableOKButton(Prompt):
    with patch.object(Prompt.OKButton, 'set_sensitive') as set_sensitive_MOCK, \
         patch.object(Prompt.firstEntry, 'get_text', return_value='ArbitraryPassword') as first_entry_get_text_MOCK, \
         patch.object(Prompt.secondEntry, 'get_text', return_value='ArbitraryPassword') as second_entry_get_text_MOCK:
                
        entry = MagicMock()
        entry.get_text.return_value ='ArbitraryPassword'
        Prompt.OnTextEntryChanged(entry)

        set_sensitive_MOCK.assert_called_once_with(True)

def test_WhenTextInSecondEntryIsChangedAndDoesntMatchFirstEntryTextThenOKButtonRemainsDisabled(Prompt):
    with patch.object(Prompt.OKButton, 'set_sensitive') as set_sensitive_MOCK, \
         patch.object(Prompt.firstEntry, 'get_text', return_value='ArbitraryPassword') as first_entry_get_text_MOCK, \
         patch.object(Prompt.secondEntry, 'get_text', return_value='WrongPassword') as second_entry_get_text_MOCK:
                
        entry = MagicMock()
        entry.get_text.return_value ='WrongPassword'
        Prompt.OnTextEntryChanged(entry)

        set_sensitive_MOCK.assert_called_once_with(False)

def test_EncryptionPromptGetEntryMethodReturnsWhateverIsInTheSecondInputField(Prompt):
    with patch.object(Prompt.secondEntry, 'get_text', return_value='ArbitraryPassword') as second_entry_get_text_MOCK:
        assert Prompt.get_entry() == 'ArbitraryPassword'

def test_OnEnterKeyPushedAndPasswordsMatchThenEncryptionPromptReturnsGTKOK(Prompt):
    Prompt.entriesMatch = True
    

#Bug found on pressing 'Enter' key will cause ResponseType.OK to be returned, regardless of passwords matching