#!/usr/bin/env python
#coding=utf

from PyQt4.QtGui import QLabel

class MyLabel(QLabel):
    '''extend QLabel and set shortcuts'''
    def __init__(self, s, parent=None):
        QLabel.__init__(self, s, parent)
        #super(MyLabel, self).__init__(s, parent)

    def keyPressEvent(self, e):
        self.hide()
        if self.buddy():
            self.buddy().show()
        super(MyLabel, self).keyPressEvent(e)

if __name__  == '__main__':
    import sys
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    app = QApplication(sys.argv)
    l = MyLabel(u'测试')
    l.show()
    sys.exit(app.exec_())

