# coding : utf-8 

######## GUI platform in python #########
#usually GUI is written in compiled programming language,
#so that great disadvantage of GUI with python is heavey to run.

#GUI in python platform are such as, PyQt5 (main stream), Tkinter etc...  

####### PyQt5 ########
### PyQt is cross format application, it works independent of OS. 

###### references 
## PyQt5 tutorial 
# http://zetcode.com/gui/pyqt5/
## python入門　PyQt5を使ってGUIを作ろう
# https://www.sejuku.net/blog/75467




####installation :
#pip install SIP ( for use c++ program in python )
#pip install PyQt5
#( if ptython3 is not default, use pip3 instead of pip3. )


import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sip
 
class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
            
        # position of window, (upper left x,y ,) 
        self.setGeometry(300, 100, 400, 300)
        self.setWindowTitle('QCheckBox')
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
