import sqlite3

def init_db():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()

    # Users table with role
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT NOT NULL CHECK(role IN ('admin', 'member'))
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER,
            book_id INTEGER,
            date_issued TEXT,
            due_date TEXT,
            date_returned TEXT,
            fine INTEGER DEFAULT 0
        )
    ''')

    # Insert default admin user (only if not already present)
    cur.execute("SELECT * FROM users WHERE username = ?", ("admin",))
    if not cur.fetchone():
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    ("admin", "admin123", "admin"))

    conn.commit()
    conn.close()
