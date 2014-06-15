#!/usr/bin/python
#coding=utf8

import DB
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ViewEventItem import EventShowWidget

if '__main__' == __name__:
    import sys
    app = QApplication( sys.argv )
    dataCount = 20
    data = DB.getLatestEvent( dataCount )
    w = EventShowWidget()
    t = w.ui.tableShowWidget
    for i in range( 5 ):
	w.ui.tableShowWidget.insertColumn( 0 )
    w.ui.tableShowWidget.setColumnWidth( 0, int( 1.5 * t.columnWidth( 0 ) ) )
    for i in range( len(data) ):
	w.ui.tableShowWidget.insertRow( i )
    #load the data to table
	for j in range( 5 ):
	    d = data[i][j]
	    if 0 == d:
		d = u''
	    elif 1 == d:
		d = u'是'
	    w.ui.tableShowWidget.setItem( i, j, 
		    QTableWidgetItem( d ) )
	
    w.ui.tableShowWidget.setHorizontalHeaderLabels(
	    [u'描述',
		'startTime',
		'endTime',
		u'已完成',
		u'超时']
	    )

    w.show()
    sys.exit( app.exec_() )
