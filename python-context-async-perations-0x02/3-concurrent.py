import asyncio
import aiosqlite


# Fetch all users
async def async_fetch_users():
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print("[ALL USERS]:", results)
            return results


# Fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            results = await cursor.fetchall()
            print("[USERS > 40]:", results)
            return results


# Run concurrently using asyncio.gather
async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )


# Run the async event loop
asyncio.run(fetch_concurrently())
