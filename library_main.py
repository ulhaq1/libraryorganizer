# Library Organizer - GUI Frontend (Tkinter)
# Refactored for clean entrypoint and testability

import os, json, tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, List, Dict
from library_model import add_book, delete_book_by_title, load_book, save_books, update_file_name, how_it_works

try:
    from library_image import open_image_drawer
except Exception:
    def open_image_drawer(*a, **k):
        messagebox.showwarning("Images", "Image feature unavailable")

window=None; text_area=None; title_entry=None; author_entry=None; year_entry=None; status_var=None; selected_library=None; library_combobox=None

def _format_books(books:List[Dict])->str:
    if not books: return "No books in library."
    lines=[f"{i}) {b['title']} by {b['author']}, {b['year']} - Status: {b['status']}" for i,b in enumerate(books,1)]
    lines.append(f"Total Books in the Library = {len(books)}")
    return "\n".join(lines)

def display_books(widget:Optional[tk.Text]=None)->str:
    books=load_book(); formatted=_format_books(books)
    target=widget or text_area
    if target is not None:
        target.delete("1.0", tk.END); target.insert(tk.END, formatted)
    return formatted

def add_book_gui(title=None, author=None, year=None, status=None):
    global title_entry,author_entry,year_entry,status_var
    if title is None and title_entry: title=title_entry.get()
    if author is None and author_entry: author=author_entry.get()
    if year is None and year_entry: year=year_entry.get()
    if status is None and status_var: status=status_var.get()
    if not (title and author and year and status): return
    books=load_book()
    for book in books:
        if book["title"].lower()==title.lower():
            if book["status"] in {"deleted","lent out"}:
                book["status"]="available"; save_books(books); display_books(); return
            else: return
    add_book(title,author,year,status); display_books()

def delete_book_gui(title=None):
    global title_entry
    if title is None and title_entry: title=title_entry.get()
    if not title: return
    delete_book_by_title(title); display_books()

def lend_book_gui(title=None):
    global title_entry
    if title is None and title_entry: title=title_entry.get()
    if not title: return
    books=load_book()
    for book in books:
        if book["title"].lower()==title.lower():
            if book["status"]=="available":
                book["status"]="lent out"; save_books(books); display_books(); return
            else: return

def _open_how_it_works_window():
    hiw=tk.Toplevel(window); hiw.title("How it Works"); hiw.geometry("500x700")
    tk.Label(hiw,text=how_it_works(),justify=tk.LEFT,padx=10,pady=10).pack(fill=tk.BOTH,expand=True)

def _populate_library_list():
    libraries=[f for f in os.listdir() if f.endswith(".json")]
    if not libraries:
        libraries.append("library.json")
        with open("library.json","w") as f: json.dump([],f)
    library_combobox["values"]=libraries; selected_library.set(libraries[0]); update_file_name(selected_library.get())

def run_app():
    global window,text_area,title_entry,author_entry,year_entry,status_var,selected_library,library_combobox
    window=tk.Tk(); window.geometry("650x650"); window.title("Library Organizer")
    selected_library=tk.StringVar(window)
    tk.Label(window,text="Welcome to Library Organizer!",font=("Arial",16)).grid(row=0,column=0,columnspan=3,pady=10)
    tk.Button(window,text="How it Works",command=_open_how_it_works_window).grid(row=1,column=0,columnspan=3,pady=10)
    text_area=tk.Text(window,height=10,width=50); text_area.grid(row=2,column=0,columnspan=3,pady=10)
    tk.Label(window,text="Title:").grid(row=3,column=0,sticky="e"); title_entry=tk.Entry(window,width=40); title_entry.grid(row=3,column=1)
    tk.Label(window,text="Author:").grid(row=4,column=0,sticky="e"); author_entry=tk.Entry(window,width=40); author_entry.grid(row=4,column=1)
    tk.Label(window,text="Year:").grid(row=5,column=0,sticky="e"); year_entry=tk.Entry(window,width=40); year_entry.grid(row=5,column=1)
    tk.Label(window,text="Status:").grid(row=6,column=0,sticky="e"); status_var=tk.StringVar(window,"available")
    tk.OptionMenu(window,status_var,"available","lent out","missing","deleted").grid(row=6,column=1)
    frame=tk.Frame(window); frame.grid(row=7,column=0,columnspan=3,pady=10,sticky="ew")
    for i in range(5): frame.grid_columnconfigure(i,weight=1)
    tk.Button(frame,text="Add Book",command=lambda:add_book_gui()).grid(row=0,column=0,sticky="ew")
    tk.Button(frame,text="Delete Book",command=lambda:delete_book_gui()).grid(row=0,column=1,sticky="ew")
    tk.Button(frame,text="List Books",command=lambda:display_books()).grid(row=0,column=2,sticky="ew")
    tk.Button(frame,text="Lend Out",command=lambda:lend_book_gui()).grid(row=0,column=3,sticky="ew")
    tk.Label(window,text="Select Library:").grid(row=8,column=0); library_combobox=ttk.Combobox(window,textvariable=selected_library,state="readonly",width=40)
    library_combobox.grid(row=8,column=1); tk.Button(window,text="Upload Image",command=lambda:open_image_drawer(window)).grid(row=9,column=0,columnspan=3,pady=10)
    _populate_library_list(); selected_library.set(library_combobox.get())
    def _on_lib(e): update_file_name(selected_library.get()); display_books()
    library_combobox.bind("<<ComboboxSelected>>",_on_lib)
    display_books(); window.mainloop()

if __name__=="__main__": run_app()
