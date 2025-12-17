while True:
    try:
        x = int(input("Enter shit!: "))
        break
    except ValueError:
        print("Not a valid number. Try again...")
