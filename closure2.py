from collections.abc import Callable

def storeArguments(func:Callable) -> Callable:
    argsList : list[str] = []
    
    def innerFunc(someStuff) -> None:
        argsList.append(someStuff)
        func(someStuff)

    return innerFunc

print_ = storeArguments(print)
print_("What up my dawg!!")
print_("Is tis real bro??")

print(print_.__closure__[0].cell_contents)
