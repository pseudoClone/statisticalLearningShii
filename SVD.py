import numpy as np

def SVD_Compute(A):
    originalMat = np.copy(A)
    originalMatTranspose = originalMat.T
    originalMulTranspose = np.matmul(originalMat, originalMatTranspose)
    TransposeMuloriginal = np.matmul(originalMatTranspose, originalMat)
    ATAEigVal, ATAEigVec = np.linalg.eig(TransposeMuloriginal)
    _, AATEigVec = np.linalg.eig(originalMulTranspose)

    SingularValue = np.sqrt(ATAEigVal)

    U =  np.copy(AATEigVec)
    V = np.copy(ATAEigVec)

    Sigma = np.zeros_like(originalMat, dtype=float)
    np.fill_diagonal(Sigma,SingularValue)

    newMatrix = np.matmul(U, np.matmul(Sigma, V.T))
    print("Original Matrix A:\n", originalMat)
    print("\nU (Left Singular Vectors):\n", U)
    print("\nSigma (Singular Values):\n", Sigma)
    print("\nV^T (Right Singular Vectors):\n", V.T)
    print("\nReconstructed A (U * Sigma * V^T):\n", newMatrix)

def main():
    A = np.array([[1, 2, 3], [2, 4, 6]])
    SVD_Compute(A)

if __name__== "__main__":
    main()
