from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView


class ImageView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.__aspectRatioMode = Qt.KeepAspectRatio
        self.__gradient_enabled = False
        self.__initVal()

    def __initVal(self):
        self._scene = QGraphicsScene()
        self._p = QPixmap()
        self._item = ''

    def setFilename(self, filename: str):
        self._p = QPixmap(filename)
        self._scene = QGraphicsScene()
        self._item = self._scene.addPixmap(self._p)
        self._item.setTransformationMode(Qt.SmoothTransformation)

        self.setScene(self._scene)
        self.fitInView(self._item, self.__aspectRatioMode)

    def setAspectRatioMode(self, mode):
        self.__aspectRatioMode = mode

    def resizeEvent(self, e):
        if self._item:
            self.fitInView(self.sceneRect(), self.__aspectRatioMode)
        return super().resizeEvent(e)