#!/usr/bin/python
#coding=utf8

import DB
import datetime
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ViewEventItem import EventShowWidget

def dyeRow( widget, rowNo, columnRange, color ):
    for i in range( columnRange[0], columnRange[1] ):
	widget.item( rowNo, i ).setBackground( QBrush(  color ))

def insertDataToRow( widget, data, rowNumber ):
    curDate = datetime.datetime.now()
    startTime = datetime.datetime.strptime( data[1], '%Y-%m-%d %H:%M:%S' )
    delta = startTime - curDate
    isToday = True if -1 == delta.days else False

    for j in range( len(data) ):
	d = data[j]
	if 0 == d:
	    d = u''
	elif 1 == d:
	    d = u'是'
	widget.setItem( rowNumber, j, QTableWidgetItem( d ) )

    if abs( delta.days ) < 60: 
	color = QColor( 255+delta.days*4, 140+delta.days*2, 75-delta.days*3 )#TODO a better way to show time difference using color
	dyeRow( widget=widget, rowNo=rowNumber, columnRange=(0,len(data)), color=color )

if '__main__' == __name__:
    import sys
    app = QApplication( sys.argv )
    dataCount = 20
    #data = DB.getLatestEvent( dataCount )
    data = DB.getEventByPage( 1, 5 )
    w = EventShowWidget()
    t = w.ui.tableShowWidget
    for i in range( 5 ):
	w.ui.tableShowWidget.insertColumn( 0 )
    w.ui.tableShowWidget.setColumnWidth( 0, int( 1.5 * t.columnWidth( 0 ) ) )
    for i in range( len(data) ):
	w.ui.tableShowWidget.insertRow( i )
	#load the data to table
	insertDataToRow( widget=w.ui.tableShowWidget, data=data[i], rowNumber=i )
    
    w.ui.tableShowWidget.setHorizontalHeaderLabels(
	    [u'描述',
		'startTime',
		'endTime',
		u'已完成',
		u'超时']
	    )

    w.show()
    sys.exit( app.exec_() )
