from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QTextEdit, QListWidget
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置主窗口的中心控件
        self.setCentralWidget(QTextEdit())

        # 创建并添加第一个停靠窗口
        self.addDockWidget(Qt.RightDockWidgetArea, self.createDockWidget("Dock 1"))

        # 创建并添加第二个停靠窗口
        self.addDockWidget(Qt.RightDockWidgetArea, self.createDockWidget("Dock 2"))

        self.setWindowTitle("Dockable")
        self.setGeometry(300, 300, 400, 300)

    def createDockWidget(self, title):
        dock = QDockWidget(title, self)
        dock.setAllowedAreas(Qt.AllDockWidgetAreas)
        listWidget = QListWidget(dock)
        listWidget.addItems([f"Item {i}" for i in range(10)])
        dock.setWidget(listWidget)
        return dock


app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
