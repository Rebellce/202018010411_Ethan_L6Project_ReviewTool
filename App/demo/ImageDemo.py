from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenuBar, QToolBar,
                             QAction, QDockWidget, QLabel, QColorDialog, QStatusBar)
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint


class ImageEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('canvas demo')
        self.setGeometry(300, 300, 800, 600)

        # 中央画布
        self.canvas = QImage(self.size(), QImage.Format_ARGB32)
        self.canvas.fill(Qt.white)
        self.drawing = False
        self.brushSize = 2
        self.brushColor = Qt.black
        self.lastPoint = QPoint()

        # 菜单栏
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('文件')
        editMenu = menubar.addMenu('编辑')

        # 工具栏
        toolbar = QToolBar(self)
        self.addToolBar(Qt.LeftToolBarArea, toolbar)
        toolbar.addAction('画笔', self.selectBrush)
        toolbar.addAction('橡皮擦', self.selectEraser)

        # 图层面板
        layersDock = QDockWidget("图层", self)
        self.addDockWidget(Qt.RightDockWidgetArea, layersDock)

        # 属性/设置面板
        settingsDock = QDockWidget("属性", self)
        self.addDockWidget(Qt.RightDockWidgetArea, settingsDock)

        # 状态栏
        statusbar = self.statusBar()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.canvas)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.canvas, self.canvas.rect())

    def selectBrush(self):
        self.brushColor = QColorDialog.getColor()

    def selectEraser(self):
        self.brushColor = Qt.white


if __name__ == '__main__':
    app = QApplication([])
    editor = ImageEditor()
    editor.show()
    app.exec()
