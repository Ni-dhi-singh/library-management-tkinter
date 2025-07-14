import tkinter as tk
from books import manage_books
from members import manage_members
from transactions import issue_return_books


def open_dashboard(role):
    win = tk.Tk()
    win.title("Library Dashboard")
    win.geometry("400x300")

    # Apply dark mode colors
    bg_color = "#1e1e1e"
    fg_color = "#ffffff"
    btn_bg = "#2c2c2c"
    btn_fg = "#ffffff"

    win.configure(bg=bg_color)

    tk.Label(win, text="Library Management System", font=("Helvetica", 16, "bold"),
             bg=bg_color, fg=fg_color).pack(pady=20)

    # Reusable button creator
    def dark_button(text, cmd):
        return tk.Button(win, text=text, width=25, bg=btn_bg, fg=btn_fg, command=cmd, activebackground="#3c3c3c")

    dark_button("Manage Books", manage_books).pack(pady=10)
    dark_button("Manage Members", manage_members).pack(pady=10)
    dark_button("Issue/Return Books", issue_return_books).pack(pady=10)


