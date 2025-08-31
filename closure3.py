from collections.abc import Callable

def store_arguments(func:Callable) -> Callable:
    # argsList : list[str] = []
    argsList = []

    
    def inner(*args, **kwargs) -> None:
        argsList.append((args, kwargs))
        func(*args, **kwargs)

    return inner

print_ = store_arguments(print)

print_("I love this game")
print_(42, 42, 88)
print_(10, 20, 30, 40, sep=":")


print(print_.__closure__[0].cell_contents)
