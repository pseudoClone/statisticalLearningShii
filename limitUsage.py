def limit_to_3_uses(func):
    counter = 0

    def wrapper(*args, **kwargs):
        nonlocal counter
        if counter < 3:
            counter += 1
            output = func(*args, **kwargs)
            return output
        else:
            print(f"Max usage of function reached\n")
    return wrapper

@limit_to_3_uses
def do_something(first, second):
    return first * second

print(do_something(3,2))
print(do_something(3,2))
print(do_something(3,2))
print(do_something(3,2))
