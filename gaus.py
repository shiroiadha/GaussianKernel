import cv2
import numpy as np
import math
import sys
from pickletools import uint8
from numpy import uint8
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

class ShowImage(QMainWindow):

    def __init__(self):
        super(ShowImage, self).__init__()
        loadUi('GUI.ui', self)
        self.Image = None
        self.Image2 = None

        # Operation menu list
        self.button_loadimg.clicked.connect(self.func)  # Manggil fungsi load image saat opsi tombol ditekan
        self.button_grayscale.clicked.connect(self.gs)  # Manggil fungsi grayscaling saat opsi tombol ditekan
        self.actionGaussianF.triggered.connect(self.gk) # Manggil fungsi konvolusi citra (Gaussian) saat opsi tombol ditekan
        # self.actionSharpener.triggered.connect(self.sp) # Manggil fungsi konvolusi citra (Image Sharpenning / High Pass Kernel) saat opsi tombol ditekan
        # # Upscaling option
        self.action1_5.triggered.connect(self.up1_5)    # Upscaling 1.5 kali
        self.action2.triggered.connect(self.up2)        # Upscaling 2 kali
        self.action4.triggered.connect(self.up4)        # Upscaling 4 kali
        self.actionUnsharpM.triggered.connect(self.um)  # Upscaling 4 kali
        self.actionSave.triggered.connect(self.saveF)   # Simpan hasil perubahan

    def func(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Load Image",
            "",
            "Image Files (*.png *.jpg *.bmp *.jpeg);;All Files (*)"
        )
        if filename:
            self.Image = cv2.imread(filename)
            if self.Image is not None:
                self.displayImage(1)
            else:
                QMessageBox.warning(self, "Error", "Failed to Load Image.")

    def saveF(self):
        if self.Image is None:
            QMessageBox.warning(self, "Error", "Tidak ada gambar untuk disimpan.")
            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "",
            "JPEG Files (*.jpg);;PNG Files (*.png);;Bitmap Files (*.bmp);;All Files (*)"
        )

        if filename:
            success = cv2.imwrite(filename, self.Image)
            if success:
                QMessageBox.information(self, "Success", "Gambar berhasil disimpan.")
            else:
                QMessageBox.warning(self, "Error", "Gagal menyimpan gambar.")

    def gs(self):
        H, W = self.Image.shape[:2]
        gray = np.zeros((H, W), dtype=uint8)
        for i in range(H):
            for j in range(W):
                # np.clip(calculated_grayscale, min_pixel_num, max_pixel_num)
                gray[i, j] = np.clip(0.299 * self.Image[i, j, 0] +
                                     0.587 * self.Image[i, j, 1] +
                                     0.114 * self.Image[i, j, 2], 0, 255)
        self.Image = gray
        self.displayImage(2)

    def gk(self):
        # try:
        #     self.Image = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)
        # except:
        #     pass

        sgm = 1.5                     # Sigma
        kz = math.ceil(6 * sgm)     # Kernel Size
        ax = np.linspace(-(kz - 1) / 2., (kz - 1) / 2., kz)
        xx, yy = np.meshgrid(ax, ax)
        kernel = np.exp(-(xx ** 2 + yy ** 2) / (2. * sgm ** 2))
        kernel = kernel / np.sum(kernel)

        blurred = cv2.filter2D(self.Image, -1, kernel)
        self.Image = blurred
        self.displayImage(2)

    def up1_5(self):
        n = 1.5
        self.Image = cv2.resize(self.Image, (self.Image.shape[1]*n, self.Image.shape[0]*n), interpolation=cv2.INTER_LINEAR)
        self.displayImage(2)

    def up2(self):
        n = 2
        self.Image = cv2.resize(self.Image, (self.Image.shape[1]*n, self.Image.shape[0]*n), interpolation=cv2.INTER_LINEAR)
        self.displayImage(2)

    def up4(self):
        n = 4
        self.Image = cv2.resize(self.Image, (self.Image.shape[1]*n, self.Image.shape[0]*n), interpolation=cv2.INTER_LINEAR)
        self.displayImage(2)

    def um(self):
        # Gaussian Blur
        blurred = cv2.GaussianBlur(self.Image, (5, 5), 1.0)
        # Unsharp Masking
        amount = 1.5
        sharpened = cv2.addWeighted(self.Image, 1 + amount, blurred, -amount, 0)
        self.Image = sharpened
        self.displayImage(2)


    def displayImage(self, windows=1):
        qformat = QImage.Format_Indexed8

        if len(self.Image.shape) == 3:
            if self.Image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        img = QImage(self.Image, self.Image.shape[1], self.Image.shape[0],
                     self.Image.strides[0], qformat)

        img = img.rgbSwapped()

        # Opsi tampil gambar (1 buat label dikiri, 2 buat label dikanan)
        pixmap = QPixmap.fromImage(img)
        scaled_pixmap = pixmap.scaled(self.label_loadimg.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        if windows == 1:
            self.label_loadimg.setPixmap(scaled_pixmap)
            self.label_loadimg.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        if windows == 2:
            self.label_outimg.setPixmap(scaled_pixmap)
            self.label_outimg.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

app = QtWidgets.QApplication(sys.argv)
window = ShowImage()
window.setWindowTitle('Gaussian Kernel')
window.show()
sys.exit(app.exec())