from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2
import numpy as np
import imutils
import qimage2ndarray


def openfile(self):
    self.editToolBarH.clear()
    self.scale = 1
    self.view.activate = False

    file_name, _ = QFileDialog.getOpenFileName(
        self, "Open file", ".", "Image Files (*.png *.jpg *.bmp *.jpeg)"
    )
    if not file_name:
        return
    else:
        self.scene.clear()
        self.image = QImage(file_name)
        self.pixmap = QPixmap.fromImage(self.image)
        self.scene.setSceneRect(0, 0, self.image.width(), self.image.height())
        self.scene.addPixmap(self.pixmap)
