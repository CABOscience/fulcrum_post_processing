#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
import parameters as PA
import tools as TO

# System
import os, logging
from datetime import date

##############################################
# Logs
##############################################

def create_log(recordType="",recordID="",logName=""):
  # Source https://stackoverflow.com/a/49202811
  for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
  if PA.LogTitle != "":
    logName=PA.LogTitle
  today = str(date.today())
  logPath = TO.get_fulcrum_path_and_basename("logs/"+today+"/")
  if not os.path.exists(logPath):
    os.makedirs(logPath)
  logFilename = logPath+today+"_"+logName+"_"+recordType
  if recordID != "":
    logFilename = logFilename+"_"+recordID
  logFilename = logFilename+".log"
  logging.basicConfig(level=logging.INFO,
                      filename=logFilename, filemode="a+",
                      format="%(asctime)-15s %(levelname)-8s %(message)s")
  

def l_info(v,logName=""):
  if PA.LogTitle != "":
    logName=PA.LogTitle
  logger = logging.getLogger(logName)
  print(v)
  logger.info(v)

def l_war(v,logName=""):
  if PA.LogTitle != "":
    logName=PA.LogTitle
  logger = logging.getLogger(logName)
  print(v)
  logger.warning(v)

def l_err(v,logName=""):
  if PA.LogTitle != "":
    logName=PA.LogTitle
  logger = logging.getLogger(logName)
  print(v)
  logger.error(v)

def l_debug(v,logName=""):
  if PA.LogTitle != "":
    logName=PA.LogTitle
  if PA.Debug == 'True':
    l_info('## DEBUG ==> {}'.format(v),logName)

