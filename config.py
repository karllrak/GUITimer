#!/usr/bin/python
#coding=utf-8
import sys
import os

if getattr( sys, 'frozen', False ):
    APPLICATION_PATH = os.path.dirname( sys.executable )
else:
    APPLICATION_PATH = os.path.dirname( __file__ )
