import asyncio

async def download_file(url:str):
    print(f"Starting download from {url}")
    await(asyncio.sleep(2)) # Simulating download
    print(f"Download finished from {url}")

async def main():
    task1 = asyncio.create_task(download_file("https://example.com/file1"))
    task2 = asyncio.create_task(download_file("https://example.com/file2"))

    # Waiting for tasks to be completed
    await(task1)
    await(task2)

asyncio.run(main())
