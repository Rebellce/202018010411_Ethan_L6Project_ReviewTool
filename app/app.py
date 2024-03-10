from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import os

from ui.ui import ImageCropper
ui_path = os.path.join(os.path.dirname(__file__), 'ui')
if ui_path not in sys.path:
    sys.path.insert(0, ui_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ImageCropper()
    win.show()
    sys.exit(app.exec_())
