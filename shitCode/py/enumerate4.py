batches = [
    (["x1", "x2", "x3"], ["y1", "y2", "y3"]),
    (["x4", "x5", "x6"], ["y4", "y5", "y6"]),
    (["x7", "x8", "x9"], ["y7", "y8", "y9"])
]

for batchIndex, (X, y) in enumerate(batches):
    print(f"Batch {batchIndex}:\n    X:{X}\n    y:{y}")
