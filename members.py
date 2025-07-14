import tkinter as tk
import sqlite3
import theme_config
from tkinter import messagebox, ttk
from utils import apply_theme

def manage_members():
    def add_member():
        name = e_name.get()
        phone = e_phone.get()
        email = e_email.get()
        if not name or not phone or not email:
            messagebox.showwarning("Missing Info", "Please enter Name, Phone, and Email.")
            return
        conn = sqlite3.connect("library.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO members (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
        conn.commit()
        conn.close()
        e_name.delete(0, tk.END)
        e_phone.delete(0, tk.END)
        e_email.delete(0, tk.END)
        show_members()

    def show_members():
        for row in listbox.get_children():
            listbox.delete(row)
        conn = sqlite3.connect("library.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM members")
        for row in cur.fetchall():
            listbox.insert('', tk.END, values=row)
        conn.close()

    def on_row_select(event):
        selected = listbox.selection()
        if selected:
            values = listbox.item(selected[0], 'values')
            e_name.delete(0, tk.END)
            e_phone.delete(0, tk.END)
            e_email.delete(0, tk.END)
            e_name.insert(0, values[1])
            e_phone.insert(0, values[2])
            e_email.insert(0, values[3])

    def edit_member():
        selected = listbox.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select a member to edit.")
            return
        member_id = listbox.item(selected[0])["values"][0]
        name = e_name.get()
        phone = e_phone.get()
        email = e_email.get()
        if not name or not phone or not email:
            messagebox.showwarning("Missing Info", "Name, Phone, and Email cannot be empty.")
            return
        conn = sqlite3.connect("library.db")
        cur = conn.cursor()
        cur.execute("UPDATE members SET name=?, phone=?, email=? WHERE id=?", (name, phone, email, member_id))
        conn.commit()
        conn.close()
        show_members()

    def delete_member():
        selected = listbox.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select a member to delete.")
            return
        member_id = listbox.item(selected[0])["values"][0]
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this member?")
        if confirm:
            conn = sqlite3.connect("library.db")
            cur = conn.cursor()
            cur.execute("DELETE FROM members WHERE id=?", (member_id,))
            conn.commit()
            conn.close()
            show_members()
            e_name.delete(0, tk.END)
            e_phone.delete(0, tk.END)
            e_email.delete(0, tk.END)

    win = tk.Toplevel()
    win.title("Manage Members")
    apply_theme(win, theme_config.current_theme)

    tk.Label(win, text="Name").grid(row=0, column=0, padx=10, pady=5)
    e_name = tk.Entry(win)
    e_name.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(win, text="Phone").grid(row=1, column=0, padx=10, pady=5)
    e_phone = tk.Entry(win)
    e_phone.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(win, text="Email").grid(row=2, column=0, padx=10, pady=5)
    e_email = tk.Entry(win)
    e_email.grid(row=2, column=1, padx=10, pady=5)

    tk.Button(win, text="Add Member", command=add_member).grid(row=3, column=0, pady=10)
    tk.Button(win, text="Edit Selected", command=edit_member).grid(row=3, column=1, pady=10)
    tk.Button(win, text="Delete Selected", command=delete_member).grid(row=3, column=2, pady=10)

    listbox = ttk.Treeview(win, columns=("ID", "Name", "Phone", "Email"), show="headings")
    listbox.heading("ID", text="ID")
    listbox.heading("Name", text="Name")
    listbox.heading("Phone", text="Phone")
    listbox.heading("Email", text="Email")
    listbox.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    listbox.bind("<<TreeviewSelect>>", on_row_select)
    show_members()
