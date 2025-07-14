import tkinter as tk
import sqlite3
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import theme_config
from utils import apply_theme
from email_utils import send_email  # Step 1: Import email sending function

def issue_return_books():
    def issue_book():
        member_id = e_member_id.get()
        book_id = e_book_id.get()
        issue_date = datetime.now()
        due_date = issue_date + timedelta(days=14)  # 2 weeks from issue

        conn = sqlite3.connect("library.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO transactions (member_id, book_id, issue_date, due_date) VALUES (?, ?, ?, ?)",
                    (member_id, book_id, issue_date.strftime("%Y-%m-%d"), due_date.strftime("%Y-%m-%d")))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Book issued successfully.")
        e_member_id.delete(0, tk.END)
        e_book_id.delete(0, tk.END)
        show_transactions()

    def return_book():
        selected = listbox.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select a transaction to return.")
            return

        txn_id = listbox.item(selected[0])["values"][0]
        return_date = datetime.now()

        conn = sqlite3.connect("library.db")
        cur = conn.cursor()

        # Get due date and member_id
        cur.execute("SELECT due_date, member_id FROM transactions WHERE id=?", (txn_id,))
        result = cur.fetchone()
        due_date_str, member_id = result
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d")

        # Calculate fine
        fine = 0
        if return_date > due_date:
            days_late = (return_date - due_date).days
            fine = days_late * 5  # ₹5 per day

            # Step 2: Fetch member email and send fine email
            cur.execute("SELECT email, name FROM members WHERE id=?", (member_id,))
            member = cur.fetchone()
            if member:
                email, name = member
                if email:
                    subject = "Library Fine Notice"
                    body = (
                        f"Dear {name},\n\n"
                        f"You returned a book {days_late} day(s) late. A fine of ₹{fine} has been applied.\n"
                        "Please make the payment at the library counter.\n\n"
                        "Thank you."
                    )
                    send_email(email, subject, body)

        # Update transaction
        cur.execute("UPDATE transactions SET return_date=?, fine=? WHERE id=?",
                    (return_date.strftime("%Y-%m-%d"), fine, txn_id))

        conn.commit()
        conn.close()

        messagebox.showinfo("Returned", f"Book returned. Fine: ₹{fine}")
        show_transactions()

    def show_transactions():
        for row in listbox.get_children():
            listbox.delete(row)
        conn = sqlite3.connect("library.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM transactions")
        for row in cur.fetchall():
            listbox.insert('', tk.END, values=row)
        conn.close()

    win = tk.Toplevel()
    win.title("Issue / Return Books")
    apply_theme(win, theme_config.current_theme)

    tk.Label(win, text="Member ID").grid(row=0, column=0, padx=10, pady=5)
    e_member_id = tk.Entry(win)
    e_member_id.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(win, text="Book ID").grid(row=1, column=0, padx=10, pady=5)
    e_book_id = tk.Entry(win)
    e_book_id.grid(row=1, column=1, padx=10, pady=5)

    tk.Button(win, text="Issue Book", command=issue_book).grid(row=2, column=0, padx=10, pady=10)
    tk.Button(win, text="Return Book", command=return_book).grid(row=2, column=1, padx=10, pady=10)

    listbox = ttk.Treeview(
        win,
        columns=("ID", "Member ID", "Book ID", "Issued", "Due Date", "Returned", "Fine"),
        show="headings"
    )
    for col in listbox["columns"]:
        listbox.heading(col, text=col)
    listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    show_transactions()
