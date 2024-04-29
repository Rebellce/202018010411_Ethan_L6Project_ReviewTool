import re

from App.ui.myQGraphicsView import myQGraphicsView as myQGraphicsView

from App.modules.fileModule import openIMGFile, saveIMGFile, openAvatarFile
from App.modules.imgModule import *
from App.modules.textModule import *
from App.modules.OCRModule import *
from App.modules.detectionModule import *
from App.modules.userModule import *
from App.ui.myLabelList import myLabelList


class ImageCropper(QMainWindow):
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    PASSWORD_PATTERN = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,12}$')

    def __init__(self):
        super().__init__()

        #  init picture settings

        self.user = UserModule()
        self.userName = ""
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
        self.pixmap = None
        self.oldPixmap = None

        #  init user interface
        self.initUI()

        #  init model
        self.detector = Detector()
        self.toolEdit()
        self.setupOCRTab()
        self.setupAITextTab()
        self.initUserTab()
        self.createToolBarV()
        self.initPaint()

        # init threads
        self.OCRThread = None
        self.detectThread = None

        # init ui status
        self.OCRSwitch = False  # this switch is used to control the OCR button in the AITextDetector tab
        self.toolEditBtnSwitch = False  # this switch is used to control the tool edit button in the ImageEditor tab
        self.initToolEditSwitch = False  # if set to True, when the edit slider value is changed, the picture will be not be updated

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
        self.tabUser = QWidget()
        # No need to set fixed width for the tabFilter, it will be managed by splitter

        self.tabs.addTab(self.tabEdit, 'ImageEditor')
        self.tabs.addTab(self.tabOCR, 'OCRTool')
        self.tabs.addTab(self.tabAIText, 'AITool')
        self.tabs.addTab(self.tabUser, 'User')
        self.tabs.setTabVisible(0, False)
        self.tabs.currentChanged.connect(self.onTabChanged)

        # Create a widget for user information
        self.userWidget = QWidget()
        # Add the tabs widget to the splitter
        rightSplitter = QSplitter(Qt.Vertical)
        rightSplitter.addWidget(self.tabs)
        rightSplitter.setCollapsible(0, False)
        rightSplitter.addWidget(self.userWidget)
        self.splitter.addWidget(rightSplitter)
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

    #  ====================  User Module Functions ====================
    def initUserTab(self):
        self.user.initUser(self)
        self.userTablayout = QVBoxLayout()
        self.tabUser.setLayout(self.userTablayout)
        self.userTabLabel = QLabel("")
        self.userTabLabel.setFixedHeight(40)
        self.userTabLabel.setWordWrap(True)
        self.userTablayout.addWidget(self.userTabLabel)
        self.userTablayout.setContentsMargins(5, 0, 5, 0)
        self.initUserMini()
        self.initLogin()
        self.initRegister()
        self.initUserMain()
        self.jumpToLogin(None)

    def initUserMini(self):
        self.userWidget.setFixedHeight(80)
        self.userName = "Ethan Zhu"
        filePath = "../icons/avatar.png"
        self.userLayout = QHBoxLayout()
        self.userLabelLayoutV = QVBoxLayout()
        self.userLabelWidgetV = QWidget()
        self.userLabelLayoutV.setContentsMargins(0, 0, 0, 0)  # Set all margins to zero
        self.userLabelLayoutV.setSpacing(0)  # Set spacing to zero

        self.userLabelWidgetV.setLayout(self.userLabelLayoutV)
        self.userLabel = QLabel(f"Hello, {self.userName}")
        self.userLabel.setWordWrap(True)
        self.userLabel.setFixedHeight(40)

        self.avatar = QLabel()
        self.avatar.setFixedSize(50, 50)
        self.avatar.setStyleSheet(f"""
            QLabel {{
                border-radius: 25px;  
            border: 2px solid black;
            background-image: url('{filePath}');
            background-position: center;
            background-repeat: no-repeat;
            }}
        """)
        self.avatar.mousePressEvent = self.openAvatarFile
        self.userLayout.addWidget(self.avatar)
        self.userLayout.addWidget(self.userLabelWidgetV)
        self.userLabelLayoutV.addWidget(self.userLabel)
        self.userWidget.setLayout(self.userLayout)
        self.userWidget.mousePressEvent = self.jumpToUserTab
        self.userWidget.hide()

    def initRegister(self):
        self.regPromptBoxes = {}
        self.registerWidget = QWidget()
        mainLayout = QVBoxLayout()

        self.firstNameInput = QLineEdit()
        self.firstNameInput.setMaxLength(20)
        self.firstNameInput.setPlaceholderText("Enter first name..")
        self.createLineEdit("First Name:", self.firstNameInput, mainLayout, self.regPromptBoxes)
        self.firstNameInput.mousePressEvent = self.initRegPrompt

        self.lastNameInput = QLineEdit()
        self.lastNameInput.setMaxLength(20)
        self.lastNameInput.setPlaceholderText("Enter last name..")
        self.createLineEdit("Last Name:", self.lastNameInput, mainLayout, self.regPromptBoxes)
        self.lastNameInput.mousePressEvent = self.initRegPrompt

        self.emailInput = QLineEdit()
        self.emailInput.setMaxLength(50)
        self.emailInput.setPlaceholderText("Enter email..")
        self.createLineEdit("Email:", self.emailInput, mainLayout, self.regPromptBoxes)
        self.emailInput.mousePressEvent = self.initRegPrompt

        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.passwordInput.setMaxLength(20)
        self.passwordInput.setPlaceholderText("Enter password..")
        self.createLineEdit("Password:", self.passwordInput, mainLayout, self.regPromptBoxes)
        self.passwordInput.mousePressEvent = self.initRegPrompt

        self.confirmPasswordInput = QLineEdit()
        self.confirmPasswordInput.setEchoMode(QLineEdit.Password)
        self.confirmPasswordInput.setMaxLength(20)
        self.confirmPasswordInput.setPlaceholderText("Confirm password..")
        self.createLineEdit("Confirm Password:", self.confirmPasswordInput, mainLayout, self.regPromptBoxes)
        self.confirmPasswordInput.mousePressEvent = self.initRegPrompt

        buttonsLayout = QHBoxLayout()
        self.registerButton = QPushButton("OK")
        self.registerButton.clicked.connect(self.onRegister)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.jumpToLogin)
        buttonsLayout.addWidget(self.registerButton)
        buttonsLayout.addWidget(self.cancelButton)
        mainLayout.addLayout(buttonsLayout)

        self.registerTip = QLabel("This part is for test")
        self.registerTip.setStyleSheet("color:red; font-family:SimHei; font-size:12pt;")
        self.registerTip.setFixedHeight(20)
        self.registerTip.setWordWrap(True)
        self.registerTip.hide()
        mainLayout.addWidget(self.registerTip)

        self.registerWidget.setLayout(mainLayout)
        self.userTablayout.addWidget(self.registerWidget)

    def initLogin(self):
        self.loginPromptBoxes = {}
        self.loginWidget = QWidget()
        self.userLoginSplitter = QSplitter(Qt.Vertical)
        loginLayout = QVBoxLayout()
        self.loginWidget.setLayout(loginLayout)
        self.loginEmailInput = QLineEdit()
        self.loginEmailInput.setMaxLength(50)
        self.loginEmailInput.setPlaceholderText("Enter email..")
        self.createLineEdit("Email:", self.loginEmailInput, loginLayout, self.loginPromptBoxes)
        self.loginEmailInput.mousePressEvent = self.initLoginPrompt

        self.loginPasswordInput = QLineEdit()
        self.loginPasswordInput.setEchoMode(QLineEdit.Password)
        self.loginPasswordInput.setMaxLength(20)
        self.loginPasswordInput.setPlaceholderText("Enter password..")
        self.createLineEdit("Password:", self.loginPasswordInput, loginLayout, self.loginPromptBoxes)
        self.loginPasswordInput.mousePressEvent = self.initLoginPrompt
        buttonsLayout = QVBoxLayout()
        self.loginButton = QPushButton("login")
        self.loginButton.clicked.connect(self.onLogin)

        gotoRegisterLabel = QLabel("new comers? go to register")
        gotoRegisterLabel.setStyleSheet("""
                color:gray;
                font-family:SimHei; 
                font-size:10pt; 
                text-decoration: underline;
        """)
        gotoRegisterLabel.setAlignment(Qt.AlignCenter)
        gotoRegisterLabel.mousePressEvent = self.jumpToRegister

        buttonsLayout.addWidget(self.loginButton)
        buttonsLayout.addWidget(gotoRegisterLabel)
        loginLayout.addLayout(buttonsLayout)

        infoLayout = QHBoxLayout()
        infoWidget = QWidget()
        infoWidget.setLayout(infoLayout)
        pixmap = QPixmap("../icons/cloud-download.png")
        pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio)
        label = QLabel()
        label.setPixmap(pixmap)
        infoLayout.addWidget(label)
        infoLayout.addWidget(QLabel("Login to access your files."))
        infoLayout.setAlignment(Qt.AlignCenter)

        self.userLoginSplitter.addWidget(self.loginWidget)
        self.userLoginSplitter.addWidget(infoWidget)
        self.userLoginSplitter.setCollapsible(0, False)
        self.userLoginSplitter.setCollapsible(1, False)
        self.userLoginSplitter.setSizes([500, 2000])

        self.userTablayout.addWidget(self.userLoginSplitter)

    def initUserMain(self):
        self.userMainSplitter = QSplitter(Qt.Vertical)

        userLoggedInLayout = QVBoxLayout()
        self.userLoggedInWidget = QWidget()
        self.userLoggedInWidget.setLayout(userLoggedInLayout)
        self.userLoggedInWidget.setFixedHeight(60)
        buttonsLayout2 = QHBoxLayout()
        buttonsWidget2 = QWidget()
        buttonsWidget2.setLayout(buttonsLayout2)
        buttonsWidget2.setFixedHeight(50)
        buttonsLayout2.setContentsMargins(0, 0, 0, 0)
        self.userLogOutButton = QPushButton("Log out")
        self.userLogOutButton.clicked.connect(self.logout)
        buttonsLayout2.addWidget(self.userLogOutButton)
        userLoggedInLayout.addWidget(buttonsWidget2)

        infoLayout = QHBoxLayout()
        infoWidget = QWidget()
        infoWidget.setLayout(infoLayout)
        infoLayout.addWidget(QLabel("Why?"))

        self.userMainSplitter.addWidget(self.userLoggedInWidget)
        self.userMainSplitter.addWidget(infoWidget)
        self.userMainSplitter.setCollapsible(0, False)
        self.userMainSplitter.setCollapsible(1, False)
        self.userMainSplitter.setSizes([300, 2000])

        self.userTablayout.addWidget(self.userMainSplitter)

    def createLineEdit(self, label, lineEdit, mainLayout, promptBoxes):
        promptLabel = QLabel()
        promptLabel.setStyleSheet("color:red; font-family:SimHei; font-size:11pt;")
        promptLabel.setText("")
        promptBoxes[lineEdit] = promptLabel
        layout = QVBoxLayout()
        widget = QWidget()
        widget.setFixedHeight(100)
        widget.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)
        layout.addWidget(QLabel(label))
        layout.addWidget(lineEdit)
        layout.addWidget(promptLabel)
        mainLayout.addWidget(widget)

    def setPrompt(self, lineEdit, label, promptBoxes):
        promptBoxes[lineEdit].setText(label)

    def initRegPrompt(self, event):
        self.registerTip.hide()
        for lineEdit, prompt in self.regPromptBoxes.items():
            self.setPrompt(lineEdit, "", self.regPromptBoxes)

    def initLoginPrompt(self, event):
        for lineEdit, prompt in self.loginPromptBoxes.items():
            self.setPrompt(lineEdit, "", self.loginPromptBoxes)

    def onRegister(self):
        for lineEdit, prompt in self.regPromptBoxes.items():
            if not lineEdit.text():
                self.setPrompt(lineEdit, "This field is required.", self.regPromptBoxes)
                return
        if not self.validateEmail(self.emailInput.text()):
            self.regPromptBoxes[self.emailInput].setText("Invalid email address.")
            return
        result = self.validatePassword(self.passwordInput.text())
        if result != "":
            self.regPromptBoxes[self.passwordInput].setText(result)
            return
        if self.passwordInput.text() != self.confirmPasswordInput.text():
            self.setPrompt(self.confirmPasswordInput, "Passwords do not match.", self.regPromptBoxes)
            return
        self.register()

    def onLogin(self):
        for lineEdit, prompt in self.loginPromptBoxes.items():
            if not lineEdit.text():
                self.setPrompt(lineEdit, "This field is required.", self.loginPromptBoxes)
                return
        if not self.validateEmail(self.loginEmailInput.text()):
            self.loginPromptBoxes[self.loginEmailInput].setText("Invalid email address.")
            return
        self.login()

    def validateEmail(self, email):
        if not self.EMAIL_PATTERN.match(email):
            return False
        return True

    def validatePassword(self, password):
        if len(password) < 6:
            return "Least 6 characters long."
        elif len(password) > 12:
            return "Most 12 characters long."
        elif not self.PASSWORD_PATTERN.match(password):
            return "Need letters & numbers."
        else:
            return ""

    def register(self):
        self.tabUser.setDisabled(True)
        data = {
            "email": self.emailInput.text(),
            "password": getSha256(self.passwordInput.text()),
            "firstName": self.firstNameInput.text(),
            "lastName": self.lastNameInput.text()
        }
        self.user.register(data)

    def responseRegister(self, message, status):
        self.tabUser.setDisabled(False)
        if status == 200:
            self.tabUser.setDisabled(True)
        elif status == 400:
            self.setPrompt(self.emailInput, message, self.regPromptBoxes)
        elif status == -1:
            self.registerTip.setText(message)
            self.registerTip.show()
        else:
            assert False, "Unknown status code"

    def login(self):
        self.tabUser.setDisabled(True)
        data = {
            "email": self.loginEmailInput.text(),
            "password": getSha256(self.loginPasswordInput.text())
        }
        self.user.login(data)

    def responseLogin(self, message, status):
        self.tabUser.setDisabled(False)
        if status == 200:
            self.tabUser.setDisabled(True)
        elif status == 400 or status == -1:
            self.setPrompt(self.loginPasswordInput, message, self.loginPromptBoxes)
        else:
            assert False, "Unknown status code"

    def logout(self):
        self.tabUser.setDisabled(True)
        self.user.logout()

    def responseLogout(self):
        self.tabUser.setDisabled(False)
        self.jumpToLogin(None)
        self.userWidget.hide()

    def jumpToUserTab(self, event):
        self.tabs.setCurrentIndex(3)

    def jumpToRegister(self, event):
        self.userLoginSplitter.hide()
        self.userMainSplitter.hide()
        self.userTabLabel.setText("<h2>Register:</h2>")
        self.registerWidget.show()

    def jumpToLogin(self, event):
        self.userMainSplitter.hide()
        self.registerWidget.hide()
        self.userTabLabel.setText("<h2>Login:</h2>")
        self.userLoginSplitter.show()

    def jumpToUserLoggedIn(self):
        if self.user.state == 1:
            self.userLoginSplitter.hide()
            self.registerWidget.hide()
            self.userName = f"{self.user.firstName} {self.user.lastName}"
            self.userTabLabel.setText(f"The account of <b><u>{self.user.email}</u></b>")
            self.userLabel.setText(f"Welcome back,  <b>{self.userName} 🍒</b>")
            self.userMainSplitter.show()
            self.userWidget.show()
            self.tabUser.setDisabled(False)


    #   ====================  File Module Functions ====================
    def openAvatarFile(self, event):
        if openAvatarFile(self):
            self.avatar.setStyleSheet(f"""
                QLabel {{
                    border-radius: 25px;  
                border: 2px solid black;
                background-image: url('../icons/avatar.png');
                background-position: center;
                background-repeat: no-repeat;
                }}
            """)

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

    def confirmRotation(self):
        confirmRotation(self)

    def edit(self):
        edit(self)

    def undoEdit(self):
        undoEdit(self)

    #   ====================  Text Module Functions ====================
    def text(self):
        self.painting = False
        if self.image is not None:
            initEditTool(self)
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
        self.buttonReloadModel.hide()

        self.detectResultWidget = QWidget()
        self.detectResultLayout = QVBoxLayout()
        self.detectResultLayout.setContentsMargins(0, 0, 0, 0)
        self.detectResultLabel = QLabel()
        self.detectResultLabel.setWordWrap(True)
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

        self.buttonOCR = self._createToolBar('../icons/OCR.png', self.startOCR, "")
        _layout.addWidget(self.buttonOCR)

        self.textEditOCRResult = QTextEdit()
        self.textEditOCRResult.setReadOnly(True)

        ocrLayout.addLayout(_layout)
        ocrLayout.addWidget(self.textEditOCRResult)
        self.tabOCR.setLayout(ocrLayout)

    def toolEdit(self):
        self.adjustments = {
            'brightness': onBrightnessChanged,
            'shadows': onShadowsChanged,
            'highlights': onHightlightsChanged,
            'sharpness': onSharpnessChanged,
            'saturation': onSaturationChanged,
            'contrast': onContrastChanged
        }
        self.sliderList = []
        self.hbox = QVBoxLayout()
        self.labelContrast = QLabel("Contrast: 0")
        self._tool(self.labelContrast, 'contrast')
        # Saturation
        self.labelSaturation = QLabel("Saturation: 0")
        self._tool(self.labelSaturation, 'saturation')
        # Exposure
        self.labelSharpness = QLabel("Sharpness: 0")
        self._tool(self.labelSharpness, 'sharpness')
        # Hightlights
        self.labelHightlights = QLabel("Hightlights: 0")
        self._tool(self.labelHightlights, 'highlights')
        # Shadows
        self.labelShadows = QLabel("Shadows: 0")
        self._tool(self.labelShadows, 'shadows')
        # Brightness
        self.labelBrightness = QLabel("Brightness: 0")
        self._tool(self.labelBrightness, 'brightness')
        self.tabEdit.setLayout(self.hbox)

    def _tool(self, label, adjustment, log=None):
        if log is None:
            log = self.onAdjustmentChanged
        vbox = QVBoxLayout()
        widgetT = QWidget()
        widgetT.setFixedHeight(100)
        sliderTem = QSlider(Qt.Horizontal)
        self.sliderList.append(sliderTem)
        sliderTem.setMinimum(-100)
        sliderTem.setMaximum(100)
        sliderTem.valueChanged.connect(lambda value: log(adjustment, value))
        vbox.addWidget(label)
        vbox.addWidget(sliderTem)
        widgetT.setLayout(vbox)
        self.hbox.addWidget(widgetT)

    def initEditTool(self):
        initEditTool(self)

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
        if self.tabs.tabText(index) == 'AITool':
            # self.myGaugeWidget1.refreshGauge()
            # self.myGaugeWidget2.refreshGauge()
            if self.OCRSwitch:
                self.buttonFromOCR.show()
            else:
                self.buttonFromOCR.hide()
            if self.detector.initState is None:
                self.onReloadModel()
            elif self.detector.initState is False:
                self.buttonAIStart.hide()
            else:
                self.buttonAIStart.show()
        elif self.tabs.tabText(index) == 'User':
            if self.user.state == 0:
                if self.user.loadCookies():
                    self.user.getUser()


    def updateView(self):
        self.scene.clear()
        self.scene.addPixmap(self.pixmap)
        # self.pixmap = pixmap

    def changeColor(self):
        color = QColorDialog.getColor()
        self.brushColor = color

    def onAdjustmentChanged(self, adjustment, value):

        if self.image is not None:
            self.painting = False
            function = self.adjustments.get(adjustment)
            if function:
                function(self, value, self.pixmap)
                if not self.toolEditBtnSwitch:
                    showEditTools(self)
                    self.toolEditBtnSwitch = True
            else:
                assert False, "Adjustment type not recognized"

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
        self.buttonToolEdit = self._createToolBar('../icons/Colorful.png', self.edit, "Ctrl+E")
        self.listTool = [self.buttonOpen, self.buttonSave, self.buttonZoomIn, self.buttonZoomOut, self.buttonCrop,
                         self.buttonFlipH, self.buttonFlipV, \
                         self.buttonResize, self.buttonRotate, self.buttonText, self.buttonToolEdit]
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
        self.textEditAIText.setDisabled(True)
        self.detectResultLabel.clear()
        self.detectResultLabel.setText("Loading model...Please ensure the network connected...")
        self.detectThread = DetectThread(self.detector)
        self.detectThread.start()
        self.detectThread.finished.connect(self.loadModelResult)

    def loadModelResult(self, _text="", errorFlag=False):
        self.detectResultLabel.clear()
        if errorFlag:
            self.detectResultLabel.setText(formatError(_text))
            self.detector.initState = False
            self.detectResultContent.hide()
            self.buttonReloadModel.show()
        else:
            self.detectResultLabel.setText(formatNormal(_text))
            self.detector.initState = True
            self.buttonAIStart.show()
            self.buttonReloadModel.hide()
        self.textEditAIText.setDisabled(False)
