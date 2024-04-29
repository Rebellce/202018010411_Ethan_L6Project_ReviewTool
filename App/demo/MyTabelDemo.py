from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QColor


class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    _counter = 0

    def __init__(self, text, bgColor="lightgray", parent=None):
        super().__init__(text, parent)
        type(self)._counter += 1
        self.id = self._counter
        self.backgroundColor = bgColor
        self.setWordWrap(True)
        self.deselectStyle()
        self.setAlignment(Qt.AlignCenter)
        # self.setMinimumHeight(20)

    def selectStyle(self):
        self.setStyleSheet(f"background-color: #E5E5E5; border-radius: 5px; padding: 4px; border: 2px solid lightgray;")

    def deselectStyle(self):
        self.setStyleSheet(
            f"background-color: {self.backgroundColor}; border-radius: 5px; padding: 4px; border-bottom: 2px solid #AED6F1;")

    def mousePressEvent(self, event):
        self.clicked.emit()


class MyClickableRow(QWidget):
    rowSelected = pyqtSignal(int)
    _counter = 0

    def __init__(self, parent=None, *args, color=0):
        super().__init__(parent)
        type(self)._counter += 1
        self.id = self._counter
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.setContentsMargins(0, 0, 0, 0)


        self.selected = False
        self.allLabels = []
        if color == 0:
            self.labelColor = "#D6EAF8"
        elif color == 1:
            self.labelColor = "#D4EFDF"
        elif color == 2:
            self.labelColor = "#FCF3CF"
        for i in range(4):
            label = ClickableLabel(args[i], bgColor=self.labelColor)
            if i == 0:
                label.setFixedSize(25, 25)
            elif i == 2:
                label.setFixedWidth(100)
            elif i == 3:
                label.setFixedWidth(50)
            label.clicked.connect(self.labelClicked)
            self.layout.addWidget(label)
            self.allLabels.append(label)

    def selectRow(self):
        for label in self.allLabels:
            label.selectStyle()
        self.selected = True

    def deselectRow(self):
        for label in self.allLabels:
            label.deselectStyle()
        self.selected = False

    def labelClicked(self):
        if self.selected:
            self.rowSelected.emit(-1)
        else:
            self.rowSelected.emit(self.id)


class MyTabelWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.rows = {}
        self.selectedRowIndex = -1  # -1 means no row is selected
        self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addSpacerItem(self.spacer)
        self.setContentsMargins(0, 0, 0, 0)

    def insertRow(self, *args, color=0, top=False):
        row = MyClickableRow(self, *args, color=color)
        row.rowSelected.connect(self.updateSelectedRow)
        if top:
            self.layout.insertWidget(0, row)
        else:
            self.layout.insertWidget(self.layout.count() - 1, row)
        self.rows[row.id] = row

    def removeRow(self):
        if self.selectedRowIndex != -1:
            row = self.rows.pop(self.selectedRowIndex)
            self.layout.removeWidget(row)
            row.deleteLater()
            self.selectedRowIndex = -1

    def moveRowToTop(self):
        if self.selectedRowIndex != -1:
            row = self.rows[self.selectedRowIndex]
            self.layout.removeWidget(row)
            self.layout.insertWidget(0, row)

    def updateSelectedRow(self, rowId):
        if rowId == -1:
            if self.selectedRowIndex != -1:
                self.rows[self.selectedRowIndex].deselectRow()
        else:
            if self.selectedRowIndex != -1:
                self.rows[self.selectedRowIndex].deselectRow()
            self.rows[rowId].selectRow()
        self.selectedRowIndex = rowId


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow


    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.initUI()

        def initUI(self):
            layout = QVBoxLayout()
            widget = QWidget()
            widget.setLayout(layout)
            self.setCentralWidget(widget)
            buttonLayout = QHBoxLayout()
            self.tableWidget = MyTabelWidget(self)
            addButton = QPushButton("Add Row", self)
            addButton.clicked.connect(self.addRow)
            removeButton = QPushButton("Remove Row", self)
            removeButton.clicked.connect(self.removeRow)
            moveButton = QPushButton("To Top", self)
            moveButton.clicked.connect(self.moveRowToTop)

            buttonLayout.addWidget(addButton)
            buttonLayout.addWidget(removeButton)
            buttonLayout.addWidget(moveButton)

            buttonWidget = QWidget()
            buttonWidget.setLayout(buttonLayout)
            layout.addWidget(buttonWidget)
            layout.addWidget(self.tableWidget)

            self.tableWidget.insertRow("🔍", "John Doe", "2021-04-01 00:00:00", "OCR", color=0)
            self.tableWidget.insertRow("📊", "Jane Smith", "2021-04-01 00:00:00", "Ai", color=1)
            self.tableWidget.insertRow("🖼️", "Emily Johnson", "2021-04-01 00:00:00", "File", color=2)

            self.setWindowTitle('PyQt Custom Table Test')
            self.resize(400, 300)

        def addRow(self):
            self.tableWidget.insertRow("🎶", "John Doe", "2021-04-01 00:00:00", "OCR", color=0, top=True)

        def removeRow(self):
            self.tableWidget.removeRow()

        def moveRowToTop(self):
            self.tableWidget.moveRowToTop()


    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
