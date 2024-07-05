#!/usr/bin/env python3
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib')))

import src.AAA_EncryptionToolMain
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

if __name__ == '__main__':
    print('Running AAA_EncryptionTool application')
    main = src.AAA_EncryptionToolMain.EncryptionTool()
    gtk.main()