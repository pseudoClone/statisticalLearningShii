num1 = int(input("Enter the total numbers: "))
num2 = int(input("Enter your second number:"))


def gcd(*args):
    args = list(args)
    args.sort()
    args = list(map(int, args))
    if(args[0] == 0):
        return args[1]
    return(gcd(args[0],args[1] % args[0]))

print(gcd(num1,num2))
