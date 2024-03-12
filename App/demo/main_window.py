from PyQt5.QtWidgets import QMainWindow, QLabel, QMenuBar, QStatusBar, QAction, QToolBar


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Educator\'s Assistant')
        self.setGeometry(100, 100, 800, 600)

        # Menu
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('File')

        # Menu Actions
        openAction = QAction('Open', self)
        fileMenu.addAction(openAction)

        # Toolbar
        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)
        toolbar.addAction(openAction)

        # Status Bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")

        # Central Widget
        self.label = QLabel("Hello World!")
        self.setCentralWidget(self.label)

        self.show()

