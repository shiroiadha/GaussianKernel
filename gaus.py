import cv2, math
import numpy as np
import matplotlib.pyplot as plt

# Fungsi untuk menerapkan Gaussian Blur dengan kernel custom
def apply_gaussian_blur(image_path, kernel_size=5, sigma=1.0):
    # Baca gambar
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print("Gagal memuat gambar. Periksa path-nya.")
        return

    # Buat Gaussian kernel secara manual
    def gaussian_kernel(size, sigma):
        ax = np.linspace(-(size - 1) / 2., (size - 1) / 2., size)
        xx, yy = np.meshgrid(ax, ax)
        kernel = np.exp(-(xx**2 + yy**2) / (2. * sigma**2))
        return kernel / np.sum(kernel)

    kernel = gaussian_kernel(kernel_size, sigma)

    # Terapkan filter Gaussian menggunakan kernel custom
    blurred = cv2.filter2D(image, -1, kernel)

    # Tampilkan hasil
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title("Original")
    plt.imshow(image, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.title("Gaussian Blurred")
    plt.imshow(blurred, cmap='gray')
    plt.axis('off')
    
    plt.show()

# Ganti dengan path ke file gambarmu
sigma = 1
kernel_size = math.ceil(6* sigma)
apply_gaussian_blur('blendNgeGabut.png', kernel_size, sigma)