# import gi
# from gi.repository import Gtk as gtk

NAME_INDEX = 0
SIZE_INDEX = 1
MODIFIED_INDEX = 2

ERROR_NO_INPUT_IN_SEARCH_BAR = '<span foreground="#ff1a1a" weight="normal">No text was entered to search for. Removing filter</span>'
GREEN_ENCRYPT_BUTTON =  '<span background="green" foreground="white" weight="normal">Encrypt</span>'

def FOLDER_SELECTED(path:str) -> str:
    string = '<span foreground="#000000" weight="normal">Displaying content in '+path+'</span>'
    return string

def ERROR_INPUT_NOT_FOUND(input:str) -> str:
    string = '<span foreground="red" weight="Bold">No text was entered to search for</span>'
    return string

# You need to set the widget name in glade or with widget.set_name("example")
# re-type this one
# def apply_button_style(self, button, color):
#     css_provider = Gtk.CssProvider()
#     css_provider.load_from_data(bytes(f".{button.get_name()} {{ background-color: {color}; }}", encoding='utf-8'))
#     style_context = button.get_style_context()
#     style_context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
