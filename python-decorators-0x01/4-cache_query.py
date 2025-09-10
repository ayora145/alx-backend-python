
import sqlite3
import functools

# Simple cache dictionary
query_cache = {}

# Reuse the with_db_connection decorator
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

# Cache decorator
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Use query string as the cache key
        query = kwargs.get("query")
        if query in query_cache:
            print(f"Using cached result for query: {query}")
            return query_cache[query]

        result = func(*args, **kwargs)
        query_cache[query] = result
        print(f"Cached result for query: {query}")
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# Example usage
if __name__ == "__main__":
    # First call executes query and caches result
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    # Second call uses cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)
