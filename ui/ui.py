from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import yaml
# import torch
import numpy as np
# import hydra
# from basicsr.archs.rrdbnet_arch import RRDBNet
# from omegaconf import OmegaConf
# from lb.model.realesrgan.utils import RealESRGANer
# from lb.model.realesrgan.srvggnet import SRVGGNetCompact
# from lb.model.lama.saicinpainting.training.trainers import load_checkpoint
from ui.myQGraphicsView import myQGraphicsView as myQGraphicsView

from modules.fileModule import openIMGFile, saveIMGFile


# from lb.backend.edittool import *
# from lb.backend.filter import *
# from lb.backend.aitools import *
# from lb.backend.general import *

# device = torch.device(f'cuda' if torch.cuda.is_available() else 'cpu')
# checkpoint_path = '/home/thaivv/ImageEditor/lb/model/lama/weight/model/best.ckpt'
# config = '/home/thaivv/ImageEditor/lb/model/lama/weight/config.yaml'

# @hydra.main(config_path="/home/thaivv/ImageEditor/lb/model/lama/configs/prediction", config_name="default.yaml")
# def main(predict_config: OmegaConf):
#     with open(config, 'r') as f:
#         train_config = OmegaConf.create(yaml.safe_load(f))
#     train_config.training_model.predict_only = True
#     model = load_checkpoint(train_config, checkpoint_path, strict=False, map_location='cpu')
#     model.eval()
#     model.to(device)
#     return model


class ImageCropper(QMainWindow):
    def __init__(self):
        super().__init__()

        #  init picture settings
        self.scale = 1
        self.image = None
        self.painting = False
        self.temperature = ()
        self.contrast = ()
        self.saturation = ()
        self.sharpness = ()
        self.highlights = ()
        self.shadows = ()
        self.brightness = ()

        #  init user interface
        self.initUI()

        #  init model
        self.toolFilter()
        self.toolEdit()
        self.createToolBarV()
        self.initPaint()

    def initPaint(self):
        self.drawing = False
        self.brushSize = 9
        self.brushColor = Qt.black
        self.lastPoint = QPoint()

    def initUI(self):
        # set window size and position
        screen = QDesktopWidget().screenGeometry()
        self.width = screen.width() * 0.5
        ratio = 3 / 4
        self.height = self.width * ratio  # adjust the ratio
        self.width = min(self.width, screen.width() / 2)
        self.height = min(self.height, screen.height() * ratio)
        self.left = (screen.width() - self.width) / 2
        self.top = (screen.height() - self.height) / 2
        self.setGeometry(int(self.left), int(self.top), int(self.width), int(self.height))

        # overview of the window
        self.setWindowTitle("Educational Assistant Tool")
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        # create a scene and a view to display the image
        self.scene = QGraphicsScene()
        self.view = myQGraphicsView()
        self.view.setScene(self.scene)
        self.transform = self.view.transform()

        # Create a horizontal layout and a horizontal splitter
        self.layout = QHBoxLayout(self.centralWidget)
        self.splitter = QSplitter(Qt.Horizontal)  # Use horizontal splitter

        # Add the view to the splitter
        self.splitter.addWidget(self.view)
        self.view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create tabs for overview the image and filtering
        self.tabs = QTabWidget()
        self.tabEdit = QWidget()
        self.tabFilter = QWidget()
        # No need to set fixed width for the tabFilter, it will be managed by splitter

        self.tabs.addTab(self.tabEdit, 'Edit Image')
        self.tabs.addTab(self.tabFilter, 'Filter')

        # Add the tabs widget to the splitter
        self.splitter.addWidget(self.tabs)

        # Add the splitter to the main layout
        self.layout.addWidget(self.splitter)

        initialSizes = [self.width * 0.75, self.width * 0.25]
        self.splitter.setSizes(initialSizes)

        # The splitter handle allows resizing of the contained widgets
        self.splitter.setCollapsible(0, False)  # Disable collapsing for the view
        self.splitter.setCollapsible(1, False)  # Disable collapsing for the tab bar

        # create two toolbars for editing
        self.editToolBarV = QToolBar(self)
        self.editToolBarH = QToolBar(self)
        self.addToolBar(Qt.LeftToolBarArea, self.editToolBarV)
        self.addToolBar(Qt.TopToolBarArea, self.editToolBarH)
        self.editToolBarH.setFixedHeight(50)

        self.dentaX = self.editToolBarV.width()
        self.dentaY = self.editToolBarH.height()
        self.show()

#   ====================  File Module Functions ====================

    def openfile(self):
        self.painting = False
        openIMGFile(self)

    def savefile(self):
        self.painting = False
        saveIMGFile(self)

    def toolFilter(self):
        self.hboxTool = QVBoxLayout()
        self.blur, self.blurBin = self.createtoolFilter('Box blur', self.boxBlur, True)
        self.blur1, self.gaus = self.createtoolFilter('Gaussian blur', self.gaussianBlur, True)
        self.blur2, self.med = self.createtoolFilter('Median blur', self.medianBlur, True)
        self.hboxTool.addWidget(self.blur)
        self.hboxTool.addWidget(self.blur1)
        self.hboxTool.addWidget(self.blur2)
        self.tabFilter.setLayout(self.hboxTool)

    def createtoolFilter(self, name, log, flag):
        hboxTool = QHBoxLayout()
        widgetFilter = QWidget()
        button_action = QPushButton(name)
        button_action.clicked.connect(log)
        spinBoxW = QSpinBox()
        spinBoxW.setMinimum(1)
        spinBoxW.setSingleStep(2)
        spinBoxW.setValue(3)
        if flag:
            hboxTool.addWidget(spinBoxW)
        hboxTool.addWidget(button_action)
        widgetFilter.setLayout(hboxTool)
        return widgetFilter, spinBoxW

    def toolEdit(self):
        self.hbox = QVBoxLayout()
        self.labelT = QLabel("Temperature: 0")
        self._tool(self.labelT, self.onTemperatureChanged)
        self.labelContrast = QLabel("Contrast: 0")
        self._tool(self.labelContrast, self.onContrastChanged)
        # Saturation
        self.labelSaturation = QLabel("Saturation: 0")
        self._tool(self.labelSaturation, self.onSaturationChanged)
        # Exposure
        self.labelSharpness = QLabel("Sharpness: 0")
        self._tool(self.labelSharpness, self.onSharpnessChanged)
        # Hightlights
        self.labelHightlights = QLabel("Hightlights: 0")
        self._tool(self.labelHightlights, self.onHightlightsChanged)
        # Shadows
        self.labelShadows = QLabel("Shadows: 0")
        self._tool(self.labelShadows, self.onShadowsChanged)
        # Brightness
        self.labelBrightness = QLabel("Brightness: 0")
        self._tool(self.labelBrightness, self.onBrightnessChanged)
        self.tabEdit.setLayout(self.hbox)

    def _tool(self, label, log):
        vbox = QVBoxLayout()
        widgetT = QWidget()
        widgetT.setFixedHeight(60)
        sliderTem = QSlider(Qt.Horizontal)
        sliderTem.setMinimum(-100)
        sliderTem.setMaximum(100)
        sliderTem.valueChanged.connect(log)
        vbox.addWidget(label)
        vbox.addWidget(sliderTem)
        widgetT.setLayout(vbox)
        self.hbox.addWidget(widgetT)

    def superResolution(self):
        if self.image is not None:
            self.painting = False
            # superResolution(self, self.pixmap)

    def inpainting(self):
        self.painting = True
        self.pixmapBlack = QPixmap(self.pixmap.size())
        self.pixmapBlack.fill(Qt.black)
        self.editToolBarH.clear()
        backColor = QAction(QIcon("icons/highlight.png"), "Change background color", self)
        backColor.triggered.connect(self.changeColor)
        px_7 = QAction('7px', self)
        px_7.triggered.connect(self.changeSize7px)
        px_9 = QAction('9px', self)
        px_9.triggered.connect(self.changeSize9px)
        px_13 = QAction('13px', self)
        px_13.triggered.connect(self.changeSize13px)
        px_17 = QAction('17px', self)
        px_17.triggered.connect(self.changeSize17px)
        px_21 = QAction('21px', self)
        px_21.triggered.connect(self.changeSize21px)
        finish = QAction('OK', self)
        finish.triggered.connect(self.lama)
        self.editToolBarH.addAction(backColor)
        self.editToolBarH.addAction(px_7)
        self.editToolBarH.addAction(px_9)
        self.editToolBarH.addAction(px_13)
        self.editToolBarH.addAction(px_17)
        self.editToolBarH.addAction(px_21)
        self.editToolBarH.addAction(finish)

    def lama(self):
        pass
        # lama(self, self.pixmap, self.pixmapBlack)

    def changeSize7px(self):
        self.brushSize = 7

    def changeSize9px(self):
        self.brushSize = 9

    def changeSize13px(self):
        self.brushSize = 13

    def changeSize17px(self):
        self.brushSize = 17

    def changeSize21px(self):
        self.brushSize = 21

    def mousePressEvent(self, event):
        if self.painting and self.image is not None:
            # if left mouse button is pressed
            if event.button() == Qt.LeftButton:
                # make drawing flag true
                self.drawing = True
                # make last point to the point of cursor
                self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if self.painting and self.image is not None:
            # checking if left button is pressed and drawing flag is true
            if (event.buttons() & Qt.LeftButton) & self.drawing:
                # creating painter object
                painter = QPainter(self.pixmap)
                painterBlack = QPainter(self.pixmapBlack)

                # set the pen of the painter
                painter.setPen(QPen(self.brushColor, self.brushSize,
                                    Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                painterBlack.setPen(QPen(Qt.white, self.brushSize,
                                         Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

                # draw line from the last point of cursor to the current point
                point1 = self.view.mapToScene(self.lastPoint)
                point2 = self.view.mapToScene(event.pos())
                point3 = QPointF(point1.x() - 1.5 * self.dentaY, point1.y() - self.dentaX / 2)
                point4 = QPointF(point2.x() - 1.5 * self.dentaY, point2.y() - self.dentaX / 2)
                painter.drawLine(point3, point4)
                painterBlack.drawLine(point3, point4)
                # self.view.mapToScene(event.pos())

                # change the last point
                self.lastPoint = event.pos()
                # update
                self.updateView()

    def mouseReleaseEvent(self, event):
        if self.painting and self.image is not None:
            if event.button() == Qt.LeftButton:
                # make drawing flag false
                self.drawing = False

    def paintEvent(self, event):
        if self.painting and self.image is not None:
            # create a canvas
            canvasPainter = QPainter()
            # draw rectangle  on the canvas
            canvasPainter.drawPixmap(self.rect(), self.pixmap, self.pixmap.rect())

    def updateView(self):
        self.scene.clear()
        self.scene.addPixmap(self.pixmap)
        # self.pixmap = pixmap

    def changeColor(self):
        color = QColorDialog.getColor()
        self.brushColor = color

    def emboss(self):
        if self.image is not None:
            self.painting = False
            # emboss(self, self.pixmap)

    def boxBlur(self):
        if self.image is not None:
            self.painting = False
            # boxBlur(self, self.pixmap)

    def gaussianBlur(self):
        if self.image is not None:
            self.painting = False
            # gaussianBlur(self, self.pixmap)

    def medianBlur(self):
        if self.image is not None:
            self.painting = False
            # medianBlur(self, self.pixmap)

    def onBrightnessChanged(self, value):
        if self.image is not None:
            self.painting = False
            # onBrightnessChanged(self, value, self.pixmap)

    def onShadowsChanged(self, value):
        if self.image is not None:
            self.painting = False
            # onShadowsChanged(self, value, self.pixmap)

    def onHightlightsChanged(self, value):
        if self.image is not None:
            self.painting = False
            # onHightlightsChanged(self, value,self.pixmap)

    def onSharpnessChanged(self, value):
        if self.image is not None:
            self.painting = False
            # onSharpnessChanged(self, value, self.pixmap)

    def onSaturationChanged(self, value):
        if self.image is not None:
            self.painting = False
            # onSaturationChanged(self, value, self.pixmap)

    def onContrastChanged(self, value):
        if self.image is not None:
            self.painting = False
            # onContrastChanged(self, value, self.pixmap)

    def onTemperatureChanged(self, value):
        if self.image is not None:
            self.painting = False
            # onTemperatureChanged(self, value, self.pixmap)

    def createToolBarV(self):
        self.buttonOpen = self._createToolBar('../icons/plus.png', self.openfile, "Ctrl+O")
        self.buttonSave = self._createToolBar('../icons/save.png', self.savefile, "Ctrl+S")
        self.buttonZoomIn = self._createToolBar('../icons/zoom-in.png', self.zoomIn, "Ctrl++")
        self.buttonZoomOut = self._createToolBar('../icons/zoom-out.png', self.zoomOut, "Ctrl+-")
        self.buttonCrop = self._createToolBar('../icons/crop.png', self.crop, "Ctrl+A")
        self.buttonFlipH = self._createToolBar('../icons/flipH.png', self.flipH, "Ctrl+A")
        self.buttonFlipV = self._createToolBar('../icons/filpV.png', self.flipV, "Ctrl+A")
        self.buttonResize = self._createToolBar('../icons/resize.png', self.resize, "Ctrl+A")
        self.buttonRotate = self._createToolBar('../icons/rotate.png', self.rotate, "Ctrl+A")
        self.buttonText = self._createToolBar('../icons/text.png', self.text, "Ctrl+A")
        self.listTool = [self.buttonOpen, self.buttonSave, self.buttonZoomIn, self.buttonZoomOut, self.buttonCrop,
                         self.buttonFlipH, self.buttonFlipV, \
                         self.buttonResize, self.buttonRotate, self.buttonText]
        for bt in self.listTool:
            bt.clicked.connect(self.button_clicked)

    def button_clicked(self):

        sender = self.sender()
        sender.setChecked(True)
        for button in self.listTool:
            if button != sender:
                button.setChecked(False)

    def _createToolBar(self, name, log, shortCut):
        window = QWidget()
        button = QVBoxLayout()
        toolButton = QToolButton(self)
        toolButton.setAutoRaise(True)
        toolButton.clicked.connect(log)
        toolButton.setShortcut(QKeySequence(shortCut))
        toolButton.setIcon(QIcon(name))
        toolButton.setIconSize(QSize(25, 25))
        toolButton.setCheckable(True)
        button.addWidget(toolButton)
        spacer = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Fixed)
        button.addItem(spacer)
        window.setLayout(button)
        self.editToolBarV.addWidget(window)
        return toolButton

    def zoomIn(self):
        pass
        # self.painting = False
        # zoomIn(self)

    def zoomOut(self):
        pass
        # self.painting = False
        # zoomOut(self)

    def actionZoom(self):
        pass
        # self.painting = False
        # actionZoom(self)

    def resize(self):
        pass
        # self.painting = False
        # resize(self)

    def buttonClickToResize(self):
        pass
        # self.painting = False
        # buttonClickToResize(self)

    def crop(self):
        pass
        # self.painting = False
        # crop(self)

    def buttonClicked(self):
        pass
        # self.painting = False
        # buttonClicked(self)

    def flipH(self):
        pass
        # self.painting = False
        # flipH(self)

    def flipV(self):
        pass
        # self.painting = False
        # flipV(self)

    def rotate(self):
        pass
        # self.painting = False
        # rotate(self)

    def rotateImage(self, angle):
        pass
        # self.painting = False
        # rotateImage(self, angle)

    def rotateImage90(self):
        pass
        # rotateImage90(self)

    def rotateImage_90(self):
        pass
        # rotateImage_90(self)

    def text(self):
        pass
        # self.painting = False
        # text(self)

    def buttonClickToSetText(self):
        pass
        # buttonClickToSetText(self)

    def buttonClickToSetTextPixmap(self):
        pass
        # buttonClickToSetTextPixmap(self)

    def fontColorChanged(self):
        pass
        # fontColorChanged(self)

    def highlight(self):
        pass

    # highlight(self)

    def bold(self):
        pass
        # bold(self)
        #

    def italic(self):
        pass
        # italic(self)

    def underline(self):
        pass
        # underline(self)

    def strike(self):
        pass
        # strike(self)

    def alignLeft(self):
        pass
        # alignLeft(self)

    def alignRight(self):
        pass
        # alignRight(self)

    def alignCenter(self):
        pass
        # alignCenter(self)

    def alignJustify(self):
        pass
        # alignJustify(self)
