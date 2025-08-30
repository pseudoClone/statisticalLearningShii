def my_decoration(func):
    def wrapper():
        print("Before the function runs")
        func()
        print("After the function runs")
    return wrapper

# @my_decorator syntax is a shorthand for say_hello = my_decorator(say_hello)

@my_decoration
def say_hello():
    print("Hello")
