import json, os
File_name="library.json"

def update_file_name(new): global File_name; File_name=new
def load_book():
    if not os.path.exists(File_name): return []
    try:
        with open(File_name) as f: return json.load(f)
    except json.JSONDecodeError: return []
def save_books(books): open(File_name,"w").write(json.dumps(books,indent=4))
def add_book(title,author,year,status):
    books=load_book()
    for b in books:
        if b["title"].lower()==title.lower():
            if b["status"] in {"deleted","lent out"}: b["status"]="available"; save_books(books); return
            else: return
    books.append({"title":title,"author":author,"year":int(year),"status":status}); save_books(books)
def delete_book_by_title(title):
    books=load_book(); matches=[b for b in books if b["title"].lower()==title.lower()]
    if matches: matches[-1]["status"]="deleted"; save_books(books)
def how_it_works(): return "Add/Delete/List/Search/Lend books in JSON libraries."
