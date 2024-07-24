import pytest
from unittest.mock import MagicMock, patch, call
import src.lib.Restyle as Restyle
from gi.repository import Gtk as gtk

DECRYPT_BUTTON_STYLE_CLASS = 'redButtonWhiteText'
ENCRYPT_BUTTON_STYLE_CLASS = 'greenButtonWhiteText'
DISABLED_BUTTON_STYLE_CLASS = 'disabledButton'
FIRST_STYLE = 0
SECOND_STYLE = 1

STYLE_CLASSES_LIST = [
    'arbitraryColorClass1',
    'arbitraryColorClass2'
]

@pytest.fixture
def MockCSSProvider(mocker):
    mocker.patch('gi.repository.Gtk.CssProvider')    
    return mocker

def prepareMocks(mockProvider):
    cssProviderMock = gtk.CssProvider.return_value 
    cssProviderMock.load_from_data = MagicMock()

    styleContextMock = MagicMock()
    styleContextMock.remove_class = MagicMock()
    styleContextMock.add_provider = MagicMock()
    styleContextMock.add_class = MagicMock()
    styleContextMock.list_classes.return_value = STYLE_CLASSES_LIST

    buttonMock = MagicMock(spec=gtk.Button)
    buttonMock.get_style_context.return_value = styleContextMock
    buttonMock.set_sensitive = MagicMock()
    buttonMock.set_label = MagicMock()

    return cssProviderMock, styleContextMock, buttonMock

#<<<<<<<<<<<<<<<<<<<< Begin Tests >>>>>>>>>>>>>>>>>>>>
def test_MakeButtonGreenClearsPreExistingSyleClassesAndAddsGreenButtonStyleClassAndEditsText(MockCSSProvider):
    cssProviderMock, styleContextMock, buttonMock = prepareMocks(MockCSSProvider)
    Restyle.makeButtonGreen(buttonMock)

    buttonMock.set_label.assert_called_once_with('Encrypt')
    
    styleContextMock.list_classes.assert_called_once()
    styleContextMock.remove_class.assert_has_calls([call(STYLE_CLASSES_LIST[FIRST_STYLE]), call(STYLE_CLASSES_LIST[SECOND_STYLE])], any_order=False)
    styleContextMock.add_provider.assert_called_once_with(cssProviderMock, gtk.STYLE_PROVIDER_PRIORITY_USER)
    styleContextMock.add_class.assert_called_once_with(ENCRYPT_BUTTON_STYLE_CLASS)

###########################################################################
def test_MakeButtonRedClearsPreExistingSyleClassesAndAddsRedButtonWhiteTextClassAndEditsText(MockCSSProvider):
    cssProviderMock, styleContextMock, buttonMock = prepareMocks(MockCSSProvider)
    Restyle.makeButtonRed(buttonMock)
    
    buttonMock.set_label.assert_called_once_with('Decrypt')

    styleContextMock.list_classes.assert_called_once()
    styleContextMock.remove_class.assert_has_calls([call(STYLE_CLASSES_LIST[FIRST_STYLE]), call(STYLE_CLASSES_LIST[SECOND_STYLE])], any_order=False) 
    styleContextMock.add_provider.assert_called_once_with(cssProviderMock, gtk.STYLE_PROVIDER_PRIORITY_USER)
    styleContextMock.add_class.assert_called_once_with(DECRYPT_BUTTON_STYLE_CLASS)

###########################################################################
def test_ClearButtonWillRemoveAllStyleClassesAndSetSensitivityToFalseAndChangeLabelToEncrypt(MockCSSProvider):
    cssProviderMock, styleContextMock, buttonMock = prepareMocks(MockCSSProvider)
    Restyle.disableButton(buttonMock)

    buttonMock.set_label.assert_called_once_with('Encrypt')
    buttonMock.set_sensitive.assert_called_once_with(False)

    styleContextMock.list_classes.assert_called_once()
    styleContextMock.remove_class.assert_has_calls([call(STYLE_CLASSES_LIST[FIRST_STYLE]), call(STYLE_CLASSES_LIST[SECOND_STYLE])], any_order=False) 
    styleContextMock.add_provider.assert_called_once_with(cssProviderMock, gtk.STYLE_PROVIDER_PRIORITY_USER)
    styleContextMock.add_class.assert_called_once_with(DISABLED_BUTTON_STYLE_CLASS)
