import base64

import imutils
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qimage2ndarray
from PIL import Image, ImageEnhance
import cv2
import numpy as np

from App.ui.ui import ImageCropper


def initEditTool(ui: ImageCropper):
    index = ui.tabs.indexOf(ui.tabEdit)
    if index != -1:
        ui.tabs.tabBar().setTabVisible(index, False)
    else:
        assert False, 'Tab not found'
    ui.toolEditBtnSwitch = False
    updateView(ui, ui.oldPixmap)
    # ui.oldPixmap = ui.pixmap.copy()
    ui.initToolEditSwitch = True
    for slider in ui.sliderList:
        if slider.value() != 0:
            slider.setValue(0)
    ui.initToolEditSwitch = False
    ui.editToolBarH.clear()
    ui.view.activate = False
    ui.view.crop_rect = None


def edit(ui: ImageCropper):
    if ui.image is not None:
        initEditTool(ui)
        index = ui.tabs.indexOf(ui.tabEdit)
        if index != -1:
            ui.tabs.tabBar().setTabVisible(index, True)
            ui.tabs.setCurrentIndex(index)


def showEditTools(ui: ImageCropper):
    # Buttons
    toolEditLabel = QLabel("Save changes?")
    toolEditConfirmBtn = QToolButton()
    toolEditConfirmBtn.clicked.connect(ui.confirmEdit)
    toolEditConfirmBtn.setIcon(QIcon('../icons/check.png'))

    toolEditCancelBtn = QToolButton()
    toolEditCancelBtn.clicked.connect(ui.undoEdit)
    toolEditCancelBtn.setIcon(QIcon('../icons/undo.png'))
    left_spacer = QWidget()
    left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    right_spacer = QWidget()
    right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    widget = QWidget()
    layout = QHBoxLayout()
    layout.addWidget(toolEditLabel)
    layout.addWidget(toolEditConfirmBtn)
    layout.addWidget(toolEditCancelBtn)
    layout.setSpacing(20)
    widget.setLayout(layout)
    ui.editToolBarH.addWidget(left_spacer)
    ui.editToolBarH.addWidget(widget)
    ui.editToolBarH.addWidget(right_spacer)


def undoEdit(ui: ImageCropper):
    ui.scene.clear()
    ui.pixmap = ui.oldPixmap.copy()
    ui.scene.addPixmap(ui.pixmap)
    ui.scene.update()


def confirmEdit(ui: ImageCropper):
    ui.oldPixmap = ui.pixmap.copy()


def zoomIn(ui):
    if ui.image is not None:
        initEditTool(ui)
        ui.scale = 1.1
        ui.actionZoom()


def zoomOut(ui):
    if ui.image is not None:
        initEditTool(ui)
        ui.scale = 0.9
        ui.actionZoom()


def actionZoom(ui):
    if ui.image is not None:
        ui.view.scale(ui.scale, ui.scale)


def crop(ui):
    # self = crop(self)
    if ui.buttonCrop.isChecked and ui.image is not None:
        initEditTool(ui)

        ui.view.activate = True
        labelCrop = QLabel()
        labelCrop.setText('Crop the image?  ')
        buttonCrop = QToolButton()
        buttonCrop.setText('OK')
        buttonCrop.setAutoRaise(True)
        buttonCrop.setIcon(QIcon('../icons/check.png'))
        buttonCrop.clicked.connect(ui.cropClicked)
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        ui.editToolBarH.addWidget(left_spacer)
        ui.editToolBarH.addWidget(labelCrop)
        ui.editToolBarH.addWidget(buttonCrop)
        ui.editToolBarH.addWidget(right_spacer)


def cropClicked(ui):
    crop_start, crop_end = ui.view.getResult()
    if crop_start is not None and crop_end is not None:
        x, y, x1, y1 = ui.view.mapToScene(crop_start).x(), ui.view.mapToScene(crop_start).y(), ui.view.mapToScene(
            crop_end).x(), ui.view.mapToScene(crop_end).y()
        x = 0 if x < 0 else x
        y = 0 if y < 0 else y
        x1 = ui.pixmap.width() if x1 > ui.pixmap.width() else x1
        y1 = ui.pixmap.height() if y1 > ui.pixmap.height() else y1
        crop_rect = QRectF(x, y, x1 - x, y1 - y)
        ui.pixmap = ui.pixmap.copy(crop_rect.toRect())
        ui.view.crop_rect = None
        ui.view.crop_start = None
        ui.view.crop_end = None
        ui.scene.clear()  # Clear the scene
        ui.scene.setSceneRect(0, 0, ui.pixmap.width(), ui.pixmap.height())
        ui.scene.addPixmap(ui.pixmap)
        ui.scene.update()
        ui.oldPixmap = ui.pixmap.copy()


def resize(ui):
    if ui.image is not None:
        initEditTool(ui)
        window = QWidget()
        width = QLabel()
        width.setText('Width:')
        height = QLabel()
        height.setText('Height:')
        ui.spinBoxW = QSpinBox()
        ui.spinBoxW.setMinimum(10)
        ui.spinBoxW.setMaximum(1000)
        ui.spinBoxW.setSingleStep(1)
        ui.spinBoxW.setValue(100)
        ui.spinBoxW.setSuffix("%")
        ui.spinBoxW.valueChanged.connect(lambda: previewResize(ui))

        ui.spinBoxH = QSpinBox()
        ui.spinBoxH.setMinimum(10)
        ui.spinBoxH.setMaximum(1000)
        ui.spinBoxH.setSingleStep(1)
        ui.spinBoxH.setValue(100)
        ui.spinBoxH.setSuffix("%")
        ui.spinBoxH.valueChanged.connect(lambda: previewResize(ui))

        button_action = QAction(ui)
        button_action.setIcon(QIcon('../icons/check.png'))
        button_action.triggered.connect(ui.buttonClickToResize)
        toolBarH = QHBoxLayout()
        toolBarH.addWidget(width)
        toolBarH.addWidget(ui.spinBoxW)
        toolBarH.addWidget(height)
        toolBarH.addWidget(ui.spinBoxH)
        window.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        window.setLayout(toolBarH)
        ui.editToolBarH.addWidget(window)
        ui.editToolBarH.addAction(button_action)


def buttonClickToResize(ui):
    ui.oldPixmap = ui.pixmap.copy()


def previewResize(ui):
    if ui.spinBoxW.value() is not None and ui.spinBoxH.value() is not None:
        widthPercent = ui.spinBoxW.value() / 100.0
        heightPercent = ui.spinBoxH.value() / 100.0
        width = int(ui.oldPixmap.width() * widthPercent)
        height = int(ui.oldPixmap.height() * heightPercent)
        ui.pixmap = ui.oldPixmap.scaled(QSize(width, height), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        ui.scene.clear()
        ui.scene.setSceneRect(0, 0, ui.pixmap.width(), ui.pixmap.height())
        ui.scene.addPixmap(ui.pixmap)
        ui.scene.update()


def flipH(ui):
    scale = (-1, 1)
    flip(ui, scale)


def flipV(ui):
    scale = (1, -1)
    flip(ui, scale)


def flip(ui, scale: tuple):
    if ui.image is not None:
        initEditTool(ui)
        ui.pixmap = ui.pixmap.transformed(QTransform().scale(scale[0], scale[1]))
        ui.pixmap = ui.pixmap.copy()
        ui.scene.setSceneRect(0, 0, ui.pixmap.width(), ui.pixmap.height())
        ui.scene.clear()
        ui.scene.addPixmap(ui.pixmap)
        ui.scene.update()
        ui.oldPixmap = ui.pixmap.copy()


def rotate(ui):
    if ui.image is not None:
        ui.original_pixmap = ui.pixmap.copy()
        ui.pixmap_ = ui.pixmap.copy()
        initEditTool(ui)

        ui.slider = QSlider(Qt.Horizontal, ui)
        ui.slider.setMinimum(-180)
        ui.slider.setMaximum(180)
        ui.slider.setFixedWidth(ui.view.width() // 2.5)
        ui.editToolBarH.clear()
        buttonRotateL = QToolButton()
        buttonRotateL.clicked.connect(ui.rotateImage90R)
        buttonRotateL.setIcon(QIcon('../icons/rotateLeft.png'))
        buttonRotateR = QToolButton()
        buttonRotateR.clicked.connect(ui.rotateImage90L)
        buttonRotateR.setIcon(QIcon('../icons/rotateRight.png'))
        ui.slider.valueChanged.connect(ui.rotateImage)
        buttonUndoRotation = QToolButton()
        buttonUndoRotation.clicked.connect(ui.undoRotation)
        buttonUndoRotation.setIcon(QIcon('../icons/undo.png'))
        buttonConfirmRotation = QToolButton()
        buttonConfirmRotation.clicked.connect(ui.confirmRotation)
        buttonConfirmRotation.setIcon(QIcon('../icons/check.png'))
        window = QWidget()
        toolBarH = QHBoxLayout()
        toolBarH.setSizeConstraint(QLayout.SetFixedSize)
        toolBarH.addWidget(buttonRotateL)
        toolBarH.addWidget(buttonRotateR)
        toolBarH.addWidget(ui.slider)
        toolBarH.addWidget(buttonUndoRotation)
        toolBarH.addWidget(buttonConfirmRotation)
        window.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        window.setLayout(toolBarH)
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        ui.editToolBarH.addWidget(left_spacer)
        ui.editToolBarH.addWidget(window)
        ui.editToolBarH.addWidget(right_spacer)


def rotateImage(ui, angle):
    image = converPixmapToCV(ui.pixmap_)
    rotated_image = imutils.rotate_bound(image, angle)
    pixmap = QPixmap.fromImage(
        QImage(rotated_image, rotated_image.shape[1], rotated_image.shape[0], rotated_image.strides[0],
               QImage.Format_RGB888).rgbSwapped())
    ui.pixmap = pixmap
    ui.scene.clear()
    ui.scene.setSceneRect(0, 0, ui.pixmap.width(), ui.pixmap.height())
    ui.scene.addPixmap(ui.pixmap)
    ui.scene.update()


def rotateImage90R(ui):
    image = converPixmapToCV(ui.pixmap)
    rotated_image = imutils.rotate_bound(image, -90)
    pixmap = QPixmap.fromImage(
        QImage(rotated_image, rotated_image.shape[1], rotated_image.shape[0], rotated_image.strides[0],
               QImage.Format_RGB888).rgbSwapped())
    ui.pixmap = pixmap
    ui.scene.clear()
    ui.scene.setSceneRect(0, 0, ui.pixmap.width(), ui.pixmap.height())
    ui.scene.addPixmap(ui.pixmap)
    ui.scene.update()


def rotateImage90L(ui):
    image = converPixmapToCV(ui.pixmap)
    rotated_image = imutils.rotate_bound(image, 90)
    pixmap = QPixmap.fromImage(
        QImage(rotated_image, rotated_image.shape[1], rotated_image.shape[0], rotated_image.strides[0],
               QImage.Format_RGB888).rgbSwapped())
    ui.pixmap = pixmap
    ui.scene.clear()
    ui.scene.setSceneRect(0, 0, ui.pixmap.width(), ui.pixmap.height())
    ui.scene.addPixmap(ui.pixmap)
    ui.scene.update()


def undoRotation(ui: ImageCropper):
    ui.slider.setValue(0)
    ui.scene.clear()
    ui.scene.addPixmap(ui.oldPixmap)
    ui.scene.update()


def confirmRotation(ui: ImageCropper):
    ui.oldPixmap = ui.pixmap.copy()


def onBrightnessChanged(ui, value, pixmap):
    ui.labelBrightness.setText('Brightness: {}'.format(value))
    if ui.image is not None and ui.initToolEditSwitch is False:
        ui.temperature = ()
        ui.contrast = ()
        ui.saturation = ()
        ui.sharpness = ()
        ui.highlights = ()
        ui.shadows = ()

        image = converPixmapToCV(pixmap)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        apha = 1 + value / 100
        if len(ui.brightness) > 0:
            pass
        else:
            ui.brightness += (image,)
        enhancer = ImageEnhance.Brightness(ui.brightness[0])
        im_output = enhancer.enhance(apha)
        pixmap_new = convertPILtoPixmap(im_output)
        updateView(ui, pixmap_new)


def onShadowsChanged(ui, value, pixmap):
    ui.labelShadows.setText('Shadows: {}'.format(value))
    if ui.image is not None and ui.initToolEditSwitch is False:
        ui.temperature = ()
        ui.contrast = ()
        ui.saturation = ()
        ui.sharpness = ()
        ui.highlights = ()
        ui.brightness = ()
        image = converPixmapToCV(pixmap)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        apha = 1 - value / 100
        if len(ui.shadows) > 0:
            pass
        else:
            ui.shadows += (image,)
        im_output = ui.shadows[0].point(lambda x: x * apha)
        pixmap_new = convertPILtoPixmap(im_output)
        updateView(ui, pixmap_new)


def onHightlightsChanged(ui, value, pixmap):
    ui.labelHightlights.setText('Hightlights: {}'.format(value))
    if ui.image is not None and ui.initToolEditSwitch is False:
        ui.temperature = ()
        ui.contrast = ()
        ui.saturation = ()
        ui.sharpness = ()
        ui.shadows = ()
        ui.brightness = ()
        image = converPixmapToCV(pixmap)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        apha = 1 + value / 100
        if len(ui.highlights) > 0:
            pass
        else:
            ui.highlights += (image,)
        im_output = ui.highlights[0].point(lambda x: x * apha)
        # im_output = enhancer.enhance(apha)
        pixmap_new = convertPILtoPixmap(im_output)
        updateView(ui, pixmap_new)


def onSharpnessChanged(ui, value, pixmap):
    ui.labelSharpness.setText('Sharpness: {}'.format(value))
    if ui.image is not None and ui.initToolEditSwitch is False:
        ui.temperature = ()
        ui.contrast = ()
        ui.saturation = ()
        ui.highlights = ()
        ui.shadows = ()
        ui.brightness = ()
        image = converPixmapToCV(pixmap)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        apha = 1 + value / 100
        if len(ui.sharpness) > 0:
            pass
        else:
            ui.sharpness += (image,)
        enhancer = ImageEnhance.Sharpness(ui.sharpness[0])
        im_output = enhancer.enhance(apha)
        pixmap_new = convertPILtoPixmap(im_output)
        updateView(ui, pixmap_new)


def onSaturationChanged(ui, value, pixmap):
    ui.labelSaturation.setText('Saturation: {}'.format(value))
    if ui.image is not None and ui.initToolEditSwitch is False:
        ui.temperature = ()
        ui.contrast = ()
        ui.sharpness = ()
        ui.highlights = ()
        ui.shadows = ()
        ui.brightness = ()
        image = converPixmapToCV(pixmap)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        apha = 1 + value / 100
        if len(ui.saturation) > 0:
            pass
        else:
            ui.saturation += (image,)
        enhancer = ImageEnhance.Color(ui.saturation[0])
        im_output = enhancer.enhance(apha)
        pixmap_new = convertPILtoPixmap(im_output)
        updateView(ui, pixmap_new)


def onContrastChanged(ui, value, pixmap):
    ui.labelContrast.setText('Contrast: {}'.format(value))
    if ui.image is not None and ui.initToolEditSwitch is False:
        ui.temperature = ()
        ui.saturation = ()
        ui.sharpness = ()
        ui.highlights = ()
        ui.shadows = ()
        ui.brightness = ()
        image = converPixmapToCV(pixmap)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        apha = 1 + value / 100
        if len(ui.contrast) > 0:
            pass
        else:
            ui.contrast += (image,)
        enhancer = ImageEnhance.Contrast(ui.contrast[0])
        im_output = enhancer.enhance(apha)
        pixmap_new = convertPILtoPixmap(im_output)
        updateView(ui, pixmap_new)


def updateView(ui, pixmap):
    ui.scene.clear()
    ui.scene.addPixmap(pixmap)
    ui.pixmap = pixmap


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


def convertPixmapToba64(pixmap):
    byte_array = QByteArray()
    buffer = QBuffer(byte_array)
    buffer.open(QIODevice.WriteOnly)

    pixmap.save(buffer, 'PNG')
    buffer.close()

    base64_data = base64.b64encode(byte_array)
    return base64_data.decode('utf-8')


def convertBase64ToPixmap(base64_data):
    byte_array = QByteArray(base64.b64decode(base64_data))
    pixmap = QPixmap()
    if not pixmap.loadFromData(byte_array, 'PNG'):
        print("Failed to load image")
    return pixmap
