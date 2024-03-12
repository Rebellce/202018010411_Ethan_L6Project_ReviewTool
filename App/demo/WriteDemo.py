import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QColorDialog, QToolBar, QFontComboBox, \
    QSpinBox
from PyQt5.QtGui import QIcon, QColor, QFont
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        # Rich text actions
        bold_action = QAction(QIcon(), 'Bold', self)
        bold_action.triggered.connect(self.set_bold)
        bold_action.setCheckable(True)

        italic_action = QAction(QIcon(), 'Italic', self)
        italic_action.triggered.connect(self.set_italic)
        italic_action.setCheckable(True)

        underline_action = QAction(QIcon(), 'Underline', self)
        underline_action.triggered.connect(self.set_underline)
        underline_action.setCheckable(True)

        color_action = QAction(QIcon(), 'Color', self)
        color_action.triggered.connect(self.set_color)

        font_box = QFontComboBox()
        font_box.currentFontChanged.connect(self.set_font)

        font_size_box = QSpinBox()
        font_size_box.setValue(12)
        font_size_box.valueChanged.connect(self.set_font_size)

        # Toolbar
        # Toolbar
        self.toolbar = QToolBar("Rich Text")
        self.toolbar.setFloatable(True)
        self.toolbar.setMovable(True)

        # Adjust the size policy and preferred size of the font box
        font_box = QFontComboBox()
        font_box.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        font_box.setMaximumWidth(200)  # Adjust the maximum width as needed
        font_box.currentFontChanged.connect(self.set_font)

        # Adjust the size policy and preferred size of the font size box
        font_size_box = QSpinBox()
        font_size_box.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        font_size_box.setMaximumWidth(60)  # Adjust the maximum width as needed
        font_size_box.setRange(1, 100)  # Set a sensible range for font sizes
        font_size_box.setValue(12)
        font_size_box.valueChanged.connect(self.set_font_size)

        self.toolbar.addWidget(font_box)
        self.toolbar.addWidget(font_size_box)
        self.toolbar.addAction(bold_action)
        self.toolbar.addAction(italic_action)
        self.toolbar.addAction(underline_action)
        self.toolbar.addAction(color_action)
        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)
        self.toolbar.setIconSize(QtCore.QSize(16, 16))  # Adjust icon size if you are using icons
        self.toolbar.setFixedWidth(240)  # Set a fixed width based on your preference

        self.setWindowTitle("Rich Text Editor")
        self.setGeometry(300, 300, 600, 400)

    def set_bold(self):
        if self.text_edit.fontWeight() != QFont.Bold:
            self.text_edit.setFontWeight(QFont.Bold)
        else:
            self.text_edit.setFontWeight(QFont.Normal)

    def set_italic(self):
        state = self.text_edit.fontItalic()
        self.text_edit.setFontItalic(not state)

    def set_underline(self):
        state = self.text_edit.fontUnderline()
        self.text_edit.setFontUnderline(not state)

    def set_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_edit.setTextColor(color)

    def set_font(self, font):
        self.text_edit.setCurrentFont(font)

    def set_font_size(self, size):
        self.text_edit.setFontPointSize(size)


def main():
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
