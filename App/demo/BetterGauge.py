from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QPen, QFont
from PyQt5.QtCore import QRect, QPoint, Qt, QLine, QRectF
import math


class CMPassrate5(QWidget):
    def __init__(self):
        super().__init__()
        self.radius = 100
        self.side = 10
        self.outRange = 60
        self.range = 120
        self.lineCount = 8
        self.lineLength = 10
        self.textCount = 10
        self.value = 50
        self.color = QColor(0, 255, 0)

    def paintEvent(self, event):
        width = self.width()
        height = self.height()
        side = min(width, height)

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        painter.translate(width / 2, height / 2)
        painter.scale(side / 200.0, side / 200.0)

        self.drawE(painter)
        self.drawEPoint(painter)
        self.drawLine(painter)
        self.drawEText(painter)
        self.drawValue(painter)

    def drawE(self, painter):
        rect = QRect(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)
        rectF = QRectF(rect)
        painter.save()
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        subPath = QPainterPath()
        outPath = QPainterPath()
        outPubPath = QPainterPath()
        outPath.arcTo(rectF, -45, self.outRange)
        outPubPath.addEllipse(rectF.adjusted(self.side, self.side, -self.side, -self.side))
        outPath -= outPubPath
        self.color.setAlpha(100)
        painter.setBrush(self.color)
        painter.drawPath(outPath)

        path.arcTo(rectF, -45 + self.outRange, self.range)
        subPath.addEllipse(rectF.adjusted(4, 4, -4, -4))
        path -= subPath
        self.color.setAlpha(180)
        painter.setBrush(self.color)
        painter.drawPath(path)

        painter.restore()

    def drawEPoint(self, painter):
        painter.save()
        self.color.setAlpha(180)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color)

        x = (self.radius - self.side / 2) * math.cos(math.radians(self.range + 135))
        y = (self.radius - self.side / 2) * math.sin(math.radians(self.range + 135))
        painter.drawEllipse(QPoint(x, y), self.side, self.side)
        painter.restore()

    def drawLine(self, painter):
        painter.save()
        painter.rotate(135)
        self.color.setAlpha(100)
        painter.setPen(self.color)
        line = QLine(QPoint(self.radius - self.side - self.lineLength, 0), QPoint(self.radius - self.side, 0))

        for i in range(self.lineCount):
            painter.drawLine(line)
            painter.rotate(270.0 / self.lineCount)
        painter.restore()

    def drawEText(self, painter):
        painter.save()
        painter.setPen(Qt.black)
        textRange = 270.0 / (self.textCount - 1)

        for i in range(self.textCount + 1):
            x = (self.radius - self.side - self.lineLength) * math.cos(math.radians(textRange * i + 135))
            y = (self.radius - self.side - self.lineLength) * math.sin(math.radians(textRange * i + 135))
            text = str(i * 10)
            if i < 5:
                rectF = QRectF(QRect(x, y - 4, 20, 10))
            elif i == 5:
                rectF = QRectF(QRect(x - 7, y, 20, 10))
            else:
                rectF = QRectF(QRect(x - 20, y - 5, 20, 10))
            painter.drawText(rectF, Qt.AlignCenter, text)

        painter.restore()

    def drawValue(self, painter):
        painter.save()
        pen = QPen(self.color)
        pen.setWidth(2)
        painter.setPen(pen)
        font = QFont()
        font.setPixelSize(45)
        painter.setFont(font)

        rectF = QRect(-25, -25, 50, 50)
        painter.drawText(rectF, Qt.AlignCenter, str(self.value))
        painter.restore()


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建自定义控件的实例
        self.gauge = CMPassrate5()

        # 可以设置控件的属性，例如值
        self.gauge.value = 50  # 设置仪表盘的值

        # 设置窗口的中央控件为自定义控件
        self.setCentralWidget(self.gauge)

        # 设置窗口的其他属性
        self.setWindowTitle('Custom Gauge Example')
        self.setGeometry(300, 300, 400, 400)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
