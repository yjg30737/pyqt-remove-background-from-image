import os

from PyQt5.QtWidgets import QWidget, QListWidget, QApplication, QSplitter, QVBoxLayout, QLabel

from imageView import ImageView


class ListViewerWidget(QWidget):
    def __init__(self):
        super(ListViewerWidget, self).__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__dirname = ''

    def __initUi(self):
        self.__listWidget = QListWidget()
        self.__listWidget.itemDoubleClicked.connect(self.__setCurrentImage)
        self.__listWidget.itemActivated.connect(self.__setCurrentImage)
        self.__imageView = ImageView()

        lay = QVBoxLayout()
        lay.addWidget(QLabel('Files'))
        lay.addWidget(self.__listWidget)
        lay.setContentsMargins(0, 0, 0, 0)

        leftWidget = QWidget()
        leftWidget.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(QLabel('Image Preview'))
        lay.addWidget(self.__imageView)
        lay.setContentsMargins(0, 0, 0, 0)

        rightWidget = QWidget()
        rightWidget.setLayout(lay)

        splitter = QSplitter()
        splitter.addWidget(leftWidget)
        splitter.addWidget(rightWidget)
        splitter.setSizes([300, 700])
        splitter.setChildrenCollapsible(False)

        lay = QVBoxLayout()
        lay.addWidget(splitter)
        lay.setContentsMargins(0, 0, 0, 0)

        self.setLayout(lay)

    def __setCurrentImage(self, item):
        filename = os.path.join(self.__dirname, item.text())
        self.__imageView.setFilename(filename)

    def setCurrentDir(self, dirname):
        self.__dirname = dirname

    def getCurrentDir(self):
        return self.__dirname

    def addFiles(self, filenames):
        self.__listWidget.clear()
        self.__listWidget.addItems(filenames)

    def getFilenames(self):
        return [os.path.join(self.__dirname, self.__listWidget.item(i).text()) for i in range(self.__listWidget.count())]


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = ListViewerWidget()
    w.show()
    sys.exit(app.exec())