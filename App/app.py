from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import sys
# import os

from ui.ui import ImageCropper
# ui_path = os.path.join(os.path.dirname(__file__), 'ui')
# if ui_path not in sys.path:
#     sys.path.insert(0, ui_path)


if __name__ == "__main__":
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    # QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    app.setStyleSheet(open("ui/style.qss", "r").read())
    win = ImageCropper()
    win.show()
    sys.exit(app.exec_())
