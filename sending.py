def echo():
    value = None
    while True:
        value = (yield value)
        print(f"Received: {value}")

gen = echo()
next(gen)
while True:
    print(gen.send("Hello"))
    print(gen.send("World!"))
