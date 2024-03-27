from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QDialog, QScrollArea
from PyQt5.QtCore import Qt, QPoint, QTimer
from App.ui.myGauge import myGaugeWidget
from PyQt5.QtWidgets import QApplication


class myLabelList(QWidget):
    def __init__(self, dicList=None, parent=None):
        super().__init__(parent)
        self.contentLayout = None
        self.widgetList = []
        if dicList is None:
            self.dicList = []
        else:
            self.dicList = dicList
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        scrollArea = QScrollArea()

        contentWidget = QWidget()
        contentWidget.setStyleSheet("""
        background-color: white;
        """)
        scrollArea.setWidget(contentWidget)
        scrollArea.setWidgetResizable(True)
        scrollArea.setFrameStyle(QScrollArea.NoFrame)
        self.contentLayout = QVBoxLayout(contentWidget)
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.contentLayout.setSpacing(0)
        layout.addWidget(scrollArea)
        self.setLayout(layout)
        self.loadContent()

    def loadContent(self):
        for dic in self.dicList:
            if dic['type'] == "Human":
                widget = myGaugeWidget(number=dic['prob'], label=dic['lvl'], _type="Human")
            else:
                widget = myGaugeWidget(number=dic['prob'], label=dic['lvl'], _type="GPT")
            hoverWidget = myFloatingWidget(widget=widget)
            label = myHoverLabel(dic['text'], hoverWidget, self,level=dic['lvl'])
            self.contentLayout.addWidget(label)

    def clearContent(self):
        for i in range(self.contentLayout.count()):
            self.contentLayout.itemAt(i).widget().deleteLater()

    def reloadContent(self, dicList):
        self.dicList = dicList
        self.clearContent()
        self.loadContent()


class myFloatingWidget(QDialog):
    def __init__(self, parent=None, widget=None):
        """
        This is a floating widget to show the hover widget
        :param parent:
        :param widget:
        """
        super().__init__(parent, Qt.Tool | Qt.FramelessWindowHint)
        self.hide()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        if widget is None:
            self.setFixedSize(200, 200)
            self.setStyleSheet("background-color: blue;")
        else:
            self.layout.addWidget(widget)
            widget.show()


class myHoverLabel(QLabel):
    def __init__(self, text, floatingWidget, parent=None, level=None):
        super().__init__(text, parent)
        self.setWordWrap(True)
        self.floatingWidget = floatingWidget
        self.setMouseTracking(True)
        self.timer = QTimer(self)
        self.timer.setInterval(600)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.showAtCursor)

        colors = {
            "Highly likely human": "#E8F8F5",
            "Mostly human": "#D1F2EB",
            "Possibly mixed": "#FDEBD0",
            "Mostly GPT": "#FADBD8",
            "Highly likely GPT": "#F5B7B1",
        }
        bgColor = colors.get(level, "#FFFFFF")
        self.setStyleSheet(f"""
            border-radius: 5px;
            padding-left: 5px; padding-right: 5px;
            margin: 3px,3px;
            margin-left: 5px;
            margin-right: 5px;
            background: {bgColor};
        """)

    def enterEvent(self, event):
        self.timer.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.timer.stop()
        self.floatingWidget.hide()
        super().leaveEvent(event)

    def mouseMoveEvent(self, event):
        if self.floatingWidget.isVisible():
            self.updatePosition()
        super().mouseMoveEvent(event)

    def showAtCursor(self):
        self.updatePosition()
        self.floatingWidget.show()

    def updatePosition(self):
        globalPos = QCursor.pos()
        offsetX, offsetY = 20, -200

        windowHeight = QApplication.instance().desktop().screenGeometry().height()
        if (globalPos.y() - self.window().frameGeometry().top()) < (windowHeight / 2):
            offsetY = 20
        else:
            offsetY = -200

        self.floatingWidget.move(globalPos + QPoint(offsetX, offsetY))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    dicList = [
        {'text': 'This is a test1 This is a test1 This is a test1 This is a test1', 'type': 'Human', 'lvl': 'Highly likely human', 'prob': 50},
        {'text': 'This is a test2', 'type': 'GPT', 'lvl': 'Mostly GPT', 'prob': 80},
        {'text': 'This is a test3', 'type': 'Human', 'lvl': 'Possibly mixed', 'prob': 30},
        {'text': 'This is a test4', 'type': 'GPT', 'lvl': 'Mostly human', 'prob': 90},
        {'text': 'This is a test4', 'type': 'GPT', 'lvl': 'Highly likely GPT', 'prob': 90},
    ]
    w = myLabelList(dicList)
    w.show()
    sys.exit(app.exec_())
