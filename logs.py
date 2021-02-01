#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
import parameters as PA
import tools

# System
import os, logging
from datetime import date

##############################################
# Logs
##############################################

def create_log(recordType="",recordID="",logName=""):
  if PA.LogTitle != "":
    logName=PA.LogTitle
  today = str(date.today())
  logPath = PA.FulcrumPath+"/logs/"+today+"/"
  if not os.path.exists(logPath):
    os.makedirs(logPath)
  logFilename = logPath+today+"_"+logName+"_"+recordType
  if recordID != "":
    logFilename = logFilename+"_"+recordID
  logFilename = logFilename+".log"
  logging.basicConfig(name=logName, level=logging.INFO,
                      filename=logFilename, filemode="a+",
                      format="%(asctime)-15s %(levelname)-8s %(message)s")

def l_info(v,logName=""):
  if PA.LogTitle != "":
    logName=PA.LogTitle
  logger = logging.getLogger(logName)
  print v
  logger.info(v)

def l_war(v,logName=""):
  if PA.LogTitle != "":
    logName=PA.LogTitle
  logger = logging.getLogger(logName)
  print v
  logger.warning(v)

def l_err(v,logName=""):
  if PA.LogTitle != "":
    logName=PA.LogTitle
  logger = logging.getLogger(logName)
  print v
  logger.error(v)

def l_debug(v,logName=""):
  if PA.LogTitle != "":
    logName=PA.LogTitle
  if PA.Debug == 'True':
    l_info(v,logName)

