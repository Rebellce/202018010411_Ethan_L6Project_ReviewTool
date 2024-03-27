from App.ui.myQGraphicsView import myQGraphicsView as myQGraphicsView

from App.modules.fileModule import openIMGFile, saveIMGFile
from App.modules.imgModule import *
from App.modules.textModule import *
from App.modules.OCRModule import *
from App.modules.detectionModule import *
from App.ui.myGauge import myGaugeWidget
from App.ui.myLabelList import myLabelList


class ImageCropper(QMainWindow):
    def __init__(self):
        super().__init__()

        #  init picture settings
        self.detector = None
        self.OCRSwitch = False
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
        self.toolEdit()
        self.setupOCRTab()
        self.setupAITextTab()
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
        width = screen.width() * 0.5
        ratio = 3 / 4
        height = width * ratio  # adjust the ratio
        width = min(width, screen.width() / 2)
        height = min(height, screen.height() * ratio)
        self.left = (screen.width() - width) / 2
        self.top = (screen.height() - height) / 2
        self.setGeometry(int(self.left), int(self.top), int(width), int(height))

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
        self.tabOCR = QWidget()
        self.tabAIText = QWidget()
        # No need to set fixed width for the tabFilter, it will be managed by splitter

        self.tabs.addTab(self.tabEdit, 'ImageEditor')
        self.tabs.addTab(self.tabOCR, 'OCRTool')
        self.tabs.addTab(self.tabAIText, 'AITextDetector')

        # Add the tabs widget to the splitter
        self.splitter.addWidget(self.tabs)
        self.tabs.currentChanged.connect(self.onTabChanged)

        # Add the splitter to the main layout
        self.layout.addWidget(self.splitter)

        initialSizes = [width * 0.75, width * 0.25]
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

    #   ====================  IMG Module Functions ====================
    def zoomIn(self):
        self.painting = False
        zoomIn(self)

    def zoomOut(self):
        self.painting = False
        zoomOut(self)

    #
    def actionZoom(self):
        self.painting = False
        actionZoom(self)

    def crop(self):
        self.painting = False
        crop(self)

    def cropClicked(self):
        self.painting = False
        cropClicked(self)

    def resize(self):
        self.painting = False
        resize(self)

    def buttonClickToResize(self):
        self.painting = False
        buttonClickToResize(self)

    def flipH(self):
        pass
        self.painting = False
        flipH(self)

    def flipV(self):
        pass
        self.painting = False
        flipV(self)

    def rotate(self):
        self.painting = False
        rotate(self)

    def rotateImage(self, angle):
        self.painting = False
        rotateImage(self, angle)

    def rotateImage90R(self):
        rotateImage90R(self)

    def rotateImage90L(self):
        rotateImage90L(self)

    def undoRotation(self):
        undoRotation(self)

    #   ====================  Text Module Functions ====================
    def text(self):
        self.painting = False
        text(self)

    def buttonClickToSetText(self):
        buttonClickToSetText(self)

    def buttonClickToSetTextPixmap(self):
        buttonClickToSetTextPixmap(self)

    def fontColorChanged(self):
        fontColorChanged(self)

    def highlight(self):
        highlight(self)

    def bold(self):
        bold(self)

    def italic(self):
        italic(self)

    def underline(self):
        underline(self)

    def strike(self):
        strike(self)

    def alignLeft(self):
        alignLeft(self)

    def alignRight(self):
        alignRight(self)

    def alignCenter(self):
        alignCenter(self)

    def alignJustify(self):
        alignJustify(self)

    def setupAITextTab(self):
        # 使用QSplitter来创建可调整大小的布局
        splitter = QSplitter(Qt.Vertical)  # 垂直分割器

        controlWidget = QWidget()
        controlLayout = QVBoxLayout()

        self.textEditAIText = QTextEdit()
        self.textEditAIText.setPlaceholderText("Enter text here for AI detection...")
        buttonLayout = QHBoxLayout()
        self.buttonFromOCR = QPushButton("Copy from OCR")
        self.buttonFromOCR.clicked.connect(self.onCopyFromOCR)
        self.buttonAIStart = QPushButton("Start detect")
        self.buttonAIStart.clicked.connect(self.onStartAI)
        self.buttonReloadModel = QPushButton("Reload model")
        self.buttonReloadModel.clicked.connect(self.onReloadModel)
        controlLayout.addWidget(self.textEditAIText)
        controlLayout.addLayout(buttonLayout)
        buttonLayout.addWidget(self.buttonFromOCR)
        buttonLayout.addWidget(self.buttonAIStart)
        buttonLayout.addWidget(self.buttonReloadModel)
        controlWidget.setLayout(controlLayout)
        self.buttonFromOCR.hide()
        self.buttonAIStart.hide()

        self.detectResultWidget = QWidget()
        self.detectResultLayout = QVBoxLayout()
        self.detectResultLayout.setContentsMargins(0, 0, 0, 0)
        self.detectResultLabel = QLabel()
        self.detectResultLayout.addWidget(self.detectResultLabel)
        self.detectResultContent = myLabelList()
        self.detectResultWidget.setLayout(self.detectResultLayout)
        self.detectResultLayout.addWidget(self.detectResultContent)
        self.detectResultContent.hide()

        splitter.addWidget(controlWidget)
        splitter.addWidget(self.detectResultWidget)
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)
        splitter.setSizes([2000, 1000])
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(splitter)
        self.tabAIText.setLayout(mainLayout)

    def setupOCRTab(self):
        ocrLayout = QVBoxLayout()
        _layout = QHBoxLayout()
        # _label = QLabel("Choose model:")
        # _layout.addWidget(_label)

        self.comboBoxInterface = QComboBox()
        self.comboBoxInterface.addItem("Local Engine")
        self.comboBoxInterface.addItem("Online Engine")
        _layout.addWidget(self.comboBoxInterface)

        # self.buttonOCR = QPushButton("识别")
        self.buttonOCR = self._createToolBar('../icons/OCR.png', self.startOCR, "")
        _layout.addWidget(self.buttonOCR)

        self.textEditOCRResult = QTextEdit()
        self.textEditOCRResult.setReadOnly(True)

        ocrLayout.addLayout(_layout)
        ocrLayout.addWidget(self.textEditOCRResult)
        self.tabOCR.setLayout(ocrLayout)

    def toolEdit(self):
        self.hbox = QVBoxLayout()
        # self.labelT = QLabel("Temperature: 0")
        # self._tool(self.labelT, self.onTemperatureChanged)
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
        widgetT.setFixedHeight(100)
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
        backColor = QAction(QIcon("../icons/highlight.png"), "Change background color", self)
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

    def onTabChanged(self, index):
        if self.tabs.tabText(index) == 'AITextDetector':
            # self.myGaugeWidget1.refreshGauge()
            # self.myGaugeWidget2.refreshGauge()
            if self.OCRSwitch:
                self.buttonFromOCR.show()
            else:
                self.buttonFromOCR.hide()
            if self.detector is None:
                self.onReloadModel()
            elif self.detector is False:
                self.buttonAIStart.hide()
            else:
                self.buttonAIStart.show()

    def updateView(self):
        self.scene.clear()
        self.scene.addPixmap(self.pixmap)
        # self.pixmap = pixmap

    def changeColor(self):
        color = QColorDialog.getColor()
        self.brushColor = color

    def onBrightnessChanged(self, value):
        if self.image is not None:
            self.painting = False
            onBrightnessChanged(self, value, self.pixmap)

    def onShadowsChanged(self, value):
        if self.image is not None:
            self.painting = False
            onShadowsChanged(self, value, self.pixmap)

    def onHightlightsChanged(self, value):
        if self.image is not None:
            self.painting = False
            onHightlightsChanged(self, value, self.pixmap)

    def onSharpnessChanged(self, value):
        if self.image is not None:
            self.painting = False
            onSharpnessChanged(self, value, self.pixmap)

    def onSaturationChanged(self, value):
        if self.image is not None:
            self.painting = False
            onSaturationChanged(self, value, self.pixmap)

    def onContrastChanged(self, value):
        if self.image is not None:
            self.painting = False
            onContrastChanged(self, value, self.pixmap)

    def createToolBarV(self):
        self.buttonOpen = self._createToolBar('../icons/plus.png', self.openfile, "Ctrl+O")
        self.buttonSave = self._createToolBar('../icons/save.png', self.savefile, "Ctrl+S")
        self.buttonZoomIn = self._createToolBar('../icons/zoom-in.png', self.zoomIn, "Ctrl+=")
        self.buttonZoomOut = self._createToolBar('../icons/zoom-out.png', self.zoomOut, "Ctrl+-")
        self.buttonCrop = self._createToolBar('../icons/crop.png', self.crop, "Ctrl+X")
        self.buttonFlipH = self._createToolBar('../icons/flipH.png', self.flipH, "Ctrl+H")
        self.buttonFlipV = self._createToolBar('../icons/filpV.png', self.flipV, "Ctrl+V")
        self.buttonResize = self._createToolBar('../icons/resize.png', self.resize, "Ctrl+P")
        self.buttonRotate = self._createToolBar('../icons/rotate.png', self.rotate, "Ctrl+R")
        self.buttonText = self._createToolBar('../icons/text.png', self.text, "Ctrl+T")
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

    #  ====================  OCR Module Functions ====================
    def startOCR(self):
        self.painting = False
        self.buttonOCR.setDisabled(True)
        self.comboBoxInterface.setDisabled(True)
        self.textEditOCRResult.clear()
        if self.comboBoxInterface.currentText() == "Local Engine":
            self.localOCR()
            # print("Local Engine")
        else:
            self.onlineOCR()
            # print("Online Engine")

    def localOCR(self):
        self.painting = False
        localOCR(self)

    def onlineOCR(self):
        self.painting = False
        onlineOCR(self)

    #  ====================  Detection Module Functions ====================
    def onCopyFromOCR(self):
        self.textEditAIText.setText(self.textEditOCRResult.toPlainText())

    def onStartAI(self):
        self.detectResultContent.show()
        self.detector.startAIDetector(self)

    def onReloadModel(self):
        self.buttonAIStart.hide()
        self.detectResultLabel.clear()
        try:
            self.detector = Detector()
        except Exception as e:
            self.detector = False
            self.detectResultLabel.setText(f"<font color='red'>Failed to load model..</font>")
            self.detectResultContent.hide()
            self.buttonReloadModel.show()
        if self.detector:
            self.detectResultLabel.setText(f"<font color='black'>The detection model is ready!</font>")
            self.buttonAIStart.show()
            self.buttonReloadModel.hide()
