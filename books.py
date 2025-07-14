import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from theme_config import current_theme
from utils import apply_theme

def manage_books():
    def add_book():
        title = e_title.get()
        author = e_author.get()
        if not title or not author:
            messagebox.showwarning("Missing Info", "Please enter both Title and Author.")
            return
        conn = sqlite3.connect("library.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
        conn.commit()
        conn.close()
        e_title.delete(0, tk.END)
        e_author.delete(0, tk.END)
        show_books()

    def show_books(filter_keyword=None):
        for row in listbox.get_children():
            listbox.delete(row)
        conn = sqlite3.connect("library.db")
        cur = conn.cursor()
        if filter_keyword:
            keyword = f"%{filter_keyword}%"
            cur.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", (keyword, keyword))
        else:
            cur.execute("SELECT * FROM books")
        for row in cur.fetchall():
            listbox.insert('', tk.END, values=row)
        conn.close()

    def on_row_select(event):
        selected = listbox.selection()
        if selected:
            values = listbox.item(selected[0], 'values')
            e_title.delete(0, tk.END)
            e_author.delete(0, tk.END)
            e_title.insert(0, values[1])
            e_author.insert(0, values[2])

    def edit_book():
        selected = listbox.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select a book to edit.")
            return
        book_id = listbox.item(selected[0])["values"][0]
        title = e_title.get()
        author = e_author.get()
        if not title or not author:
            messagebox.showwarning("Missing Info", "Title and Author cannot be empty.")
            return
        conn = sqlite3.connect("library.db")
        cur = conn.cursor()
        cur.execute("UPDATE books SET title=?, author=? WHERE id=?", (title, author, book_id))
        conn.commit()
        conn.close()
        show_books()

    def delete_book():
        selected = listbox.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select a book to delete.")
            return
        book_id = listbox.item(selected[0])["values"][0]
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this book?")
        if confirm:
            conn = sqlite3.connect("library.db")
            cur = conn.cursor()
            cur.execute("DELETE FROM books WHERE id=?", (book_id,))
            conn.commit()
            conn.close()
            show_books()
            e_title.delete(0, tk.END)
            e_author.delete(0, tk.END)

    def search_books():
        keyword = e_search.get()
        show_books(keyword)

    def export_to_excel():
        conn = sqlite3.connect("library.db")
        df_books = pd.read_sql_query("SELECT * FROM books", conn)
        df_members = pd.read_sql_query("SELECT * FROM members", conn)
        df_txns = pd.read_sql_query("SELECT * FROM transactions", conn)
        conn.close()
        try:
            with pd.ExcelWriter("library_export.xlsx") as writer:
                df_books.to_excel(writer, index=False, sheet_name="Books")
                df_members.to_excel(writer, index=False, sheet_name="Members")
                df_txns.to_excel(writer, index=False, sheet_name="Transactions")
            messagebox.showinfo("Export Success", "Data exported to library_export.xlsx")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))

    def export_to_pdf():
        try:
            c = canvas.Canvas("library_export.pdf", pagesize=letter)
            conn = sqlite3.connect("library.db")
            cur = conn.cursor()

            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, 750, "Books List")
            cur.execute("SELECT * FROM books")
            data = cur.fetchall()
            y = 730
            c.setFont("Helvetica", 10)
            for row in data:
                c.drawString(50, y, f"ID: {row[0]} | Title: {row[1]} | Author: {row[2]}")
                y -= 15
                if y < 50:
                    c.showPage()
                    y = 750

            y -= 30
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y, "Members List")
            y -= 20
            c.setFont("Helvetica", 10)
            cur.execute("SELECT * FROM members")
            data = cur.fetchall()
            for row in data:
                c.drawString(50, y, f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")
                y -= 15
                if y < 50:
                    c.showPage()
                    y = 750

            y -= 30
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y, "Transactions")
            y -= 20
            c.setFont("Helvetica", 10)
            cur.execute("SELECT * FROM transactions")
            data = cur.fetchall()
            for row in data:
                c.drawString(50, y, f"ID: {row[0]} | Member ID: {row[1]} | Book ID: {row[2]} | Issued: {row[3]} | Returned: {row[4]}")
                y -= 15
                if y < 50:
                    c.showPage()
                    y = 750

            conn.close()
            c.save()
            messagebox.showinfo("Export Success", "Data exported to library_export.pdf")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))

    win = tk.Toplevel()
    win.title("Manage Books")
    win.geometry("700x500")
    apply_theme(win, current_theme)

    tk.Label(win, text="Search (Title/Author)", bg=win['bg'], fg='white' if current_theme == 'dark' else 'black').grid(row=0, column=0, padx=10, pady=5)
    e_search = tk.Entry(win)
    e_search.grid(row=0, column=1, padx=10, pady=5)
    tk.Button(win, text="Search", command=search_books).grid(row=0, column=2, padx=5)
    tk.Button(win, text="Clear", command=lambda: show_books()).grid(row=0, column=3, padx=5)

    tk.Label(win, text="Title", bg=win['bg'], fg='white' if current_theme == 'dark' else 'black').grid(row=1, column=0, padx=10, pady=5)
    e_title = tk.Entry(win)
    e_title.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(win, text="Author", bg=win['bg'], fg='white' if current_theme == 'dark' else 'black').grid(row=2, column=0, padx=10, pady=5)
    e_author = tk.Entry(win)
    e_author.grid(row=2, column=1, padx=10, pady=5)

    tk.Button(win, text="Add Book", command=add_book).grid(row=3, column=0, pady=10)
    tk.Button(win, text="Edit Selected", command=edit_book).grid(row=3, column=1, pady=10)
    tk.Button(win, text="Delete Selected", command=delete_book).grid(row=3, column=2, pady=10)

    tk.Button(win, text="Export to Excel", command=export_to_excel).grid(row=4, column=0, pady=10)
    tk.Button(win, text="Export to PDF", command=export_to_pdf).grid(row=4, column=1, pady=10)

    listbox = ttk.Treeview(win, columns=("ID", "Title", "Author"), show="headings")
    listbox.heading("ID", text="ID")
    listbox.heading("Title", text="Title")
    listbox.heading("Author", text="Author")
    listbox.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

    listbox.bind("<<TreeviewSelect>>", on_row_select)
    show_books()
