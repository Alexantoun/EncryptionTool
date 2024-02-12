import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Inside the function, we retrieve the style context of the button using get_style_context().
# We then add the specified style class to the button using the add_class() method of the style context.

# This method allows you to apply a CSS style class to the GTK button, and you can define the corresponding styles in your CSS file using the specified style class.

def makeGreenButton(button):
    print('Modifying button color')
    cssProvider = Gtk.CssProvider()
    cssProvider.load_from_data(GREEN_BACKGROUND_WHITE_TEXT_STYLES.encode())
    styleContext = button.get_style_context()
    styleContext.remove_class('text-button')
    styleContext.add_provider(cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_USER) #need to override the gnome theme 
    button.get_style_context().add_class('greenButtonWhiteText')
 
 #Gtk has a known issue where background-color doesnt work so use backgroun-image instead
GREEN_BACKGROUND_WHITE_TEXT_STYLES = """
    .greenButtonWhiteText {
        background-image: image(#4e9a06); 
        color: white; font-weight: bold;
    }

    .greenButtonWhiteText:active{
        background-image: image(#4E7A06); 
        color: white; font-weight: bold;
    }

    """#active state will have slightly darker green color

