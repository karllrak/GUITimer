#!/usr/bin/python
#coding=utf-8

import json
import os
import sys

if getattr( sys, 'frozen', False ):
    APPLICATION_PATH = os.path.dirname( sys.executable )
else:
    APPLICATION_PATH = os.path.dirname( __file__ )

def initConfigFile(filePath):
    #todo
    return

def loadConfig(configName):
    '''load the saved config for given configName or do nothing'''
    #assure there is a config file or return
    config = None
    try:
        f = open(configFilePath, 'r')
    except IOError:
        initConfigFile(configFilePath)
        try:
            f = open(configFilePath, 'r')
        except:
            #MyLog('e', 'config file #'+configFilePath+'#')
            #todo yet
            return

    config = json.loads(f.read())
    if config.has_key(configName):
        #todo
        pass
    else:
        pass
