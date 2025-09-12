import asyncio
import aiosqlite


async def async_fetch_users(db_name="example.db"):
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            print("All users:")
            for row in rows:
                print(row)
            return rows


async def async_fetch_older_users(db_name="example.db"):
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            print("\nUsers older than 40:")
            for row in rows:
                print(row)
            return rows


async def fetch_concurrently():
    # Run both queries concurrently
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results


if __name__ == "__main__":
    # Setup example database with some test data
    import sqlite3

    conn = sqlite3.connect("example.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    cur.execute("DELETE FROM users")  # Clear old data
    cur.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [
        ("Alice", 25),
        ("Bob", 35),
        ("Charlie", 45),
        ("Diana", 55),
    ])
    conn.commit()
    conn.close()

    # Run concurrent queries
    asyncio.run(fetch_concurrently())
