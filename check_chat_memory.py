# -*- coding: utf-8 -*-
"""
Check Chat Memory Table
-----------------------
This script inspects the contents of chat_memory.db (user_memory table).
"""

import sqlite3
import os
from datetime import datetime

# Path to database (adjust if your structure differs)
DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "chat_memory.db")
)

def check_database():
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at: {DB_PATH}")
        return

    print(f"✅ Connected to: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='user_memory';
    """)
    table_exists = cursor.fetchone()

    if not table_exists:
        print("⚠️ Table 'user_memory' does NOT exist.")
        conn.close()
        return

    print("\n================================================================================")
    print("📘 Table: user_memory")
    print("================================================================================")

    # Get column names
    cursor.execute("PRAGMA table_info(user_memory);")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"🧩 Columns: {columns}")

    # Fetch rows
    cursor.execute("SELECT * FROM user_memory ORDER BY updated_at DESC;")
    rows = cursor.fetchall()

    if not rows:
        print("ℹ️ No data found in user_memory.")
    else:
        for i, row in enumerate(rows, 1):
            print(f"\n--- Row {i} ---")
            for col, val in zip(columns, row):
                print(f"{col}: {val if val else 'NULL'}")

    conn.close()

if __name__ == "__main__":
    check_database()
