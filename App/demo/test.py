from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QDialog, QDesktopWidget
from PyQt5.QtCore import Qt, QPoint, QTimer


class FloatingWidget(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Tool | Qt.FramelessWindowHint)
        self.setFixedSize(100, 100)  # 设置控件大小为100x100像素
        self.setStyleSheet("background-color: blue;")  # 设置控件的背景颜色


class HoverLabel(QLabel):
    def __init__(self, text, floatingWidget, parent=None):
        super().__init__(text, parent)
        self.floatingWidget = floatingWidget
        self.setMouseTracking(True)
        self.timer = QTimer(self)
        self.timer.setInterval(600)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.decideFloatingWidgetPosition)

    def enterEvent(self, event):
        self.timer.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.timer.stop()
        self.floatingWidget.hide()
        super().leaveEvent(event)

    def decideFloatingWidgetPosition(self):
        mainWindowPos = self.window().pos()  # 获取主窗口的位置
        globalPos = QCursor.pos()  # 获取鼠标的全局位置
        localPos = globalPos - mainWindowPos  # 将鼠标位置转换为相对于主窗口的局部位置
        windowHeight = self.window().height()  # 获取窗口的高度
        offsetX, offsetY = 20, 20

        # 根据鼠标相对于窗口的位置决定悬浮窗口显示在鼠标的上方还是下方
        if localPos.y() < (windowHeight / 2):  # 鼠标在窗口上半部
            offsetY = 20  # 在鼠标下方显示
        else:  # 鼠标在窗口下半部
            offsetY = -20 - self.floatingWidget.height()  # 在鼠标上方显示

        self.floatingWidget.move(globalPos + QPoint(offsetX, offsetY))
        self.floatingWidget.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hover Example')
        self.setGeometry(100, 100, 400, 300)
        self.initUI()

    def initUI(self):
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout(centralWidget)

        # 创建鼠标悬停时显示的独立控件
        floatingWidget = FloatingWidget(self)

        paragraphs = ['第一个段落', '第二个段落', '第三个段落']
        for para in paragraphs:
            label = HoverLabel(para, floatingWidget, self)
            layout.addWidget(label)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
