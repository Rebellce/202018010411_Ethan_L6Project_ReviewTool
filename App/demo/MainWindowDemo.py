from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QDockWidget, QListWidget, QTabWidget, QApplication, QPushButton, \
    QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置主窗口的中心区域
        self.centralWidget = QTextEdit()
        self.setCentralWidget(self.centralWidget)

        # 添加侧边工具栏
        self.addDockWidget(Qt.LeftDockWidgetArea, self.createDockWidget("Tools", self.createToolBar()))

        # 添加底部选项卡和日志
        self.addDockWidget(Qt.BottomDockWidgetArea, self.createDockWidget("Tabs & Logs", self.createTabs()))

        # 添加右侧信息面板
        self.addDockWidget(Qt.RightDockWidgetArea, self.createDockWidget("Info Panel", self.createInfoPanel()))

    def createToolBar(self):
        # 创建工具栏内容
        layout = QVBoxLayout()
        layout.addWidget(QPushButton("Button 1"))
        layout.addWidget(QPushButton("Button 2"))
        layout.addWidget(QPushButton("Button 3"))
        # 添加更多按钮...

        toolBarWidget = QWidget()
        toolBarWidget.setLayout(layout)
        return toolBarWidget

    def createTabs(self):
        # 创建选项卡
        tabs = QTabWidget()
        tabs.addTab(QListWidget(), "Tab 1")
        tabs.addTab(QListWidget(), "Tab 2")
        # 添加更多选项卡...
        return tabs

    def createInfoPanel(self):
        # 创建信息面板
        listWidget = QListWidget()
        listWidget.addItems(["Item 1", "Item 2", "Item 3"])
        # 添加更多信息...
        return listWidget

    def createDockWidget(self, title, widget):
        # 创建通用的 DockWidget
        dockWidget = QDockWidget(title)
        dockWidget.setWidget(widget)
        return dockWidget


app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
