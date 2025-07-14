📚 Library Management System (Tkinter + SQLite)
A desktop-based Library Management System built using Python Tkinter, SQLite, and features like role-based login, dark/light mode, book/member management, email reminders, and data export to Excel/PDF.

🚀 Features
🔐 Role-based Login (Admin / Member)

🌗 Light/Dark Theme Toggle

👤 Manage Members (Add/Edit/Delete/Search)

📖 Manage Books (Add/Edit/Delete/Search)

🔁 Issue/Return Books with transaction history

⏰ Due Date & Fine Calculation

📧 Email Reminder for overdue books

📄 Export data to Excel and PDF

🔍 Search functionality for all records

💾 Data stored using SQLite database

🛠️ Tech Stack
Python 3.x

Tkinter (GUI)

SQLite (Database)

pandas (Excel export)

reportlab (PDF generation)

smtplib (Email sending)

📁 Folder Structure
pgsql
Copy
Edit
LIB/
├── books.py
├── borrow_return.py
├── dashboard.py
├── database.py
├── email_utils.py
├── init_db.py
├── library.db
├── login.py
├── main.py
├── members.py
├── theme_config.py
├── transactions.py
├── utils.py
└── .gitignore

