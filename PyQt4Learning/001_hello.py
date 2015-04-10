import sys
from PyQt4 import QtGui, QtCore
class demowind(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setWindowTitle('Demo Window')
        self.setGeometry(300,300,200,200)
        quit=QtGui.QPushButton('Close',self)
        quit.setGeometry(10,10,70,40)
        self.connect(quit,QtCore.SIGNAL('clicked()'),QtGui.qApp,QtCore.SLOT('quit()'))

app = QtGui.QApplication(sys.argv)
dw = demowind()
dw.show()
sys.exit(app.exec_())
