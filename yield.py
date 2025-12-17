def countShit(number: int):
    for i in range(number):
        yield i

counter = countShit(4)
for i in counter:
    print(i)
