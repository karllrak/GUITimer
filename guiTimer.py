#!/usr/bin/python
#coding=utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_guiTimer import Ui_Form
import qrc_guiTimer_rc
import sys
import time
import datetime
import DB
import pdb


class MainWidget( QWidget ):
    """ the widget """
    def __init__( self ):
	''' the init function '''
	QWidget.__init__( self )
	self.createSystemTray()
	self.createUI()
	self.createConnections()
	self.setWindowTitle( u'定时器' )
	#then the size policy
	self.setSizePolicy( QSizePolicy.Maximum, QSizePolicy.Maximum )
	self.quitWithoutTray = False
	#then the positon/geometry
	self.setGeometry( 400, 400, self.size().width(), self.size().height() )

	self.mission = None
	self.intervalTimer = None
	DB.initTables()

    def closeEvent( self, evt ):
	'''
	override the closeEvent to decide whether use systemTray
	'''
	if self.quitWithoutTray:
	    if None != self.mission:
		self.mission.storeEvent()
	    evt.accept()
	else:
	    self.hide()
	    evt.ignore()

    def showAllShortCut( self ):
	'''
	not implemented
	show all shortcuts set
	'''
	pass

    def keyPressEvent( self, evt ):
	if evt.key() == Qt.Key_Escape or (evt.key() == Qt.Key_W\
		and evt.modifiers() & Qt.ControlModifier ):
	    self.hide()
	    if self.msgLabel.isVisible():
		self.msgLabel.hide()
	elif ( evt.key() == Qt.Key_Q and evt.modifiers()&Qt.ControlModifier ):
	    self.noTrayClose()
	#global shortcut to invoke the app, not implemented
	elif ( evt.key() == Qt.Key_T and evt.modifiers()&Qt.AltModifier ):
	    self.show()
	else:
	    QWidget.keyPressEvent( self, evt )

    @pyqtSlot(int)
    def trayActivated( self, reason ):
	if QSystemTrayIcon.DoubleClick == reason or QSystemTrayIcon.Trigger == reason:
	    self.show()

    def createUI( self ):
	self.ui = Ui_Form()
	self.ui.setupUi( self )
	self.nowTimeText = time.strftime(u'%H:%M:%S'.encode('utf-8')).decode('utf-8') 
	self.ui.labelStartTime.setText( self.nowTimeText )
	self.ui.labelEndTime.setText( '' )
	self.ui.lineEditTimeCount.setFocus()
	self.msgLabel = QLabel( u'<h1>时间到!</h1><img src=":/img/38.gif"/>' )

    def createConnections( self ):
	self.connect( self.ui.btnSetStartTime, SIGNAL('clicked()'),\
		self.updateStartTime )
	self.connect( self.ui.btnStartTimer, SIGNAL('clicked()'), \
		self.startTimer )
	self.connect( self.ui.btnComplete, SIGNAL('clicked()'), \
		self.missionComplete )

    def startTimer( self ):
	self.nowTimeText = time.strftime(u'%H:%M:%S'.encode('utf-8')).decode('utf-8') 
	self.ui.labelStartTime.setText( self.nowTimeText )

	self.timer = QTimer()
	minute = self.ui.lineEditTimeCount.text()
	try:
	    minute = float( minute )
	except ValueError:
	    return
	self.timer.singleShot( minute*60*1000, self, SLOT('timeOutMsg()'))
	self.mainTimerTimeout = False

	dueTimeText = datetime.datetime.fromtimestamp( time.time() + minute*60 ).strftime( u'%H:%M:%S'.encode('utf8') ).decode( 'utf8' )
	self.ui.labelEndTime.setText( dueTimeText )

	self.mission = DB.dailyEvent()
	desc = self.ui.LEDescription.text()
	if len(desc) != 0:
	    self.mission.setDescription( desc )
	
	self.resetIntervalTimer()

    def resetIntervalTimer( self ):
	if None == self.intervalTimer:
	    self.intervalTimer = QTimer()
	    self.connect( self.intervalTimer, SIGNAL('timeout()'), self.intervalNoticeMsg)
	else:
	    self.intervalTimer.stop()

	self.intervalNoticeTime = self.ui.intervalNoticeEdit.text()
	if self.intervalNoticeTime != '':
	    try:
		self.intervalNoticeTime = float( self.intervalNoticeTime )
	    except ValueError:
		return
	    self.intervalCount = 0
	    self.intervalTimer.start( self.intervalNoticeTime*60*1000 )



    @pyqtSlot()
    def intervalNoticeMsg( self ):
	if not self.mission.isComplete():
	    self.intervalCount = self.intervalCount + 1
	    self.systemTray.showMessage( u'友情提醒', u'已经过了'+unicode( self.intervalCount )+u'个'+unicode(self.intervalNoticeTime)+u'分钟\n'+u'有木有!'*20, QSystemTrayIcon.Information, 2000 )


    @pyqtSlot()
    def missionComplete( self ):
	self.mission.setEndTimeNow()
	self.intervalCount = 0
	self.mission.setComplete()
	self.mission.storeEvent()

    @pyqtSlot()
    def timeOutMsg( self ):
	#self.msgLabel.setWindowFlags( Qt.FramelessWindowHint )
	self.msgLabel.setGeometry( 400, 400, self.size().width(), self.size().height() )
	#self.timer.singleShot( 2800, self.msgLabel, SLOT('hide()') )
	self.msgLabel.show()
	self.mission.setTimeouted()
	self.mainTimerTimeout = True

    @pyqtSlot()
    def noTrayClose( self ):
	self.quitWithoutTray = True
	self.close()
	sys.exit()

    @pyqtSlot()
    def updateStartTime( self ):
	text = self.ui.lineEditStartTime.text()
	if len(text) < 1:
	    self.nowTimeText = time.strftime(u'%H:%M:%S'.encode('utf-8')).decode('utf-8') 
	    text =  self.nowTimeText
	else:
	    infer = TimeInference( text )

	self.ui.labelStartTime.setText( text )

    def createSystemTray( self ):
	self.systemTray = QSystemTrayIcon( self )
	self.trayIcon = QIcon( ':/systemTray/tray.ico' )
	self.trayMenu = QMenu( self )
	self.exitAction = QAction( u'退出', self )
	self.showAction = QAction( u'显示', self )
	self.connect( self.exitAction, SIGNAL('triggered()'), self.noTrayClose )
	self.connect( self.showAction, SIGNAL('triggered()'), self.show )
	self.trayMenu.addAction( self.exitAction )
	self.trayMenu.addAction( self.showAction )
	self.systemTray.setContextMenu( self.trayMenu )
	self.systemTray.setIcon( self.trayIcon )
	#self.connect( self.systemTray, SIGNAL('activated(int)'), self.trayActivated )
	self.systemTray.activated.connect( self.trayActivated )
	self.systemTray.show()
    pass

if __name__ == "__main__":
    a = QApplication( sys.argv )
    a.setQuitOnLastWindowClosed( False )
    mywidget = MainWidget()
    mywidget.show()
    sys.exit( a.exec_() )

