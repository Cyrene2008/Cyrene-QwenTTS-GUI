import sys
import os

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, 'frozen'):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        # In onedir mode, _MEIPASS is the _internal directory
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)
