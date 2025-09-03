def count_up_to(n):
    count = 1
    while count <= n:
        yield count
        count += 1

counter = count_up_to(5) # count_up_to is generator function and counter is generator

print(next(counter))
print(next(counter))
print(next(counter))
print(next(counter))
print(next(counter))
