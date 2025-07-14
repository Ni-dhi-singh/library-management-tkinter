# utils.py
import tkinter as tk

def apply_theme(win, theme):
    if theme == "dark":
        bg = "#1e1e1e"
        fg = "#ffffff"
        entry_bg = "#2e2e2e"
        btn_bg = "#333333"
        active_bg = "#444444"
    else:
        bg = "#f0f0f0"
        fg = "#000000"
        entry_bg = "#ffffff"
        btn_bg = "#e0e0e0"
        active_bg = "#d0d0d0"

    win.configure(bg=bg)
    for widget in win.winfo_children():
        if isinstance(widget, (tk.Label, tk.Button)):
            widget.configure(bg=bg, fg=fg)
            if isinstance(widget, tk.Button):
                widget.configure(bg=btn_bg, activebackground=active_bg)
        elif isinstance(widget, tk.Entry):
            widget.configure(bg=entry_bg, fg=fg, insertbackground=fg)
