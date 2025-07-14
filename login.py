import tkinter as tk
from tkinter import messagebox
import sqlite3
from dashboard import open_dashboard
from theme_config import current_theme
from utils import apply_theme

def login_screen():
    def login():
        username = username_entry.get()
        password = password_entry.get()

        conn = sqlite3.connect("library.db")
        cur = conn.cursor()
        cur.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
        result = cur.fetchone()
        conn.close()

        if result:
            role = result[0]
            messagebox.showinfo("Login Success", f"Welcome {username} ({role})!")
            win.destroy()
            open_dashboard(role)  # Pass the role to dashboard
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def register():
        username = username_entry.get()
        password = password_entry.get()
        role = role_var.get()

        if not username or not password or not role:
            messagebox.showwarning("Input Error", "Enter username, password, and select role.")
            return

        conn = sqlite3.connect("library.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        if cur.fetchone():
            messagebox.showerror("User Exists", "Username already taken.")
        else:
            cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                        (username, password, role))
            conn.commit()
            messagebox.showinfo("Registration Successful", f"Registered as {role}. You can now log in.")
        conn.close()

    def toggle_theme():
        new_theme = "dark" if current_theme == "light" else "light"
        with open("theme_config.py", "w") as f:
            f.write(f'current_theme = "{new_theme}"\n')
        messagebox.showinfo("Theme Changed", f"Switched to {new_theme} mode.\nPlease restart the app.")
        win.destroy()

    win = tk.Tk()
    win.title("Login")
    win.geometry("350x350")
    apply_theme(win, current_theme)

    tk.Label(win, text="Username").pack(pady=5)
    username_entry = tk.Entry(win)
    username_entry.pack(pady=5)

    tk.Label(win, text="Password").pack(pady=5)
    password_entry = tk.Entry(win, show="*")
    password_entry.pack(pady=5)

    tk.Label(win, text="Role (for registration only)").pack(pady=5)
    role_var = tk.StringVar()
    role_dropdown = tk.OptionMenu(win, role_var, "admin", "member")
    role_dropdown.pack(pady=5)

    tk.Button(win, text="Login", command=login).pack(pady=10)
    tk.Button(win, text="New User? Register", command=register).pack(pady=5)
    tk.Button(win, text="Toggle Theme", command=toggle_theme).pack(pady=10)

    win.mainloop()
