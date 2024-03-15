import imutils
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qimage2ndarray
from PIL import Image, ImageEnhance
import cv2
import numpy as np


def zoomIn(self):
    self.editToolBarH.clear()
    self.view.activate = False
    self.view.crop_rect = None
    self.scale = 1.1
    self.actionZoom()


def zoomOut(self):
    self.editToolBarH.clear()
    self.view.activate = False
    self.view.crop_rect = None
    self.scale = 0.9
    self.actionZoom()


def actionZoom(self):
    if self.image is not None:
        self.view.scale(self.scale, self.scale)


def crop(self):
    # self = crop(self)
    if self.buttonCrop.isChecked and self.image is not None:
        self.editToolBarH.clear()
        self.view.activate = True
        buttonCrop = QToolButton()
        buttonCrop.setText('OK')
        buttonCrop.setAutoRaise(True)
        buttonCrop.setIcon(QIcon('../icons/check.png'))
        buttonCrop.clicked.connect(self.cropClicked)
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.editToolBarH.addWidget(left_spacer)
        self.editToolBarH.addWidget(buttonCrop)
        self.editToolBarH.addWidget(right_spacer)


def cropClicked(self):
    crop_start, crop_end = self.view.getResult()
    if crop_start is not None and crop_end is not None:
        x, y, x1, y1 = self.view.mapToScene(crop_start).x(), self.view.mapToScene(crop_start).y(), self.view.mapToScene(
            crop_end).x(), self.view.mapToScene(crop_end).y()
        x = 0 if x < 0 else x
        y = 0 if y < 0 else y
        x1 = self.pixmap.width() if x1 > self.pixmap.width() else x1
        y1 = self.pixmap.height() if y1 > self.pixmap.height() else y1
        crop_rect = QRectF(x, y, x1 - x, y1 - y)
        self.pixmap = self.pixmap.copy(crop_rect.toRect())
        self.view.crop_rect = None
        self.view.crop_start = None
        self.view.crop_end = None
        self.scene.clear()  # Clear the scene
        self.scene.setSceneRect(0, 0, self.pixmap.width(), self.pixmap.height())
        self.scene.addPixmap(self.pixmap)
        self.scene.update()


def resize(self):
    if self.image is not None:
        self.editToolBarH.clear()
        self.view.activate = False
        self.view.crop_rect = None
        window = QWidget()
        width = QLabel()
        width.setText('Width:')
        height = QLabel()
        height.setText('Height:')
        self.spinBoxW = QSpinBox()
        self.spinBoxW.setMinimum(100)
        self.spinBoxW.setMaximum(2100)
        self.spinBoxW.setSingleStep(1)
        self.spinBoxW.setValue(100)

        self.spinBoxH = QSpinBox()
        self.spinBoxH.setMinimum(100)
        self.spinBoxH.setMaximum(2100)
        self.spinBoxH.setSingleStep(1)
        self.spinBoxH.setValue(100)
        button_action = QAction(self)
        button_action.setIcon(QIcon('../icons/check.png'))
        button_action.triggered.connect(self.buttonClickToResize)
        toolBarH = QHBoxLayout()
        toolBarH.addWidget(width)
        toolBarH.addWidget(self.spinBoxW)
        toolBarH.addWidget(height)
        toolBarH.addWidget(self.spinBoxH)
        window.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        window.setLayout(toolBarH)
        self.editToolBarH.addWidget(window)
        self.editToolBarH.addAction(button_action)


def buttonClickToResize(self):
    if self.spinBoxW.value() is not None and self.spinBoxH.value() is not None:
        width = self.spinBoxW.value()
        height = self.spinBoxH.value()
        self.pixmap = self.pixmap.scaled(QSize(width, height), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.scene.clear()  # Clear the scene
        self.scene.setSceneRect(0, 0, self.pixmap.width(), self.pixmap.height())
        self.scene.addPixmap(self.pixmap)
        self.scene.update()


def flipH(self):
    scale = (-1, 1)
    flip(self, scale)


def flipV(self):
    scale = (1, -1)
    flip(self, scale)


def flip(self, scale: tuple):
    if self.image is not None:
        self.editToolBarH.clear()
        self.view.activate = False
        self.view.crop_rect = None
        self.pixmap = self.pixmap.transformed(QTransform().scale(scale[0], scale[1]))
        self.pixmap = self.pixmap.copy()
        self.scene.setSceneRect(0, 0, self.pixmap.width(), self.pixmap.height())
        self.scene.clear()
        self.scene.addPixmap(self.pixmap)
        self.scene.update()


def rotate(self):
    if self.image is not None:
        self.original_pixmap = self.pixmap.copy()
        self.pixmap_ = self.pixmap.copy()
        self.editToolBarH.clear()
        self.view.activate = False
        self.view.crop_rect = None
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(-180)
        self.slider.setMaximum(180)
        self.slider.setFixedWidth(self.view.width() // 2.5)
        self.editToolBarH.clear()
        buttonRotateL = QToolButton()
        buttonRotateL.clicked.connect(self.rotateImage90R)
        buttonRotateL.setIcon(QIcon('../icons/rotateLeft.png'))
        buttonRotateR = QToolButton()
        buttonRotateR.clicked.connect(self.rotateImage90L)
        buttonRotateR.setIcon(QIcon('../icons/rotateRight.png'))
        self.slider.valueChanged.connect(self.rotateImage)
        buttonUndoRotation = QToolButton()
        buttonUndoRotation.clicked.connect(self.undoRotation)
        buttonUndoRotation.setIcon(QIcon('../icons/undo.png'))
        window = QWidget()
        toolBarH = QHBoxLayout()
        toolBarH.setSizeConstraint(QLayout.SetFixedSize)
        toolBarH.addWidget(buttonRotateL)
        toolBarH.addWidget(buttonRotateR)
        toolBarH.addWidget(self.slider)
        toolBarH.addWidget(buttonUndoRotation)
        window.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        window.setLayout(toolBarH)
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.editToolBarH.addWidget(left_spacer)
        self.editToolBarH.addWidget(window)
        self.editToolBarH.addWidget(right_spacer)


def rotateImage(self, angle):
    image = converPixmapToCV(self.pixmap_)
    rotated_image = imutils.rotate_bound(image, angle)
    pixmap = QPixmap.fromImage(
        QImage(rotated_image, rotated_image.shape[1], rotated_image.shape[0], rotated_image.strides[0],
               QImage.Format_RGB888).rgbSwapped())
    self.pixmap = pixmap
    self.scene.clear()
    self.scene.setSceneRect(0, 0, self.pixmap.width(), self.pixmap.height())
    self.scene.addPixmap(self.pixmap)
    self.scene.update()


def rotateImage90R(self):
    image = converPixmapToCV(self.pixmap)
    rotated_image = imutils.rotate_bound(image, -90)
    pixmap = QPixmap.fromImage(
        QImage(rotated_image, rotated_image.shape[1], rotated_image.shape[0], rotated_image.strides[0],
               QImage.Format_RGB888).rgbSwapped())
    self.pixmap = pixmap
    self.scene.clear()
    self.scene.setSceneRect(0, 0, self.pixmap.width(), self.pixmap.height())
    self.scene.addPixmap(self.pixmap)
    self.scene.update()


def rotateImage90L(self):
    image = converPixmapToCV(self.pixmap)
    rotated_image = imutils.rotate_bound(image, 90)
    pixmap = QPixmap.fromImage(
        QImage(rotated_image, rotated_image.shape[1], rotated_image.shape[0], rotated_image.strides[0],
               QImage.Format_RGB888).rgbSwapped())
    self.pixmap = pixmap
    self.scene.clear()
    self.scene.setSceneRect(0, 0, self.pixmap.width(), self.pixmap.height())
    self.scene.addPixmap(self.pixmap)
    self.scene.update()


def undoRotation(self):
    if hasattr(self, 'original_pixmap'):
        self.slider.setValue(0)
        pixmap = self.original_pixmap  # 恢复原始状态
        self.scene.clear()
        self.scene.setSceneRect(0, 0, pixmap.width(), pixmap.height())
        self.scene.addPixmap(pixmap)
        self.scene.update()


def onBrightnessChanged(self, value, pixmap):
    if self.image is not None:
        self.temperature = ()
        self.contrast = ()
        self.saturation = ()
        self.sharpness = ()
        self.highlights = ()
        self.shadows = ()
        self.labelBrightness.setText('Brightness: {}'.format(value))
        image = converPixmapToCV(pixmap)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        apha = 1 + value / 100
        if len(self.brightness) > 0:
            pass
        else:
            self.brightness += (image,)
        enhancer = ImageEnhance.Brightness(self.brightness[0])
        im_output = enhancer.enhance(apha)
        pixmap_new = convertPILtoPixmap(im_output)
        updateView(self, pixmap_new)


def onShadowsChanged(self, value, pixmap):
    if self.image is not None:
        self.temperature = ()
        self.contrast = ()
        self.saturation = ()
        self.sharpness = ()
        self.highlights = ()
        self.brightness = ()
        self.labelShadows.setText('Shadows: {}'.format(value))
        image = converPixmapToCV(pixmap)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        apha = 1 - value / 100
        if len(self.shadows) > 0:
            pass
        else:
            self.shadows += (image,)
        im_output = self.shadows[0].point(lambda x: x * apha)
        pixmap_new = convertPILtoPixmap(im_output)
        updateView(self, pixmap_new)


def onHightlightsChanged(self, value, pixmap):
    if self.image is not None:
        self.temperature = ()
        self.contrast = ()
        self.saturation = ()
        self.sharpness = ()
        self.shadows = ()
        self.brightness = ()
        self.labelHightlights.setText('Hightlights: {}'.format(value))
        image = converPixmapToCV(pixmap)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        apha = 1 + value / 100
        if len(self.highlights) > 0:
            pass
        else:
            self.highlights += (image,)
        im_output = self.highlights[0].point(lambda x: x * apha)
        # im_output = enhancer.enhance(apha)
        pixmap_new = convertPILtoPixmap(im_output)
        updateView(self, pixmap_new)


def onSharpnessChanged(self, value, pixmap):
    if self.image is not None:
        self.temperature = ()
        self.contrast = ()
        self.saturation = ()
        self.highlights = ()
        self.shadows = ()
        self.brightness = ()
        self.labelSharpness.setText('Sharpness: {}'.format(value))
        image = converPixmapToCV(pixmap)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        apha = 1 + value / 100
        if len(self.sharpness) > 0:
            pass
        else:
            self.sharpness += (image,)
        enhancer = ImageEnhance.Sharpness(self.sharpness[0])
        im_output = enhancer.enhance(apha)
        pixmap_new = convertPILtoPixmap(im_output)
        updateView(self, pixmap_new)


def onSaturationChanged(self, value, pixmap):
    if self.image is not None:
        self.temperature = ()
        self.contrast = ()
        self.sharpness = ()
        self.highlights = ()
        self.shadows = ()
        self.brightness = ()
        self.labelSaturation.setText('Saturation: {}'.format(value))
        image = converPixmapToCV(pixmap)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        apha = 1 + value / 100
        if len(self.saturation) > 0:
            pass
        else:
            self.saturation += (image,)
        enhancer = ImageEnhance.Color(self.saturation[0])
        im_output = enhancer.enhance(apha)
        pixmap_new = convertPILtoPixmap(im_output)
        updateView(self, pixmap_new)


def onContrastChanged(self, value, pixmap):
    if self.image is not None:
        self.temperature = ()
        self.saturation = ()
        self.sharpness = ()
        self.highlights = ()
        self.shadows = ()
        self.brightness = ()
        self.labelContrast.setText('Contrast: {}'.format(value))
        image = converPixmapToCV(pixmap)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        apha = 1 + value / 100
        if len(self.contrast) > 0:
            pass
        else:
            self.contrast += (image,)
        enhancer = ImageEnhance.Contrast(self.contrast[0])
        im_output = enhancer.enhance(apha)
        pixmap_new = convertPILtoPixmap(im_output)
        updateView(self, pixmap_new)


def updateView(self, pixmap):
    self.scene.clear()
    self.scene.addPixmap(pixmap)
    self.pixmap = pixmap


def convertCVtoPixmap(rotated_image):
    return QPixmap.fromImage(QImage(rotated_image, rotated_image.shape[1], rotated_image.shape[0],
                                    rotated_image.shape[1] * rotated_image.shape[2], QImage.Format_BGR888).rgbSwapped())


def convertPILtoPixmap(rotated_image):
    np_image = np.array(rotated_image)
    qimage = qimage2ndarray.array2qimage(np_image)
    pixmap = QPixmap.fromImage(qimage)
    return pixmap


def converPixmapToCV(pixmap):
    image_data = qimage2ndarray.rgb_view(pixmap.toImage())
    image_data = cv2.cvtColor(image_data, cv2.COLOR_RGB2BGR)
    return image_data
