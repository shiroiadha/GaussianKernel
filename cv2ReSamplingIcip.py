import cv2
import matplotlib.pyplot as plt

# Load gambar (gantilah path jika perlu)
image = cv2.imread("hatter.png")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert ke RGB biar cocok untuk matplotlib

# Ukuran baru
new_size = (image.shape[1]*2, image.shape[0]*2)  # 2x lebih besar (upscale)

# Resize dengan berbagai interpolasi
methods = {
    "Nearest (INTER_NEAREST)": cv2.INTER_NEAREST,
    "Linear (INTER_LINEAR)": cv2.INTER_LINEAR,
    "Area (INTER_AREA)": cv2.INTER_AREA,
    "Cubic (INTER_CUBIC)": cv2.INTER_CUBIC,
    "Lanczos4 (INTER_LANCZOS4)": cv2.INTER_LANCZOS4,
}

resized_images = {
    name: cv2.resize(image, new_size, interpolation=method)
    for name, method in methods.items()
}

# Tampilkan hasil
plt.figure(figsize=(15, 10))
for i, (name, img) in enumerate(resized_images.items()):
    plt.subplot(2, 3, i+1)
    plt.imshow(img)
    plt.title(name)
    plt.axis("off")
plt.suptitle("Perbandingan Interpolasi di cv2.resize()", fontsize=16)
plt.tight_layout()
plt.show()