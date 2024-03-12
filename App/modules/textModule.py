from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2
import qimage2ndarray


def text(self):
    if self.image is not None:
        self.view.activate = True
        self.view.textFlag = True
        self.text = QTextEdit()
        self.editToolBarH.clear()
        self.painter = QPainter(self.pixmap)
        self.painter.begin(self.pixmap)
        fontbox = QFontComboBox(self)
        fontbox.currentFontChanged.connect(lambda font: self.text.setCurrentFont(font))
        fontSize = QSpinBox(self)
        fontSize.setSuffix(" pt")
        fontSize.valueChanged.connect(lambda size: self.text.setFontPointSize(size))
        fontSize.setValue(14)
        fontColor = QAction(QIcon("../icons/font-color.png"), "Change font color", self)
        fontColor.triggered.connect(self.fontColorChanged)
        backColor = QAction(QIcon("../icons/highlight.png"), "Change background color", self)
        backColor.triggered.connect(self.highlight)
        boldAction = QAction(QIcon("../icons/bold.png"), "Bold", self)
        boldAction.triggered.connect(self.bold)
        italicAction = QAction(QIcon("../icons/italic.png"), "Italic", self)
        italicAction.triggered.connect(self.italic)
        underlAction = QAction(QIcon("../icons/underline.png"), "Underline", self)
        underlAction.triggered.connect(self.underline)
        strikeAction = QAction(QIcon("../icons/strike.png"), "Strike-out", self)
        strikeAction.triggered.connect(self.strike)
        alignLeft = QAction(QIcon("../icons/align-left.png"), "Align left", self)
        alignLeft.triggered.connect(self.alignLeft)
        alignCenter = QAction(QIcon("../icons/align-center.png"), "Align center", self)
        alignCenter.triggered.connect(self.alignCenter)
        alignRight = QAction(QIcon("../icons/align-right.png"), "Align right", self)
        alignRight.triggered.connect(self.alignRight)
        alignJustify = QAction(QIcon("../icons/align-justify.png"), "Align justify", self)
        alignJustify.triggered.connect(self.alignJustify)
        self.editToolBarH.addWidget(fontbox)
        self.editToolBarH.addWidget(fontSize)
        self.editToolBarH.addSeparator()
        self.editToolBarH.addAction(fontColor)
        self.editToolBarH.addAction(backColor)
        self.editToolBarH.addSeparator()
        self.editToolBarH.addAction(boldAction)
        self.editToolBarH.addAction(italicAction)
        self.editToolBarH.addAction(underlAction)
        self.editToolBarH.addAction(strikeAction)
        self.editToolBarH.addSeparator()
        self.editToolBarH.addAction(alignLeft)
        self.editToolBarH.addAction(alignCenter)
        self.editToolBarH.addAction(alignRight)
        self.editToolBarH.addAction(alignJustify)
        button_action_text = QAction(self)
        button_action_text.setIcon(QIcon('../icons/check.png'))
        button_action_text.triggered.connect(self.buttonClickToSetText)
        self.button_action_text_Pm = QAction(self)
        self.editToolBarH.addAction(button_action_text)


def buttonClickToSetText(self):
    self.crop_start, self.crop_end = self.view.getResult()
    try:
        self.text.deleteLater()
        self.button_action_text_Pm.deleteLater()
    except Exception as e:
        print(e)
    if self.crop_start is not None and self.crop_end is not None:
        x, y, x1, y1 = self.view.mapToScene(self.crop_start).x(), self.view.mapToScene(
            self.crop_start).y(), self.view.mapToScene(self.crop_end).x(), self.view.mapToScene(self.crop_end).y()
        x = 0 if x < 0 else x
        y = 0 if y < 0 else y
        x1 = self.pixmap.width() if x1 > self.pixmap.width() else x1
        y1 = self.pixmap.height() if y1 > self.pixmap.height() else y1
        self.x = x
        self.y = y
        self.x1 = x1
        self.y1 = y1
        self.text = QTextEdit()
        self.text.setFixedSize(self.x1 - self.x, self.y1 - self.y)
        self.text.move(self.x, self.y)
        self.view.crop_rect = None
        self.scene.addWidget(self.text)
        self.button_action_text_Pm = QAction("OK", self)
        self.button_action_text_Pm.triggered.connect(self.buttonClickToSetTextPixmap)
        self.editToolBarH.addAction(self.button_action_text_Pm)


def buttonClickToSetTextPixmap(self):
    self.text.deleteLater()
    self.button_action_text_Pm.deleteLater()
    if self.text.isVisible():
        self.crop_start = None
        self.crop_end = None
        text = self.text.toPlainText().split("\n")
        self.pen = QPen(self.text.currentCharFormat().foreground().color())
        cursor = self.text.textCursor()
        cursor.movePosition(QTextCursor.Start)
        cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
        format = cursor.charFormat()
        self.font = self.text.currentFont()
        if format.fontItalic():
            self.font.setItalic(True)
        if format.fontUnderline():
            self.font.setUnderline(True)
        if format.fontStrikeOut():
            self.font.setStrikeOut(True)
        self.painter.setFont(self.font)
        self.painter.setPen(self.pen)
        x = self.x
        y = self.y
        try:
            for i in range(len(text)):
                x = self.x + i * self.font.pointSize() + 10
                y = self.y + i * self.font.pointSize() + 30
                self.painter.drawText(x, y, text[i])
        except:
            self.x = 10
            self.y = 10
            for i in range(len(text)):
                x = self.x + i * self.font.pointSize() + 10
                y = self.y + i * self.font.pointSize()
                self.painter.drawText(x, y, text[i])
        self.scene.clear()
        self.scene.addPixmap(self.pixmap)
        self.scene.update()


def converPixmapToCV(pixmap):
    image_data = qimage2ndarray.rgb_view(pixmap.toImage())
    image_data = cv2.cvtColor(image_data, cv2.COLOR_RGB2BGR)
    return image_data


def fontColorChanged(self):
    color = QColorDialog.getColor()
    self.text.setTextColor(color)


def highlight(self):
    color = QColorDialog.getColor()
    self.text.setTextBackgroundColor(color)


def bold(self):
    if self.text.fontWeight() == QFont.Bold:
        self.text.setFontWeight(QFont.Normal)
    else:
        self.text.setFontWeight(QFont.Bold)


def italic(self):
    state = self.text.fontItalic()
    self.text.setFontItalic(not state)


def underline(self):
    state = self.text.fontUnderline()
    self.text.setFontUnderline(not state)


def strike(self):
    fmt = self.text.currentCharFormat()
    fmt.setFontStrikeOut(not fmt.fontStrikeOut())
    self.text.setCurrentCharFormat(fmt)


def alignLeft(self):
    self.text.setAlignment(Qt.AlignLeft)


def alignRight(self):
    self.text.setAlignment(Qt.AlignRight)


def alignCenter(self):
    self.text.setAlignment(Qt.AlignCenter)


def alignJustify(self):
    self.text.setAlignment(Qt.AlignJustify)
