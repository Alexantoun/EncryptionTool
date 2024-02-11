import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Do this,
# def applyStyleClass(button, style_class):
#     style_context = button.get_style_context()
#     style_context.add_class(style_class)

# Inside the function, we retrieve the style context of the button using get_style_context().
# We then add the specified style class to the button using the add_class() method of the style context.

# This method allows you to apply a CSS style class to the GTK button, and you can define the corresponding styles in your CSS file using the specified style class.