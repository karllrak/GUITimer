#!/usr/bin/python
#coding=utf-8

import json
import os
import sys

if getattr( sys, 'frozen', False ):
    APPLICATION_PATH = os.path.dirname( sys.executable )
else:
    APPLICATION_PATH = os.path.dirname( __file__ )

CONFIGFILEPATH = os.sep.join([APPLICATION_PATH, 'user_config'])

def initConfigFile(filePath):
    '''exception of file related propagated to outer funcs'''
    f = open(CONFIGFILEPATH, 'w')
    f.write('#This is the config file of application {0},'
            'and the first line will be ignored'.format('GUITimer') + '\r\n')
    f.write('{}')
    f.close()
    return

def performConfigUgly(config, configName, widget):
    if config.has_key(configName):
        #todo
        pass
    else:
        pass

def loadConfig(configName, widget):
    '''
    load the saved config for given configName or do nothing
    Notice: rely on global variable CONFIGFILEPATH
    '''
    #assure there is a config file or return
    config = None
    try:
        f = open(CONFIGFILEPATH, 'r')
    except IOError:
        initConfigFile(CONFIGFILEPATH)
        try:
            f = open(CONFIGFILEPATH, 'r')
        except:
            #MyLog('e', 'config file #'+CONFIGFILEPATH+'#')
            #todo yet
            return

    f.readline()
    config = json.loads(f.read())
    f.close()
    performConfigUgly(config, configName, widget)
    return
