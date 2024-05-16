

import sqlite3
import tkinter as tk
from tkinter import messagebox
import json

def create_table():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS library (
                   borrower TEXT PRIMARY KEY,
                   book TEXT,
                   days INTEGER 
    )''')
    conn.commit()
    conn.close()

def list_borrowers():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM library''')
    borrowers = cursor.fetchall()
    conn.close()
    return borrowers

def add_borrower():
    borrower = borrower_entry.get()
    book = book_entry.get()
    days = int(days_entry.get())
    if borrower and book and days:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM library WHERE book = ?''', (book,))
        existing_entry = cursor.fetchone()
        if existing_entry:
            messagebox.showerror("Error", f"The book {book} is already borrowed.")
        else:
            cursor.execute('''INSERT INTO library (borrower, book, days) VALUES (?, ?, ?)''', (borrower, book, days))
            conn.commit()
            conn.close()
            update_listbox()
            borrower_entry.delete(0, tk.END)
            book_entry.delete(0, tk.END)
            days_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please enter all details.")

def update_listbox():
    borrowers_listbox.delete(0, tk.END)
    borrowers = list_borrowers()
    for borrower in borrowers:
        borrowers_listbox.insert(tk.END, borrower)

def remove_borrower():
    selection = borrowers_listbox.curselection()
    if selection:
        borrower = borrowers_listbox.get(selection[0])[0]
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM library WHERE borrower = ?''', (borrower,))
        conn.commit()
        conn.close()
        update_listbox()
    else:
        messagebox.showerror("Error")

def load_theme(theme_file):
    with open(theme_file, 'r', encoding='utf-8') as file:
        return json.load(file)

def switch_theme():
    global CURRENT_THEME, THEMES # Pylint complains about this due to order of reference.
    # No problem here.
    CURRENT_THEME = (CURRENT_THEME + 1) % len(THEMES)
    # Make sure the theme selection falls between 0 and 1.
    apply_theme(THEMES[CURRENT_THEME]) # 0...1, either darkor light.

def apply_theme(theme):
    app.configure(bg=theme['background'])
    borrower_label.configure(bg=theme['background'], fg=theme['foreground'])
    book_label.configure(bg=theme['background'], fg=theme['foreground'])
    days_label.configure(bg=theme['background'], fg=theme['foreground'])
    borrower_entry.configure(bg=theme['background'], fg=theme['foreground'], insertbackground=theme['cursor_color'])
    book_entry.configure(bg=theme['background'], fg=theme['foreground'], insertbackground=theme['cursor_color'])
    days_entry.configure(bg=theme['background'], fg=theme['foreground'], insertbackground=theme['cursor_color'])
    add_button.configure(bg=theme['button_bg'], fg=theme['button_fg'])
    remove_button.configure(bg=theme['button_bg'], fg=theme['button_fg'])
    switch_theme_button.configure(bg=theme['button_bg'], fg=theme['button_fg'])

create_table()

blue_theme = load_theme('blue_theme.json')
red_theme = load_theme('red_theme.json')
THEMES = [blue_theme, red_theme]
CURRENT_THEME = 0

app = tk.Tk()
app.title("Library")
WINDOW_WIDTH = 325
WINDOW_HEIGHT = 450
SCREEN_WIDTH = app.winfo_screenwidth()
SCREEN_HEIGHT = app.winfo_screenheight()
x_coordinate = (SCREEN_WIDTH - WINDOW_WIDTH) // 2
y_coordinate = (SCREEN_HEIGHT - WINDOW_HEIGHT) // 2
app.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x_coordinate}+{y_coordinate}")
app.resizable(False, False)

borrower_label = tk.Label(app, text="Borrower:")
borrower_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

borrower_entry = tk.Entry(app)
borrower_entry.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

book_label = tk.Label(app, text="Book:")
book_label.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

book_entry = tk.Entry(app)
book_entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

days_label = tk.Label(app, text="Days lending:")
days_label.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

days_entry = tk.Entry(app)
days_entry.grid(row=2,column=1, padx=10, pady=10, sticky="nsew")

add_button = tk.Button(app, text="Add borrower info:", command=add_borrower)
add_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

borrowers_listbox = tk.Listbox(app, width=50)
borrowers_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
update_listbox()

remove_button = tk.Button(app, text="Remove borrower info:", command=remove_borrower)
remove_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

theme_button = tk.Button(app, text="Switch theme", command="")
theme_button.grid(row=6,  column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

switch_theme_button = tk.Button(app, text="Switch theme", command=switch_theme)
switch_theme_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

apply_theme(THEMES[CURRENT_THEME])

app.mainloop()