import asyncio
import time
async def countShit():
    print(1)
    await asyncio.sleep(1)
    print(2)
    await asyncio.sleep(1)

async def main():
    await asyncio.gather(countShit(), countShit(), countShit())

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    elapsed_time = time.perf_counter() - start
    print(f"{__file__} executed in {elapsed_time:0.2f} seconds")

