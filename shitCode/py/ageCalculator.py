import datetime

date1 = input("Enter first date seperated by -: ")
date2 = input("Enter second date seperated by -: ")

date1 = date1.split(sep="-")
date2 = date2.split(sep="-")

date1 = datetime.date(int(date1[0]), int(date1[1]), int(date1[2]))
date2 = datetime.date(int(date2[0]), int(date2[1]), int(date2[2]))

print(f"{abs((date1 - date2).days)}")

