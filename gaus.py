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
        self.actionGaussianF.triggered.connect(self.gk) # Manggil fungsi konvolusi citra saat opsi tombol ditekan

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
        try:
            self.Image = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)
        except:
            pass

        sgm = 1                     # Sigma
        kz = math.ceil(6 * sgm)     # Kernel Size
        ax = np.linspace(-(kz - 1) / 2., (kz - 1) / 2., kz)
        xx, yy = np.meshgrid(ax, ax)
        kernel = np.exp(-(xx ** 2 + yy ** 2) / (2. * sgm ** 2))
        kernel = kernel / np.sum(kernel)

        blurred = cv2.filter2D(self.Image, -1, kernel)
        self.Image = blurred
        self.displayImage(1)

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

        # Opsi tampil gambar (1 buat input, 2 buat output proses)
        if windows == 1:
            self.label_loadimg.setPixmap(QPixmap.fromImage(img))
            self.label_loadimg.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.label_loadimg.setScaledContents(True)
        if windows == 2:
            self.label_outimg.setPixmap(QPixmap.fromImage(img))
            self.label_outimg.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.label_outimg.setScaledContents(True)

app = QtWidgets.QApplication(sys.argv)
window = ShowImage()
window.setWindowTitle('Gaussian Kernel')
window.show()
sys.exit(app.exec())