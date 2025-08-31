train_batches = [
    (["x1", "x2", "x3"], ["y1", "y2", "y3"]),
    (["x4", "x5", "x6"], ["y4", "y5", "y6"]),
    (["x7", "x8", "x9"], ["y7", "y8", "y9"]),
]
''' expected output

Batch 0:
    Inputs: ['x1', 'x2', 'x3']
    Labels: ['y1', 'y2', 'y3']
Batch 1:
    Inputs: ['x4', 'x5', 'x6']
    Labels: ['y4', 'y5', 'y6']
Batch 2:
    Inputs: ['x7', 'x8', 'x9']
    Labels: ['y7', 'y8', 'y9']

'''
for batchIndex, (first, second) in enumerate(train_batches):
    print(f"Batch{batchIndex}")
    print(f"    Inputs: {first}")
    print(f"    Labels: {second}")
