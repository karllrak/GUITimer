#!/usr/bin/python
#coding=utf8

import ui.ui_dataShow as ui_dataShow
from PyQt4.QtGui import *

class EventShowWidget( QWidget ):
    def __init__( self ):
        QWidget.__init__( self )
        self.setupUi()
    def setupUi( self ):
        self.ui = ui_dataShow.Ui_Form()
        self.ui.setupUi( self )
        #setup the contentShowWidget
        vLayout = QVBoxLayout()
        self.ui.tableShowWidget = QTableWidget( self )
        vLayout.addWidget( self.ui.tableShowWidget )
        self.ui.contentShowWidget.setLayout( vLayout )

if '__main__' == __name__:
    import sys
    app = QApplication( sys.argv )
    w = EventShowWidget()
    w.show()
    sys.exit( app.exec_() )
