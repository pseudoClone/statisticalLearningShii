# Making a variable that can take many types

from typing import Optional

def process_item(item: int | str):
    print(item)

process_item(1)

def say_hi(name: Optional[str] = None):
    if name is not None:
        print(name)
    else:
        print("Hello World! MF")

say_hi()

