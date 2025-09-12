import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params is not None else ()
        self.connection = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


if __name__ == "__main__":
    # Setup example database
    conn = sqlite3.connect("example.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    cur.execute("DELETE FROM users")  # Clear old data
    cur.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 30))
    cur.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Bob", 20))
    cur.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Charlie", 40))
    conn.commit()
    conn.close()

    # Use the ExecuteQuery context manager
    query = "SELECT * FROM users WHERE age > ?"
    with ExecuteQuery("example.db", query, (25,)) as results:
        for row in results:
            print(row)
