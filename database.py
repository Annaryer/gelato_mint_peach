import sqlite3

def get_connection():
    conn = sqlite3.connect("icecream.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS icecream (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            price INTEGER NOT NULL
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM icecream")
    count = cursor.fetchone()[0]

    if count == 0:
        icecreams = [
            ("Vanilla Dream", "Gelato", 1200),
            ("Strawberry Bliss", "Gelato", 1400),
            ("Mango Sunshine", "Sorbet", 1300),
            ("Pistachio Cream", "Gelato", 1600),
            ("Chocolate Heaven", "Gelato", 1500),
            ("Peach Breeze", "Sorbet", 1300)
        ]

        cursor.executemany(
            "INSERT INTO icecream (name, type, price) VALUES (?, ?, ?)",
            icecreams
        )
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            items TEXT NOT NULL,
            total_price INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()