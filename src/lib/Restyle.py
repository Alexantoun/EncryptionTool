import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

###########################################################################
def makeButtonGreen(button):
    print('Modifying button color to green')
    cssProvider = Gtk.CssProvider()
    cssProvider.load_from_data(GREEN_BACKGROUND_WHITE_TEXT_STYLES.encode())
    
    styleContext = button.get_style_context()
    classes = styleContext.list_classes()
    button.set_label('Encrypt')
    for styleClass in classes:
        styleContext.remove_class(styleClass)

    styleContext.add_provider(cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
    styleContext.add_class('greenButtonWhiteText')

###########################################################################
def makeButtonRed(button):
    print('Modifying button color to red')
    cssProvider = Gtk.CssProvider()
    cssProvider.load_from_data(RED_BACKGROUND_WHITE_TEXT_STYLES.encode())
    
    styleContext = button.get_style_context()
    classes = styleContext.list_classes()
    button.set_label('Decrypt')
    for styleClass in classes:
        styleContext.remove_class(styleClass)

    styleContext.add_provider(cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
    styleContext.add_class('redButtonWhiteText')

###########################################################################
def disableButton(button):
    print('Disabling button')
    cssProvider = Gtk.CssProvider()
    cssProvider.load_from_data(DISABLED_BUTTON_STYLES.encode())

    styleContext = button.get_style_context()
    classes = styleContext.list_classes()
    for styleClass in classes:
        styleContext.remove_class(styleClass)
    
    styleContext.add_provider(cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
    styleContext.add_class('disabledButton')
    button.set_label('Encrypt')
    button.set_sensitive(False)

# Gtk has a known issue where background-color doesnt work so need to use background-image instead
# Active state will have slightly darker green color
GREEN_BACKGROUND_WHITE_TEXT_STYLES = """
    .greenButtonWhiteText {
        background-image: image(#4e9a06); 
        color: white;
        font-weight: bold;
    }

    .greenButtonWhiteText:active {
        background-image: image(#4E6A04); 
    }
    """

RED_BACKGROUND_WHITE_TEXT_STYLES = """
    .redButtonWhiteText {
        background-image: image(#A93B3F); 
        color: white;
        font-weight: bold;
    }

    .redButtonWhiteText:active {
        background-image: image(#902A2D); 
    }
    """

DISABLED_BUTTON_STYLES = """
    .disabledButton {
        background-image: image(#fafafa);
        color: #eaddd2;
        font-weight: normal;
    }
"""