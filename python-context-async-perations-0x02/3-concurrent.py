# 3-concurrent.py
import asyncio
import aiosqlite
import sqlite3

async def asyncfetchusers(db_name: str = "example.db"):
    """Fetch all users asynchronously."""
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            print("All users:")
            for row in rows:
                print(row)
            return rows

async def asyncfetcholder_users(db_name: str = "example.db"):
    """Fetch users older than 40 asynchronously."""
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            rows = await cursor.fetchall()
            print("\nUsers older than 40:")
            for row in rows:
                print(row)
            return rows

async def fetch_concurrently():
    """Run both queries concurrently and return their results."""
    results = await asyncio.gather(
        asyncfetchusers(),
        asyncfetcholder_users()
    )
    return results

if __name__ == "__main__":
    # Quick local setup to ensure example.db exists with some test data.
    conn = sqlite3.connect("example.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    cur.execute("DELETE FROM users")  # clear previous test data
    cur.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [
        ("Alice", 25),
        ("Bob", 35),
        ("Charlie", 45),
        ("Diana", 55),
        ("Eve", 41),
    ])
    conn.commit()
    conn.close()

    # Run the concurrent queries
    asyncio.run(fetch_concurrently())
