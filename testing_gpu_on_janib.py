import torch
import time

# Check CUDA availability
print("CUDA available:", torch.cuda.is_available())

# Select device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# Create large matrices
A = torch.randn(5000, 5000, device=device)
B = torch.randn(5000, 5000, device=device)

# Warm-up (important for GPU timing)
_ = torch.matmul(A, B)
torch.cuda.synchronize()

# Time matrix multiplication
start = time.time()
C = torch.matmul(A, B)
torch.cuda.synchronize()
end = time.time()

print("Result matrix device:", C.device)
print("Time taken:", end - start, "seconds")
