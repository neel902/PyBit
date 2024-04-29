import win32clipboard

print("THIS IS A DEPRACATED METHOD, AND WILL SOON BE REMOVED. IT DOESNT EVEN WORK, THERES NO REASON TO USE THIS.")
input("Press enter to continue, or Ctrl+Z+Enter to exit")

def setClipboard(text : str) -> None:
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text)
    win32clipboard.CloseClipboard()

import tkinter as tk
from tkinter.ttk import Scale
from tkinter import colorchooser, filedialog, messagebox
import PIL.ImageGrab as ImageGrab

root = tk.Tk()

root.minsize(300, 200)

colour = "white"

def paint(event):
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    canvas.create_oval(
        x1,
        y1,
        x2,
        y2,
        fill=colour,
        outline=colour,
        width=1,
    )

def COP():
    print("Depracated")

canvas = tk.Canvas(
    root, bg="black", bd=5, relief=tk.GROOVE, height=100, width=150
)
canvas.place(x=10, y=10, anchor="nw")
canvas.bind("<B1-Motion>", paint)

copy = tk.Button(
    root, text="Copy", command=COP
)
copy.place(x=25, y=130, anchor="nw")

root.mainloop()