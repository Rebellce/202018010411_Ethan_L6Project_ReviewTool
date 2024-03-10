def zoomIn(self):
    self.editToolBarH.clear()
    self.view.activate = False
    self.view.crop_rect = None
    self.scale = 1.01
    self.actionZoom()


def zoomOut(self):
    self.editToolBarH.clear()
    self.view.activate = False
    self.view.crop_rect = None
    self.scale *= 0.99
    self.actionZoom()


def actionZoom(self):
    if self.image is not None:
        self.view.scale(self.scale, self.scale)
