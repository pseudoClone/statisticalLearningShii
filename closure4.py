from collections.abc import Callable

def store_arguments(func : Callable) -> Callable:
    argsList = []
    
    def inner(*args, **kwargs):
        argsList.append((args, kwargs))

        value = func(*args, **kwargs)
        return value

    return inner

def my_special_function(name:str, repeat: int):
    return name.upper() * repeat


my_special_function = store_arguments(my_special_function) # Send function for decoration

print(my_special_function("James", 2))
print(my_special_function("Carl", 3))

print(my_special_function.__closure__[0].cell_contents)
