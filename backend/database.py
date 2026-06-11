import sqlite3
from datetime import datetime

DB_PATH = "nalco_emails.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gmail_id TEXT UNIQUE,
            sender TEXT,
            subject TEXT,
            body_preview TEXT,
            category TEXT,
            urgency TEXT,
            summary TEXT,
            processed_at TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized.")

def save_email(gmail_id, sender, subject, body, category, urgency, summary):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO emails (gmail_id, sender, subject, body_preview, category, urgency, summary, processed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (gmail_id, sender, subject, body[:500], category, urgency, summary, datetime.now().isoformat()))
        conn.commit()
        print(f"Saved: {subject}")
    except sqlite3.IntegrityError:
        print(f"Already exists, skipping: {subject}")
    conn.close()

def get_all_emails():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM emails ORDER BY processed_at DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == '__main__':
    init_db()
    