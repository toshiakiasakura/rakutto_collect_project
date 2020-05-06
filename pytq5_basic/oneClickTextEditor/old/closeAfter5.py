# coding: utf-8

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = QWidget()
    window.show()
    # 5秒後に window.close を呼び出す
    QTimer.singleShot(5000, window.close)
    sys.exit(app.exec_())
