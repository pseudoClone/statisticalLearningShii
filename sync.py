import time

def countShit():
    print(1)
    time.sleep(1)
    print(2)
    time.sleep(1)

def main():
    for _ in range(3):
        countShit()

if __name__ == "__main__":
    start = time.perf_counter()
    main()
    elapsed_time = time.perf_counter() - start
    print(f"{__file__} executed in {elapsed_time:0.2f} seconds")
