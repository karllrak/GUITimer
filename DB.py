#!/usr/bin/python
#coding=utf-8
import sqlite3
import datetime
import time

def initTables():
    con = sqlite3.connect('event.db')
    c = con.cursor()
    c.execute( 'create table if not exists dailyEvent('+\
	    'description text,'+\
	    'startTime datetime,'+\
	    'endTime datetime,'+\
	    'timeouted boolean );' )
    con.commit()
    con.close()

class dailyEvent:
    def __init__( self ):
	self.startTime = time.strftime('%Y-%m-%d %H:%M:%S')
	self.timeouted = False
	self.description = u'无描述'
	self.endTime = time.strftime( '%Y-%m-%d %H:%M:%S' )
	self.complete = False

    def setComplete( self ):
	self.complete = True

    def isComplete( self ):
	return self.complete

    def setTimeouted( self ):
	self.timeouted = True

    def setStartTimeNow( self ):
	self.startTime = time.strftime( '%Y-%m-%d %H:%M:%S' ) 

    def setDescription( self, s ):
	self.description = s

    def setEndTimeNow( self ):
	self.endTime = time.strftime( '%Y-%m-%d %H:%M:%S' )

    def storeEvent( self ):
	con = sqlite3.connect( 'event.db' )
	c = con.cursor()
	c.execute( 'insert into dailyEvent values (?, ?, ?, ?)',
		    ( unicode(self.description),
		unicode(self.startTime),
		unicode(self.endTime),
		1 if self.timeouted else 0),
		)
	con.commit()
	con.close()


