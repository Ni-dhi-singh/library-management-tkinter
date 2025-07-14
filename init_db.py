import sqlite3

def init_db():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()

    # Drop and recreate the users table with 'role' column if needed
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if cur.fetchone():
        # Check if role column exists
        cur.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cur.fetchall()]
        if 'role' not in columns:
            cur.execute("ALTER TABLE users RENAME TO users_backup")
            cur.execute('''
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT,
                    role TEXT
                )
            ''')
            cur.execute('''
                INSERT INTO users (username, password, role)
                SELECT username, password, 'member' FROM users_backup
            ''')
            cur.execute("DROP TABLE users_backup")
    else:
        # Create the table if it doesn't exist
        cur.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT
            )
        ''')

    # Other tables
    cur.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY,
            name TEXT,
            phone TEXT,
            email TEXT
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT,
            author TEXT
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            member_id INTEGER,
            book_id INTEGER,
            date_issued TEXT,
            date_returned TEXT,
            due_date TEXT,
            fine INTEGER
        )
    ''')

    # Insert default admin
    cur.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
                ("admin", "admin123", "admin"))

    conn.commit()
    conn.close()
