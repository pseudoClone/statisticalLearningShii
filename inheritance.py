class Animal:
        def __init__(self, name):
                self.name = name
        def speak(self):
                return "Animal Speaks"

class Dog(Animal):
        def __init__(self, name, breed):
                super().__init__(name) # Call parent constructor(which initializes the name)
                """
                What this allows us to do is call Dog("Max", "Chihiuwa") and 
                name in Animal class is initialized automatically
                """
                self.breed = breed
        def speak(self):
                return f"{self.name} says woof!!!"

animal = Animal("Generic Animal")
dog = Dog("Buddy", "Golden Retriever")

print(animal.speak())
print(dog.speak())