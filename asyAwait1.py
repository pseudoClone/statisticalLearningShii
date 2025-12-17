from typing import Awaitable
import asyncio
import time

async def say_after(delay: int, what: str) -> Awaitable:
    await asyncio.sleep(delay)
    print(what)

async def main():
    task1 = asyncio.create_task(say_after(2, "Hello"))
    task2 = asyncio.create_task(say_after(1, "World"))

    print(f"Started at: {time.strftime('%X')}")
    await task1
    await task2

    print(f"Ended at: {time.strftime('%X')}")

if __name__ == "__main__":
    asyncio.run(main())
