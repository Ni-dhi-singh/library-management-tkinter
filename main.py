import tkinter as tk
from init_db import init_db

init_db()

from login import login_screen

def main():
    root = tk.Tk()
    root.withdraw()
    login_screen()
    root.mainloop()

main()
