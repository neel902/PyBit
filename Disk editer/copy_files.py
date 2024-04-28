import win32clipboard 

def get_copied_file():
    win32clipboard.OpenClipboard()
    try:
        # Check if the clipboard contains a file drop list
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_HDROP):
            # Get the list of copied file paths
            file_list = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
            # For demonstration purposes, print the first file path in the list
            if file_list:
                path = file_list[0]
            with open(path) as f:
                return f.read()
    finally:
        win32clipboard.CloseClipboard()
def get_copied_file_path():
    win32clipboard.OpenClipboard()
    try:
        # Check if the clipboard contains a file drop list
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_HDROP):
            # Get the list of copied file paths
            file_list = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
            # For demonstration purposes, print the first file path in the list
            if file_list:
                return file_list[0]
    finally:
        win32clipboard.CloseClipboard()
import clr
clr.AddReference('System.Collections.Specialized') # type: ignore
clr.AddReference('System.Windows.Forms') # type: ignore
from System.Collections.Specialized import StringCollection # type: ignore
from System.Windows.Forms import Clipboard # type: ignore
import ctypes
import tempfile
import os

# Function to copy a virtual file (name and content) to the clipboard
def copy_virtual_file_to_clipboard(file_name, file_content):
    # Create a temporary file

    try:
        with open("C:\\Users\\neeld\\AppData\\Local\\Temp\\" + file_name, "x") as temp_file:
            temp_file.write(file_content)
    except:
        with open("C:\\Users\\neeld\\AppData\\Local\\Temp\\" + file_name, "w") as temp_file:
            temp_file.write(file_content)

    # Get the full path of the temporary file
    temp_file_path = os.path.abspath(temp_file.name)

    file_path = temp_file_path

    files = StringCollection()
    files.Add(file_path)

    Clipboard.SetFileDropList(files)