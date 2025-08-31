from collections.abc import Callable

def wrapper() -> Callable:
    
    argsList : list[str] = []

    def printShit(someStuff: str):
        print(someStuff)
        argsList.append(someStuff)

    return printShit

printingFunction = wrapper()
printingFunction("What up my dawg!!!")
