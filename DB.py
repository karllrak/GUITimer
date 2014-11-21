#!/usr/bin/python
#coding=utf-8
import sqlite3
from datetime import datetime
import time
import os
from config import APPLICATION_PATH

def initTables():
    con = getDBConnection()
    c = con.cursor()
    c.execute('create table if not exists dailyEvent('+\
            'description text,'+\
            'startTime datetime,'+\
            'endTime datetime,'+\
            'finished boolean default 0,'+\
            'timeouted boolean);')
    con.commit()
    con.close()

def getDBConnection():
    '''
    remember to close it!
    '''
    return sqlite3.connect(os.sep.join([APPLICATION_PATH, 'event.db']))

def getEventByPage(page, itemsPerPage):
    if page < 1 or itemsPerPage < 1: return ()
    con = getDBConnection()
    c = con.cursor()
    c.execute('select * from dailyEvent order by rowid desc limit ?,?', ((page-1)*itemsPerPage,itemsPerPage))
    data = c.fetchall()
    con.commit()
    con.close()
    return data

def getLatestEvent(count = 1):
    con = getDBConnection()
    c = con.cursor()
    c.execute('select * from dailyEvent order by rowid desc limit ?', (count,))
    data = c.fetchall()
    con.commit()
    con.close()
    return data

class dailyEvent:
    def __init__(self):
        self.startTime = datetime.now()
        self.timeouted = False
        self.description = u'无描述'
        self.endTime = datetime.now()

        self.complete = False
        self.stored = False
        self.discarded = False

    def setComplete(self):
        self.complete = True

    def setDiscarded(self):
        self.discarded = True

    def isDiscarded(self):
        return self.discarded

    def isComplete(self):
        return self.complete

    def setTimeouted(self):
        self.timeouted = True

    def setStartTimeNow(self):
        self.startTime = datetime.now()

    def setDescription(self, s):
        self.description = s

    def setEndTimeNow(self):
        self.endTime = datetime.now()

    def storeEvent(self, finished=1):
        if self.stored:
            return
        else:
            self.stored = True
        finished = 1 if self.complete else 0
        discarded = 1 if self.discarded else 0
        con = getDBConnection()
        c = con.cursor()
        c.execute('insert into dailyEvent(description, startTime, endTime, timeouted, finished, discarded)  values  (?, ?, ?, ?, ?, ?)',
                (unicode(self.description),
                    unicode(self.startTime.strftime('%Y-%m-%d %H:%M:%S')),
                    unicode(self.endTime.strftime('%Y-%m-%d %H:%M:%S')),
                    1 if self.timeouted else 0,
                    finished,
                    discarded),
               )
        con.commit()
        con.close()

if __name__ == '__main__':
    print getLatestEvent(2)
