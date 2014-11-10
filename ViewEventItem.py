#!/usr/bin/python
#coding=utf8

import ui.ui_dataShow as ui_dataShow
from DB import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from EventItemController import loadData

class EventShowWidget( QWidget ):
    def __init__( self ):
        QWidget.__init__( self )
        self.setupUi()
        self.itemsperpage = 5
        self.page = 1
        self.createConnections()

    def keyPressEvent(self, evt):
        if evt.key() == Qt.Key_Escape:
            evt.accept()
            self.hide()
        super(EventShowWidget, self).keyPressEvent(evt)

    def createConnections(self):
        self.connect(self.ui.btnPrevPage, SIGNAL('clicked()'), self.loadPrevPage)
        self.connect(self.ui.btnNextPage, SIGNAL('clicked()'), self.loadNextPage)

    @pyqtSlot()
    def loadNextPage(self):
        self.page += 1
        #self.ui.tableShowWidget = QTableWidget( self )
        data = getEventByPage(self.page, self.itemsperpage)
        loadData(self, data)

    @pyqtSlot()
    def loadPrevPage(self):
        if 1 == self.page:
            return
        else:
            self.page -= 1
            data = getEventByPage(self.page, self.itemsperpage)
            #self.ui.tableShowWidget = QTableWidget( self )
            loadData(self, data)

    def setupUi( self ):
        self.ui = ui_dataShow.Ui_Form()
        self.ui.setupUi( self )
        #setup the contentShowWidget
        vLayout = QVBoxLayout()
        self.ui.tableShowWidget = QTableWidget( self )
        vLayout.addWidget( self.ui.tableShowWidget )
        self.ui.contentShowWidget.setLayout( vLayout )
        self.resize(700, 350)

if '__main__' == __name__:
    import sys
    app = QApplication( sys.argv )
    w = EventShowWidget()
    w.show()
    sys.exit( app.exec_() )
