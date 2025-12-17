from typing import Callable

class LimitUses:
    def __init__(self, limit) -> None:
        self.limit = limit
        self.counter = 0

    def __call__(self, func: Callable):
        def wrapper(*args, **kwargs):
            if self.counter < self.limit:
                self.counter += 1
                return func(*args, **kwargs)
            else:
                print("Max usage of function call reached")
        return wrapper

@LimitUses(3)
def do_something(first:int, second:int) -> int:
    return first * second

print(do_something(2,3))
print(do_something(2,3))
print(do_something(2,3))
print(do_something(2,3))
print(do_something(2,3))
