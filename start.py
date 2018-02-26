import sys
from PyQt4 import QtGui
from frm_mainwindow import Frm_MainWindow

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main_frm = Frm_MainWindow()
    main_frm.show()
    sys_exit = sys.exit(app.exec_())
    