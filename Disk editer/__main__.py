import json
import tkinter as tk
from tkinter import scrolledtext

import os

displayed_files = []

from file_extensions import file_icons
from copy_files import *

def get_files(json_data, directory="/"):
    global displayed_files
    displayed_files = []
    files = []
    for path in json_data.keys():
        if path.startswith(directory):
            file_path = path[len(directory):]
            if '/' in file_path:
                folder_name = file_path.split('/')[0]
                if folder_name not in files:
                    files.append(folder_name)
            else:
                files.append(file_path)
    return files

def getEnding(name : str):
    inverse = name[::-1]
    i = inverse.find(".")
    return inverse[:i][::-1]
def update_display(selected_directory="/"):
    files = get_files(json_data, selected_directory)
    listbox.delete(0, tk.END)
    for file in files:
        if (current_directory.get() + file in (json_data.keys())):
            if getEnding(file) in file_icons.keys():
                icon = file_icons[getEnding(file)]
            else:
                icon = file_icons["txt"]
            listbox.insert(tk.END, icon + file)
        else:
            listbox.insert(tk.END, file_icons["folder"] + file + "/")
        displayed_files.append(file)

path = ""

def on_select(event):
    selected_index = listbox.curselection()
    if selected_index:
        selected_file = displayed_files[selected_index[0]]
        selected_path = current_directory.get() + selected_file
        global path, enabled
        path = selected_path
        if selected_path in json_data:
            content = json_data[selected_path]
            text_editor.delete(1.0, tk.END)
            text_editor.insert(tk.END, content)
            text_editor.config(state=tk.NORMAL)
            enabled = True
        else:
            current_directory.set(selected_path + '/')
            update_display(selected_path + '/')
            text_editor.config(state=tk.DISABLED)
            enabled = False

def go_back():
    current_path = current_directory.get()
    if current_path != "/":
        parent_path = "/".join(current_path.rstrip("/").split("/")[:-1]) + "/"
        current_directory.set(parent_path)
        update_display(parent_path)

real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)
abs_path = os.path.dirname(dir_path)
diskTest = (abs_path + "\\Scripts\\disk.json")

if os.path.exists(diskTest):
    disk = diskTest
    print("VFS Path found succesfully")
else:
    disk = input("VFS Path: ")

enabled = False

def enable_editor():
    global enabled
    if enabled:
        json_data[path] = text_editor.get(1.0, tk.END)
        with open(disk, "w") as f:
            json.dump(json_data, f)

# Load JSON data
with open(disk, "r") as file:
    json_data = json.load(file)

def new_file():
    name = new_entry.get()
    path = current_directory.get() + name
    json_data[path] = "# New file"
    with open(disk, "w") as f:
        json.dump(json_data, f)
    update_display(current_directory.get())

def rename_file():
    selected_index = listbox.curselection()
    if selected_index:
        selected_file = displayed_files[selected_index[0]]
        selected_path = current_directory.get() + selected_file
        name = new_entry.get()
        path = current_directory.get() + name
        json_data[path] = json_data[selected_path]
        json_data.pop(selected_path)
        with open(disk, "w") as f:
            json.dump(json_data, f)
        update_display(current_directory.get())

def delete_file():
    global path
    if path in json_data:
        json_data.pop(path)
        with open(disk, "w") as f:
            json.dump(json_data, f)
        update_display(current_directory.get())

def refresh():
    update_display(current_directory.get())

# Create the main window
root = tk.Tk()
root.title("📁 VFS Explorer")

# Current directory label
current_directory = tk.StringVar()
current_directory.set("/")
directory_label = tk.Label(root, textvariable=current_directory)
directory_label.pack()

# Listbox to display files and folders
listbox = tk.Listbox(root, selectmode=tk.SINGLE, font=("Segoe UI Semibold", 12))
listbox.pack(fill=tk.BOTH, expand=True)
update_display()

# Text editor
text_editor = scrolledtext.ScrolledText(root, wrap=tk.WORD)
text_editor.pack()
text_editor.config(state=tk.DISABLED)

# Menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File Menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Delete", command=delete_file)
file_menu.add_command(label="Rename", command=rename_file)
file_menu.add_command(label="Save", command=enable_editor)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# View Menu
view_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Refresh", command=refresh)
view_menu.add_command(label="Back", command=go_back)
#Entry to new file
new_entry = tk.Entry(root)
new_entry.pack()
def on_paste(*args):
    file = get_copied_file()
    nname = get_copied_file_path()
    if file and nname:
        inverse = nname[::-1]
        i = inverse.find("\\")
        name = inverse[:i][::-1]
        path = current_directory.get() + name
        json_data[path] = file
        with open(disk, "w") as f:
            json.dump(json_data, f)
        update_display(current_directory.get())

def on_copy(*args):
    selected_index = listbox.curselection()
    if selected_index:
        selected_file = displayed_files[selected_index[0]]
        selected_path = current_directory.get() + selected_file
    copy_virtual_file_to_clipboard(selected_file, json_data[selected_path])

# Bind events
listbox.bind("<<ListboxSelect>>", on_select)
root.bind("<Control-v>", on_paste)
root.bind("<Control-c>", on_copy)
# Run the application
root.mainloop()
