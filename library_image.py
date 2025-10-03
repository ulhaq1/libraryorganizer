import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
def open_image_drawer(root): 
    file=filedialog.askopenfilename()
    if not file: return
    img=Image.open(file)
    win=tk.Toplevel(root); win.title("Image Viewer")
    tk.Label(win,image=ImageTk.PhotoImage(img)).pack()
