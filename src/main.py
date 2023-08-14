import os, sys, shutil

from PyQt5.QtGui import QFont

from script import remove_background_from_image, open_directory

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well

from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QFrame, QSizePolicy, QHBoxLayout, \
    QPushButton, QMessageBox
from PyQt5.QtCore import QThread, QCoreApplication
from PyQt5.QtCore import Qt

from findPathWidget import FindPathWidget
from listViewer import ListViewerWidget

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # HighDPI support

QApplication.setFont(QFont('Arial', 12))


class Thread(QThread):
    def __init__(self, filenames):
        super(Thread, self).__init__()
        self.__filenames = filenames

    def run(self):
        try:
            for filename in self.__filenames:
                remove_background_from_image(filename)
        except Exception as e:
            raise Exception(e)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle('Remove background from image!')
        self.__findPathWidget = FindPathWidget()
        self.__findPathWidget.getLineEdit().setPlaceholderText('Set the directory of images...')
        self.__findPathWidget.setAsDirectory(True)
        self.__findPathWidget.added.connect(self.__added)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)

        self.__listViewerWidget = ListViewerWidget()
        self.__listViewerWidget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        self.__runBtn = QPushButton('Remove Background and Save!')
        self.__runBtn.clicked.connect(self.__run)

        lay = QVBoxLayout()
        lay.addWidget(self.__findPathWidget)
        lay.addWidget(sep)
        lay.addWidget(self.__listViewerWidget)
        lay.addWidget(self.__runBtn)
        lay.setAlignment(Qt.AlignTop)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setCentralWidget(mainWidget)

    def __added(self, dirname):
        self.__listViewerWidget.setCurrentDir(dirname)
        self.__listViewerWidget.addFiles(os.listdir(dirname))

    def __run(self):
        filenames = self.__listViewerWidget.getFilenames()

        # backup
        backup_dirname = '../backup'
        os.makedirs(backup_dirname, exist_ok=True)
        for filename in filenames:
            shutil.copy(filename, os.path.join(backup_dirname, os.path.basename(filename)))

        self.__t = Thread(filenames)
        self.__t.started.connect(self.__started)
        self.__t.finished.connect(self.__finished)
        self.__t.start()

    def __started(self):
        print('started')
        self.__runBtn.setEnabled(False)

    def __finished(self):
        print('finished')
        open_directory(self.__listViewerWidget.getCurrentDir())
        self.__runBtn.setEnabled(True)
        QMessageBox.information(self, 'Finished', 'Enjoy')


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())