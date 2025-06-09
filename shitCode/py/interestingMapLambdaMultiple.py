def main():
    p = ('RSV4', 'S1000R', 'T190')
    q = ('F117 NH', 'F15C E', 'F22 R')
    
    print(f"{tuple(map(lambda x,y: x+" "+y, p, q))}")


if __name__ == "__main__":
    main()
