import sys
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.AAA_EncryptionToolMain import EncryptionTool

def main():
    EncryptionTool()
    gtk.main()

if __name__ == "__main__":
    main()
