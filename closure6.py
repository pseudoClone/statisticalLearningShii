from typing import Callable

def store_arguments(func: Callable) -> Callable:
    argsList = []
    
    #@wraps(func)
    def wrapper(*args, **kwargs):
        argsList.append((args, kwargs))
        value = func(*args, **kwargs)
        return value
    return wrapper

@store_arguments
def my_special_function(name:str, repeat:int):
    """This is a function for keeping text to UPPERCASE and repeating it"""
    return name.upper() * repeat

# Skippning my_special_function = store_arguments(my_special_function)
print(my_special_function("James", 4))
print(my_special_function("Ram", 5))

print(my_special_function.__closure__[0].cell_contents)
# help(my_special_function)
