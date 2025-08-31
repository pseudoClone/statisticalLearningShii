class CumulativeAverage:
    def __init__(self) -> None:
        self.data = []
    def __call__(self, streamValue : int):
        self.data.append(streamValue)
        return sum(self.data)/len(self.data)

streamAvg = CumulativeAverage()
print(streamAvg(10))
print(streamAvg(15))
print(streamAvg(20))
print(streamAvg(30))

