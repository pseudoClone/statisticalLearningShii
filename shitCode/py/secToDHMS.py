ipSeconds = int(input("Enter the seconds: "))

days =  ipSeconds // 86400
ipSeconds -= days * 86400

hours = ipSeconds // 3600
ipSeconds -= hours * 3600

mins = ipSeconds // 60
ipSeconds -= mins*60

print(f"Days: {days}, Hours: {hours}, Mins: {mins}, Seconds: {ipSeconds}")
