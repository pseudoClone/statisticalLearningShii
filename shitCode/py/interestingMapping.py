def someOperationg(num: str) -> str:
    return num * 2

def main():
    car = ['Mazda', 'BMW', 'Geely', 'Porsche', 'Nissan']
    sq = list(map(someOperationg, car))
    print(sq)

if __name__ == "__main__":
    main()
