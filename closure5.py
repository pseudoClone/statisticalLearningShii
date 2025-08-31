from collections.abc import Callable

def store_arguments(func: Callable) -> Callable:
    argsList = []

    def wrapper(*args, **kwargs):
        argsList.append((args, kwargs))
        value = func(*args, **kwargs)
        return value
    return wrapper

def my_special_function(name:str, repeat:int):
    return name.upper() * repeat

my_special_function = store_arguments(my_special_function)

