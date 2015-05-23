#!/usr/bin/env python3
# -- coding utf-8 --

from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QLabel

class TWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.mLayout = QVBoxLayout()
        self.mLabel = QLabel("Python+Qt的世界是美好的!")
        self.mLayout.addWidget(self.mLabel)
        self.setLayout(self.mLayout)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    win = TWindow()
    win.show()

    sys.exit(app.exec_())

