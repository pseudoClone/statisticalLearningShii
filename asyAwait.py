import asyncio
import time
from typing import Awaitable

async def say_after(delay: int, what: str) -> Awaitable:
    await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"Started at: {time.strftime('%X')}")
    await say_after(1, "Hello")
    await say_after(1, "Hello")

    print(f"Ended at: {time.strftime('%X')}")

asyncio.run(main())
    
