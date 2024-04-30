from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


def openIMGFile(ui):
    ui.editToolBarH.clear()
    ui.scale = 1
    ui.view.activate = False

    file_name, _ = QFileDialog.getOpenFileName(
        ui, "Open file", ".", "Image Files (*.png *.jpg *.bmp *.jpeg)"
    )
    if not file_name:
        return
    else:
        ui.scene.clear()
        ui.image = QImage(file_name)
        ui.pixmap = QPixmap.fromImage(ui.image)
        ui.oldPixmap = ui.pixmap.copy()
        ui.scene.setSceneRect(0, 0, ui.image.width(), ui.image.height())
        ui.scene.addPixmap(ui.pixmap)
        ui.initEditTool()


def openCloudIMGFile(ui, pixmap):
    ui.editToolBarH.clear()
    ui.scale = 1
    ui.view.activate = False
    ui.scene.clear()
    ui.image = pixmap.toImage()
    ui.pixmap = pixmap
    ui.oldPixmap = ui.pixmap.copy()
    ui.scene.setSceneRect(0, 0, ui.image.width(), ui.image.height())
    ui.scene.addPixmap(ui.pixmap)
    ui.initEditTool()


def saveIMGFile(ui):
    if ui.image is not None:
        ui.editToolBarH.clear()
        ui.view.activate = False
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(ui, "Save Image", "", "Images (*.png *.xpm *.jpg);;All Files (*)",
                                                   options=options)
        if file_name:
            ui.pixmap.save(file_name)


def openAvatarFile(ui):
    file_name, _ = QFileDialog.getOpenFileName(
        ui, "Open file", ".", "Image Files (*.png *.jpg *.bmp *.jpeg)"
    )
    if not file_name:
        return False
    else:
        pixmap = QPixmap(file_name).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        pixmap.save("../icons/avatar.png")
        return True
