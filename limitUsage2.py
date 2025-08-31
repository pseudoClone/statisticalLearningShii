from typing import Callable

def limit_uses(limit : int): # Not a decorator, since decorator takes function as argument
    def decorator(func : Callable) -> Callable:
        counter = 0

        def wrapper(*args, **kwargs):
            nonlocal counter

            if(counter < limit):
                counter = counter + 1
                output = func(*args, **kwargs)
                return output
            else:
                print(f"Max usage of function call reached")

        return wrapper
    return decorator # Since decorator is returned by limit_uses, limit_uses is a decorator factory 

@limit_uses(3)
def do_something(first, second):
    return first * second
