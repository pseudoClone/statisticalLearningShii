numbers = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

for i, sublist in enumerate(numbers):
    for j, num in enumerate(sublist):
        print(f"Main List index {i}: Sublist index {j}: {num}")
