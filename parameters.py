#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
import tools as TO
# System
import argparse, os, sys
import configparser

'''
# Use config parser to set parameters it will allow to simplify the loading and be able to set default values
$ sudo apt install python-configparser
import configparser
config = configparser.RawConfigParser()
config.read('example.cfg')
'''

##############################################
# Parameters
##############################################

# Variables
##############################################
DefaultPath     = os.path.expanduser('~/')
FulcrumVersion  = '1.1.0'
FulcrumApiKey   = ""
FulcrumApiURL   = 'https://api.fulcrumapp.com/api/v2/'
FulcrumPath     = DefaultPath
FulcrumWebhook  = DefaultPath
GoogleDrivePath = DefaultPath
WebsitePath     = DefaultPath
Debug = False

BulkLeafSamplesFormFile   = FulcrumPath
BulkLeafSamplesRecordsFile= FulcrumPath
BulkLeafSamplesLogFile = 'BulkLeafSamples_pipeline'

SpectroscopyPanelsFormFile    = FulcrumPath
SpectroscopyPanelsRecordsFile = FulcrumPath
SpectroscopyPanelsLogFile     = 'SpectroscopyPanels_pipeline'

LeafSpectraFormFile   = FulcrumPath
LeafSpectraRecordsFile= FulcrumPath
LeafSpectraLogFile = 'leafspectra_pipeline'

CampaignsPath      = GoogleDrivePath
PanelsPath         = GoogleDrivePath
ScriptPath         = TO.get_script_directory()
ConfFile           = ScriptPath+'/config.ini'
FulcrumBackupScript= ScriptPath
ProjectWebsitePath = WebsitePath
FulcrumForms      = []
FulcrumRecords    = []
KeysDataname      = []
FormsProcess      = False
WebhookProcess    = False
DirectoriesProcess= False
LimitExceededStr  = 'because you have exceeded the number of request.'
NotFoundStr       = 'because it was not found.'
NumberOfProcesses = 1
NumberOfRequests  = 0
RecordStatus      = "verified" #choices={pending, rejected, verified, submitted, approved, published, deleted}

# Set Variables from config files
##############################################
def set_parameters():
  if TO.file_is_here(ConfFile):
    c = get_config(ConfFile)
    set_global_from_config(c)
  get_arguments()

def get_config(confFile):
  config = configparser.ConfigParser()
  config.optionxform=str
  try:
    config.read(os.path.expanduser(confFile))
    return config
  except Exception, e:
    print(e)
    sys.exit(1)

def set_global_from_config(c):
    global Debug
    global DefaultPath
    global FulcrumVersion
    global FulcrumApiKey
    global FulcrumApiURL
    global FulcrumPath
    global FulcrumWebhook
    global GoogleDrivePath
    global WebsitePath
    global SpectroscopyPanelsFormFile
    global SpectroscopyPanelsRecordsFile
    global SpectroscopyPanelsLogFile
    global LeafSpectraFormFile
    global LeafSpectraRecordsFile
    global LeafSpectraLogFile
    global CampaignsPath
    global PanelsPath
    global ScriptPath
    global FulcrumBackupScript
    global ProjectWebsitePath
    global LimitExceededStr
    global NotFoundStr
    global NumberOfProcesses

    t = c.get('DEFAULT','Debug')
    if t:
      Debug = c.get('DEFAULT','Debug')
    
    if Debug == 'True':
      print 'Debug is enabled'
    else:
      print 'Debug is disable'
      
    t = c.get('DEFAULT','DefaultPath')
    if t:
      DefaultPath = c.get('DEFAULT','DefaultPath')
    
    t = c.get('DEFAULT','FulcrumVersion')
    if t:
      FulcrumVersion = c.get('DEFAULT','FulcrumVersion')
    
    t = c.get('DEFAULT','FulcrumApiKey')
    if t:
      FulcrumApiKey = c.get('DEFAULT','FulcrumApiKey')
    
    t = c.get('DEFAULT','FulcrumApiURL')
    if t:
      FulcrumApiURL = c.get('DEFAULT','FulcrumApiURL')
    
    t = c.get('DEFAULT','FulcrumPath')
    if t:
      FulcrumPath = c.get('DEFAULT','FulcrumPath')
    
    t = c.get('DEFAULT','FulcrumWebhook')
    if t:
      FulcrumWebhook = c.get('DEFAULT','FulcrumWebhook')
    
    t = c.get('DEFAULT','FulcrumWebhook')
    if t:
      FulcrumWebhook = c.get('DEFAULT','FulcrumWebhook')
    
    t = c.get('DEFAULT','GoogleDrivePath')
    if t:
      GoogleDrivePath = c.get('DEFAULT','GoogleDrivePath')
    
    t = c.get('DEFAULT','WebsitePath')
    if t:
      WebsitePath = c.get('DEFAULT','WebsitePath')
    
    t = c.get('DEFAULT','SpectroscopyPanelsFormFile')
    if t:
      SpectroscopyPanelsFormFile = c.get('DEFAULT','SpectroscopyPanelsFormFile')
    
    t = c.get('DEFAULT','SpectroscopyPanelsRecordsFile')
    if t:
      SpectroscopyPanelsRecordsFile = c.get('DEFAULT','SpectroscopyPanelsRecordsFile')
    
    t = c.get('DEFAULT','SpectroscopyPanelsLogFile')
    if t:
      SpectroscopyPanelsLogFile = c.get('DEFAULT','SpectroscopyPanelsLogFile')
    
    t = c.get('DEFAULT','LeafSpectraFormFile')
    if t:
      LeafSpectraFormFile = c.get('DEFAULT','LeafSpectraFormFile')
    
    t = c.get('DEFAULT','LeafSpectraRecordsFile')
    if t:
      LeafSpectraRecordsFile = c.get('DEFAULT','LeafSpectraRecordsFile')
    
    t = c.get('DEFAULT','LeafSpectraLogFile')
    if t:
      LeafSpectraLogFile = c.get('DEFAULT','LeafSpectraLogFile')
    
    t = c.get('DEFAULT','CampaignsPath')
    if t:
      CampaignsPath = c.get('DEFAULT','CampaignsPath')
    
    t = c.get('DEFAULT','PanelsPath')
    if t:
      PanelsPath = c.get('DEFAULT','PanelsPath')
    
    t = c.get('DEFAULT','ScriptPath')
    if t:
      ScriptPath = c.get('DEFAULT','ScriptPath')
    
    t = c.get('DEFAULT','FulcrumBackupScript')
    if t:
      FulcrumBackupScript = c.get('DEFAULT','FulcrumBackupScript')
    
    t = c.get('DEFAULT','ProjectWebsitePath')
    if t:
      ProjectWebsitePath = c.get('DEFAULT','ProjectWebsitePath')
    
    t = c.get('DEFAULT','LimitExceededStr')
    if t:
      LimitExceededStr = c.get('DEFAULT','LimitExceededStr')
    
    t = c.get('DEFAULT','NotFoundStr')
    if t:
      NotFoundStr = c.get('DEFAULT','NotFoundStr')
    
    t = c.get('DEFAULT','NumberOfProcesses')
    if t:
      NumberOfProcesses = int(c.get('DEFAULT','NumberOfProcesses'))


# Arguments
##############################################
def get_arguments():
  parser = argparse.ArgumentParser(description='Options Fulcrum Backup.')
  parser._action_groups.pop()
  required = parser.add_argument_group('optional arguments')
  
  #required.add_argument('-a', '--fulcrumApiKey',
  #  dest="fulcrumApiKey", help="Need a fulcrum Api key")
  optional = parser.add_argument_group('Optional Arguments')
  optional.add_argument('-a', '--fulcrumApiKey',
    dest="fulcrumApiKey", help="Need a fulcrum Api key")
  optional.add_argument('-d', '--project-directories', action='store_true',
    dest="directories", help="Create project website view directories")
  optional.add_argument('-rs', '--record-status', choices={"pending", "rejected", "verified", "submitted", "approved", "published", "deleted"},
    dest="recordStatus", help="Select a status of record")
  optional.add_argument('-p', '--path', type=str,
    dest="path", help="Choose a directory where fulcrum is backuped")
  exclusive = parser.add_mutually_exclusive_group()
  exclusive.add_argument('-f', '--form', nargs='+',
    dest="form", help="Fulcrum Backup: Load all records from Selected Leaf Spectra form(s) and process them")
  exclusive.add_argument('-w', '--webhooks', action='store_true',
    dest="webhooks", help="Load all records from All Leaf Spectra from webhooks")
  exclusive.add_argument('-r', '--records', nargs='+',
    dest="records", help="From Fulcrum Backup: Load record(s) and process them")
  args = parser.parse_args()
  
  if args.form and len(args.form)>0:
    global FulcrumForms
    FulcrumForms = args.form
  else:
    global FormsProcess
    FormsProcess=True
  
  if args.webhooks:
    global WebhookProcess
    WebhookProcess = True
  
  if args.records and len(args.records)>0:
    global FulcrumRecords
    FulcrumRecords = args.records
  
  if args.recordStatus and len(args.recordStatus)==1:
    global RecordStatus
    RecordStatus = args.recordStatus
  
  if args.directories:
    global DirectoriesProcess
    DirectoriesProcess = True

  if args.fulcrumApiKey:
    global FulcrumApiKey
    FulcrumApiKey = args.fulcrumApiKey

  if args.path:
    argPath = args.path
    argPath = os.path.expanduser(argPath)
    argPath = os.path.abspath(argPath)
    if (os.path.isdir(argPath)):
      if not argPath.endswith('/'):
        argPath = argPath+'/'
      global FulcrumPath
      print('Pssst: FulcrumPath from config is override by an argument')
      FulcrumPath = argPath
    else:
      print('The current path is not a directory. The program will used the default path: >> {}'.format(fulcrumPath))

