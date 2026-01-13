"""
Minimal test - no imports from app
"""
import cv2
import numpy as np

print("Loading image...")
img_path = "../test-photos/boba.jpg"
img = cv2.imread(img_path)

if img is None:
    print(f"ERROR: Could not load {img_path}")
    exit(1)

print(f"✅ Loaded image: {img.shape}")

# Convert BGR to RGB
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

print("Applying cartoon filter...")

# Resize for faster processing
height, width = img.shape[:2]
if max(height, width) > 1200:
    scale = 1200 / max(height, width)
    img = cv2.resize(img, (int(width*scale), int(height*scale)))
    print(f"Resized to: {img.shape}")

# Bilateral filter (2 passes)
color = img.copy()
for i in range(2):
    print(f"  Pass {i+1}/2...")
    color = cv2.bilateralFilter(color, d=9, sigmaColor=75, sigmaSpace=75)

print("Posterizing...")
step = 256 // 6
color = (color // step) * step

print("Median blur...")
color = cv2.medianBlur(color, 5)

print("Edge detection...")
gray = cv2.cvtColor(color, cv2.COLOR_RGB2GRAY)
gray = cv2.medianBlur(gray, 5)
edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                              cv2.THRESH_BINARY, blockSize=9, C=2)

print("Combining...")
edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
cartoon = cv2.bitwise_and(color, edges_rgb)

print("Saving...")
output = cv2.cvtColor(cartoon, cv2.COLOR_RGB2BGR)
cv2.imwrite("output/minimal_cartoon.png", output)

print("✅ DONE! Saved to output/minimal_cartoon.png")

