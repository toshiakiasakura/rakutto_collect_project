# coding : utf-8

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sip

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # 一つ目のチェックボックス
        self.upper = QCheckBox('大文字', self)
        self.upper.move(100, 30)

        # 二つ目のチェックボックス
        self.lower = QCheckBox('小文字', self)
        self.lower.move(180, 30)

        # grouping, the advantage of grouping is restict check in only one checkbox
        # within a check box group 
        self.group = QButtonGroup()
        self.group.addButton(self.upper,1)
        self.group.addButton(self.lower,2)
        
        # setting window 
        self.setGeometry(300, 50, 400, 350)
        self.setWindowTitle('QCheckBox')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
