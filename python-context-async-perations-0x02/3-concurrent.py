#!/usr/bin/env python3
"""
3-concurrent.py

Run multiple database queries concurrently using asyncio.gather and aiosqlite.
"""

import asyncio
import aiosqlite
import sqlite3


async def asyncfetchusers(db_name: str = "example.db"):
    """Fetch all users asynchronously from the database."""
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            print("All users:")
            for row in rows:
                print(row)
            return rows


async def asyncfetcholder_users(db_name: str = "example.db"):
    """Fetch users older than 40 asynchronously from the database."""
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            rows = await cursor.fetchall()
            print("\nUsers older than 40:")
            for row in rows:
                print(row)
            return rows


async def fetch_concurrently():
    """Run both queries concurrently using asyncio.gather."""
    results = await asyncio.
