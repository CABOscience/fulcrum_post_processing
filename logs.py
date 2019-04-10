#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
import tools

# System
import os, logging
from datetime import date

##############################################
# Logs
##############################################

def create_log(logName="main",recordID="",recordType=""):
  today = str(date.today())
  logPath = tools.get_script_directory()+"/logs/"+today+"/"
  if not os.path.exists(logPath):
    os.makedirs(logPath)
  logFilename = logPath+today+logName+"_"+recordType+"_"+recordID+".log"
  logging.basicConfig(name=logName, level=logging.INFO,
                      filename=logFilename, filemode="a+",
                      format="%(asctime)-15s %(levelname)-8s %(message)s")

def l_info(v,logName="main"):
  logger = logging.getLogger(logName)
  print v
  logger.info(v)

def l_war(v,logName="main"):
  logger = logging.getLogger(logName)
  print v
  logger.warning(v)

def l_err(v,logName="main"):
  logger = logging.getLogger(logName)
  print v
  logger.error(v)

def l_debug(v,logName="main"):
  print v

