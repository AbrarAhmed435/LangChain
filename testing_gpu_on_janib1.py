import torch
import time

print("CUDA available:", torch.cuda.is_available())

if not torch.cuda.is_available():
    print("No CUDA device visible")
    exit(1)

device = torch.device("cuda")
print("Using device:", device)
print("GPU:", torch.cuda.get_device_name(0))

A = torch.randn(5000, 5000, device=device)
B = torch.randn(5000, 5000, device=device)

torch.cuda.synchronize()
start = time.time()
C = torch.matmul(A, B)
torch.cuda.synchronize()
end = time.time()

print("Result matrix device:", C.device)
print("Time taken:", end - start, "seconds")

