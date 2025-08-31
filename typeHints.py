from typing import TypeAlias


def surface_area_of_cube(edge_length: int) -> str:
    return f"The surface area of cube is {6 * edge_length ** 2}.\n"

print(surface_area_of_cube(10))

def name_shit(first_name : str, last_name: str) -> str:
    full_name = first_name.title() + " " + last_name.title()
    return full_name

print(name_shit("prince", "nepal"))

# Type Aliasing
DogShit:TypeAlias = list[int]

def scale(scalar: int, dogshit: DogShit) -> DogShit:
    return [scalar * num for num in dogshit]

doggy = scale(4, [1,3,5,9])
print(doggy)
