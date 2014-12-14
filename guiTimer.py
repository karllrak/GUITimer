#!/usr/bin/python
#coding=utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import QLocalServer, QLocalSocket
from ui.ui_guiTimer import Ui_MainWindow
from MyLabel import MyLabel
from EventItemController import getWidgetWithData
import ui.qrc_guiTimer_rc
import sys
import time
from datetime import datetime, timedelta
import DB

LOCALSERVER = None

class MyMainWindow(QMainWindow):
    """ the widget """
    def __init__(self):
        ''' the init function '''
        QWidget.__init__(self)
        self.createSystemTray()
        self.createUI()
        self.createConnections()
        self.createActions()
        self.setWindowTitle(u'定时器')
        #then the size policy
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.quitWithoutTray = False
        #then the positon/geometry
        self.setGeometry(400, 400, self.size().width(), self.size().height())

        self.mission = None
        self.intervalTimer = None
        DB.initTables()

    def closeEvent(self, evt):
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

    def showAllShortCut(self):
        '''
        not implemented
        show all shortcuts set
        '''
        pass

    def keyPressEvent(self, evt):
        if evt.key() == Qt.Key_Escape or (evt.key() == Qt.Key_W\
                and evt.modifiers() & Qt.ControlModifier):
            self.hide()
            self.msgLabel.hide()#TODO no esc effect
            if self.msgLabel.isVisible():
                self.msgLabel.hide()
        elif (evt.key() == Qt.Key_Q and evt.modifiers()&Qt.ControlModifier):
            self.noTrayClose()
        #global shortcut to invoke the app, not implemented
        elif (evt.key() == Qt.Key_T and evt.modifiers()&Qt.AltModifier):
            self.show()
        else:
            QWidget.keyPressEvent(self, evt)

    @pyqtSlot(int)
    def trayActivated(self, reason):
        if QSystemTrayIcon.DoubleClick == reason or QSystemTrayIcon.Trigger == reason:
            self.show()

    def createUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.nowTimeText = time.strftime(u'%H:%M:%S'.encode('utf-8')).decode('utf-8') 
        self.ui.labelStartTime.setText(self.nowTimeText)
        self.ui.labelEndTime.setText('')
        self.ui.lineEditTimeCount.setFocus()
        self.msgLabel = MyLabel(u'<h1>时间到!</h1><img src=":/img/38.gif"/>')
        self.msgLabel.hide()
        self.msgLabel.setBuddy(self)
        self.ui.btnComplete.setDisabled(True)
        self.ui.btnDiscard.setDisabled(True)

    def createConnections(self):
        self.connect(self.ui.btnStartTimer, SIGNAL('clicked()'), \
                self.startTimer)
        self.connect(self.ui.btnComplete, SIGNAL('clicked()'), \
                self.missionComplete)
        self.connect(self.ui.btnDiscard, SIGNAL('clicked()'), \
                self.missionDiscarded)

    def createActions(self):
        self.ui.actViewData.setShortcut('Alt+D')
        self.connect(self.ui.actViewData, SIGNAL('triggered()'),
                self.viewData)

    @pyqtSlot()
    def viewData(self):
        self.dataWidget = getattr(self, 'dataWidget', False)
        if not self.dataWidget:
            self.dataWidget = getWidgetWithData()
        if self.dataWidget.isVisible():
            self.dataWidget.hide()
        else:
            self.dataWidget.show()

    def startTimer(self):
        #ui update
        self.nowTimeText = time.strftime(u'%H:%M:%S'.encode('utf-8')).decode('utf-8')
        minute = self.ui.lineEditTimeCount.text()
        try:
            minute = float(minute)
            self.timeCount = minute
        except ValueError:
            return
        self.ui.labelStartTime.setText(self.nowTimeText)
        self.dueTime = datetime.now() + timedelta(seconds=minute*60)
        dueTimeText = self.dueTime.strftime(u'%H:%M:%S'.encode('utf8')).decode('utf8')
        self.ui.labelEndTime.setText(dueTimeText)

        self.ui.btnStartTimer.setDisabled(True)
        self.ui.btnComplete.setDisabled(False)
        self.ui.btnDiscard.setDisabled(False)
        #then timer
        self.mainTimer = QTimer()
        self.mainTimer.singleShot(minute*60*1000, self, SLOT('timeOutMsg()'))

        self.mission = DB.dailyEvent()
        desc = self.ui.LEDescription.toPlainText()
        if len(desc) != 0:
            self.mission.setDescription(desc)

        self.resetIntervalTimer()

    def resetIntervalTimer(self):
        if None == self.intervalTimer:
            self.intervalTimer = QTimer()
            self.connect(self.intervalTimer, SIGNAL('timeout()'), self.intervalNoticeMsg)
        else:
            self.intervalTimer.stop()

        self.intervalNoticeTime = self.ui.intervalNoticeEdit.text()
        if self.intervalNoticeTime != '':
            try:
                self.intervalNoticeTime = float(self.intervalNoticeTime)
            except ValueError:
                return
            self.intervalCount = 0
            self.intervalTimer.start(self.intervalNoticeTime*60*1000)

    @pyqtSlot()
    def missionDiscarded(self):
        #db
        self.mission.setDiscarded()
        self.mission.setEndTimeNow()
        self.mission.storeEvent()
        #ui
        self.ui.btnComplete.setDisabled(True)
        self.ui.btnDiscard.setDisabled(True)
        self.ui.btnStartTimer.setDisabled(False)
        self.updateProgress()
        #timers
        self.mainTimer.stop()
        self.intervalTimer.stop()
        self.intervalCount = 0
        #TODO duplicated code!
        #TODO ui state change waiting -> in progress -> waiting

    @pyqtSlot()
    def intervalNoticeMsg(self):
        if not self.mission.isComplete() and not self.mission.isDiscarded():
            self.intervalCount = self.intervalCount + 1
            self.systemTray.showMessage(u'友情提醒', u'已经过了'+unicode(self.intervalCount)+u'个'+unicode(self.intervalNoticeTime)+u'分钟\n'+u'有木有!'*20, QSystemTrayIcon.Information, 2000)
            self.updateProgress()


    @pyqtSlot()
    def missionComplete(self):
        #db
        self.mission.setEndTimeNow()
        self.mission.setComplete()
        #if complete in 30s, marked as not timeouted
        if datetime.now() > self.dueTime + timedelta(seconds=30):
            self.mission.setTimeouted()

        self.mission.storeEvent()
        #ui
        self.ui.btnComplete.setDisabled(True)
        self.ui.btnDiscard.setDisabled(True)
        self.ui.btnStartTimer.setDisabled(False)
        self.updateProgress()
        #timer
        self.intervalCount = 0
        if self.mainTimer:
            self.mainTimer.stop()

    @pyqtSlot()
    def noTrayClose(self):
        self.quitWithoutTray = True
        self.close()
        sys.exit()

    @pyqtSlot()
    def timeOutMsg(self):
        if self.dueTime+timedelta(milliseconds=100) > datetime.now() > self.dueTime and not self.mission.isComplete():
            #if this is the right timeoutMsg, that is, not a discarded one, so, in the interval
            self.mainTimer.stop()
            self.msgLabel.setWindowFlags(Qt.FramelessWindowHint)
            self.msgLabel.setGeometry(self.msgLabel.width(), self.msgLabel.height(), self.size().width(), self.size().height())
            self.msgLabel.show()

    @pyqtSlot()
    def updateStartTime(self):
        text = self.ui.lineEditStartTime.text()
        if len(text) < 1:
            self.nowTimeText = time.strftime(u'%H:%M:%S'.encode('utf-8')).decode('utf-8') 
            text =  self.nowTimeText
        else:
            infer = TimeInference(text)

        self.ui.labelStartTime.setText(text)

    def updateProgress(self):
        startTime = self.mission.startTime
        nowTime = datetime.now()
        usedSeconds = (nowTime-startTime).seconds
        progress = usedSeconds / float(self.timeCount*60)
        progress = 1 if progress > 1 else progress
        self.ui.progressBar.setValue(int(progress * 100))
        pass

    def createSystemTray(self):
        self.systemTray = QSystemTrayIcon(self)
        self.trayIcon = QIcon(':/systemTray/tray.ico')
        self.trayMenu = QMenu(self)
        self.exitAction = QAction(u'退出', self)
        self.showAction = QAction(u'显示', self)
        self.connect(self.exitAction, SIGNAL('triggered()'), self.noTrayClose)
        self.connect(self.showAction, SIGNAL('triggered()'), self.show)
        self.trayMenu.addAction(self.exitAction)
        self.trayMenu.addAction(self.showAction)
        self.systemTray.setContextMenu(self.trayMenu)
        self.systemTray.setIcon(self.trayIcon)
        #self.connect(self.systemTray, SIGNAL('activated(int)'), self.trayActivated)
        self.systemTray.activated.connect(self.trayActivated)
        self.systemTray.show()
    pass

def showMainWindow():
    global mywindow
    print 're entering the application!'
    if mywindow.hasFocus():
        pass
    else:
        mywindow.hide()
        mywindow.show()

def testSingleInstanceOrExit():
    connected = False
    #try connect to QLocalServer
    local_sock = QLocalSocket()
    import sys
    QObject.connect(local_sock, SIGNAL('connected()'), sys.exit)
    connected = local_sock.connectToServer(qApp.applicationName())
    global LOCALSERVER
    if not connected:
        LOCALSERVER = QLocalServer()
        print 'setting up localserver', qApp.applicationName()
        ret = LOCALSERVER.listen(qApp.applicationName())
        if not ret:
            import os
            try:
                #todo not good way to remove /tmp/guiTimer.py
                os.remove('/tmp/'+qApp.applicationName())
                ret = LOCALSERVER.listen(qApp.applicationName())
            except:
                raise Exception('LOCALSERVER listen failed'
                        'you may need to remove /tmp/guiTimer.py manually')
        QObject.connect(LOCALSERVER, SIGNAL('newConnection()'), showMainWindow)
    else:
        print 'local socket connected'
        pass

    pass
def clearSockets():
    global LOCALSERVER
    if LOCALSERVER:
        LOCALSERVER.close()

if __name__ == "__main__":
    a = QApplication(sys.argv)
    a.setQuitOnLastWindowClosed(False)
    testSingleInstanceOrExit()
    mywindow = MyMainWindow()
    mywindow.show()
    import atexit
    atexit.register(clearSockets)
    sys.exit(a.exec_())

