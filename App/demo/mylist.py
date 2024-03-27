from PyQt5.QtWidgets import QLabel, QWidget, QApplication, QVBoxLayout, QMainWindow, QScrollArea
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPalette, QColor
from App.ui.myGauge import myGaugeWidget


class SquareWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(100, 100)  # 设置控件大小为100x100像素
        self.setStyleSheet("background-color: blue;")  # 设置控件的背景颜色
        self.hide()  # 初始时隐藏控件


# 假设其它部分的定义与之前相同

class HoverLabel(QLabel):
    def __init__(self, text, hoverWidget, parent=None):
        super().__init__(text, parent)
        self.hoverWidget = hoverWidget
        self.setMouseTracking(True)
        # 设置一个背景颜色以便我们可以看到QLabel的确切位置
        self.setStyleSheet("background-color: lightgrey;")

    def enterEvent(self, event):
        # 计算HoverWidget应当显示的位置
        pos = self.mapToGlobal(QPoint(0, self.height()))  # 将QLabel下方的位置转换为全局坐标
        # 考虑到悬浮控件的大小，调整显示位置，避免直接覆盖在QLabel上
        self.hoverWidget.move(pos + QPoint(200, -100))  # 在QLabel的右下方稍微偏移显示
        self.hoverWidget.show()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hoverWidget.hide()
        super().leaveEvent(event)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hover Example')
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout(centralWidget)

        scrollArea = QScrollArea(self)
        contentWidget = QWidget()
        scrollArea.setWidget(contentWidget)
        scrollArea.setWidgetResizable(True)
        contentLayout = QVBoxLayout(contentWidget)

        # 创建鼠标悬停时显示的控件
        hoverWidget = myGaugeWidget(self)
        hoverWidget.setFixedSize(200, 200)

        paragraphs = ['第一个段落', '第二个段落', '第三个段落']
        for para in paragraphs:
            label = HoverLabel(para, hoverWidget, self)
            contentLayout.addWidget(label)

        layout.addWidget(scrollArea)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
