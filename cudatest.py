import torch

# Check if PyTorch is available
print("PyTorch version:", torch.__version__)

# Check if CUDA (GPU) is available
if torch.cuda.is_available():
    device = torch.device("cuda")
    print("CUDA (GPU) is available.")
    print("Current GPU:", torch.cuda.get_device_name(0))  # 0 is the GPU index
else:
    device = torch.device("cpu")
    print("CUDA (GPU) is not available. Using CPU.")

# Perform a simple operation to verify CUDA usage (if available)
x = torch.tensor([1.0, 2.0, 3.0], device=device)
y = torch.tensor([4.0, 5.0, 6.0], device=device)
z = x + y
print("Result of addition:", y)

import threading
import cv2
from ultralytics import YOLO
  
