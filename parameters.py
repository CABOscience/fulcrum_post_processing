#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
import tools_fulcrum_api as TOFA
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
FulcrumForms      = []
FulcrumProjects   = []
FulcrumRecords    = []
KeysDataname      = []
LogTitle          = "main"
FormsProcess      = True
WebhookProcess    = False
DirectoriesProcess= False
NumberOfRequests  = 0
RecordStatus      = "verified" #choices={pending, rejected, verified, submitted, approved, published, deleted}

# From config
DefaultPath       = os.path.expanduser('~/')
BulkLeafSamplesLogFile = DefaultPath
BulkLeafSamplesFormFile = DefaultPath
BulkLeafSamplesRecordsFile = DefaultPath
DatabaseName = ''
DatabaseUser = ''
DatabaseHostName = ''
CampaignsPath = DefaultPath
Debug = False
FulcrumApiKey   = ""
FulcrumApiURL   = 'https://api.fulcrumapp.com/api/v2/'
FulcrumBackupScript = DefaultPath
FulcrumBulkFile = DefaultPath
FulcrumBulkFormId = ""
FulcrumPath = DefaultPath
FulcrumVersion  = '1.11.0'
FulcrumWebhook = DefaultPath
GoogleDrivePath = DefaultPath
IsParallel = True
LeafSpectraFormFile = DefaultPath
LeafSpectraLogFile = DefaultPath
LeafSpectraRecordsFile = DefaultPath
LimitExceededStr  = 'because you have exceeded the number of request.'
NotFoundStr       = 'because it was not found.'
NumberOfProcesses = 1
PanelCalibPath = DefaultPath
PanelCalibrationLogFile = DefaultPath
PanelCalibrationsFormFile = DefaultPath
PanelCalibrationsRecordsFile = DefaultPath
PanelsPath = DefaultPath
PlantsFormFile = DefaultPath
PlantsLogFile = DefaultPath
PlantsRecordsFile = DefaultPath
PlotsFormFile = DefaultPath
PlotsLogFile = DefaultPath
PlotsRecordsFile = DefaultPath
ProjectWebsitePath = DefaultPath
ScriptPath = TO.get_script_directory()
SitesFormFile = DefaultPath
SitesLogFile = DefaultPath
SitesRecordsFile = DefaultPath
SpectroscopyPanelsFormFile = DefaultPath
SpectroscopyPanelsLogFile = DefaultPath
SpectroscopyPanelsRecordsFile = DefaultPath
SubplotsFormFile = DefaultPath
SubplotsLogFile = DefaultPath
SubplotsRecordsFile = DefaultPath
WebsitePath = DefaultPath
WebhookID = ''

# Path to config
ConfFile           = ScriptPath+'/config.ini'

# Set Variables from config files
##############################################
def set_parameters():
  TOFA.check_fulcrum_version()
  if TO.file_is_here(ConfFile):
    c = get_config(ConfFile)
    set_global_from_config(c)
  get_arguments()
  print_arguments()

def set_logTitle(s):
  global LogTitle
  LogTitle = s

def wrong_parameters():
  print("You have some wrong parameters or arguments")
  sys.exit(1)

def get_config(confFile):
  config = configparser.ConfigParser()
  config.optionxform=str
  try:
    config.read(os.path.expanduser(confFile))
    return config
  except Exception as e:
    print(e)
    sys.exit(1)

def set_global_from_config(c):
    global BulkLeafSamplesLogFile
    global BulkLeafSamplesFormFile
    global BulkLeafSamplesRecordsFile
    global CampaignsPath
    global Debug
    global DefaultPath
    global DatabaseUser
    global DatabaseName
    global DatabaseHostName
    global FulcrumApiKey
    global FulcrumApiURL
    global FulcrumBackupScript
    global FulcrumBulkFormId
    global FulcrumPath
    global FulcrumVersion
    global FulcrumWebhook
    global GoogleDrivePath
    global IsParallel
    global LeafSpectraFormFile
    global LeafSpectraLogFile
    global LeafSpectraRecordsFile
    global LimitExceededStr
    global NotFoundStr
    global NumberOfProcesses
    global PanelCalibPath
    global PanelCalibrationLogFile
    global PanelCalibrationsFormFile
    global PanelCalibrationsRecordsFile
    global PanelsPath
    global PlantsFormFile
    global PlantsLogFile
    global PlantsRecordsFile
    global PlotsFormFile
    global PlotsLogFile
    global PlotsRecordsFile
    global ProjectWebsitePath
    global ScriptPath
    global SitesFormFile
    global SitesLogFile
    global SitesRecordsFile
    global SpectroscopyPanelsFormFile
    global SpectroscopyPanelsLogFile
    global SpectroscopyPanelsRecordsFile
    global SubplotsFormFile
    global SubplotsLogFile
    global SubplotsRecordsFile
    global WebsitePath
    global WebhookID
    global CaboWebsite
    
    if c.get('DEFAULT','BulkLeafSamplesLogFile'): BulkLeafSamplesLogFile = c.get('DEFAULT','BulkLeafSamplesLogFile')
    if c.get('DEFAULT','BulkLeafSamplesFormFile'): BulkLeafSamplesFormFile = c.get('DEFAULT','BulkLeafSamplesFormFile')
    if c.get('DEFAULT','BulkLeafSamplesRecordsFile'): BulkLeafSamplesRecordsFile = c.get('DEFAULT','BulkLeafSamplesRecordsFile')
    if c.get('DEFAULT','CampaignsPath'): CampaignsPath = c.get('DEFAULT','CampaignsPath')
    if c.get('DEFAULT','Debug'): Debug = c.get('DEFAULT','Debug')
    if c.get('DEFAULT','DefaultPath'): DefaultPath = c.get('DEFAULT','DefaultPath')
    if c.get('DEFAULT','DatabaseName'): DatabaseName = c.get('DEFAULT','DatabaseName')
    if c.get('DEFAULT','DatabaseUser'): DatabaseUser = c.get('DEFAULT','DatabaseUser')
    if c.get('DEFAULT','DatabaseHostName'): DatabaseHostName = c.get('DEFAULT','DatabaseHostName')
    if c.get('DEFAULT','FulcrumApiKey'): FulcrumApiKey = c.get('DEFAULT','FulcrumApiKey')
    if c.get('DEFAULT','FulcrumApiURL'): FulcrumApiURL = c.get('DEFAULT','FulcrumApiURL')
    if c.get('DEFAULT','FulcrumBackupScript'): FulcrumBackupScript = c.get('DEFAULT','FulcrumBackupScript')
    if c.get('DEFAULT','FulcrumBulkFormId'): FulcrumBulkFormId = c.get('DEFAULT','FulcrumBulkFormId')
    if c.get('DEFAULT','FulcrumPath'): FulcrumPath = c.get('DEFAULT','FulcrumPath')
    if c.get('DEFAULT','FulcrumVersion'): FulcrumVersion = c.get('DEFAULT','FulcrumVersion')
    if c.get('DEFAULT','FulcrumWebhook'): FulcrumWebhook = c.get('DEFAULT','FulcrumWebhook')
    if c.get('DEFAULT','GoogleDrivePath'): GoogleDrivePath = c.get('DEFAULT','GoogleDrivePath')
    if c.get('DEFAULT','IsParallel'): IsParallel = c.get('DEFAULT','IsParallel')
    if c.get('DEFAULT','LeafSpectraFormFile'): LeafSpectraFormFile = c.get('DEFAULT','LeafSpectraFormFile')
    if c.get('DEFAULT','LeafSpectraLogFile'): LeafSpectraLogFile = c.get('DEFAULT','LeafSpectraLogFile')
    if c.get('DEFAULT','LeafSpectraRecordsFile'): LeafSpectraRecordsFile = c.get('DEFAULT','LeafSpectraRecordsFile')
    if c.get('DEFAULT','LimitExceededStr'): LimitExceededStr = c.get('DEFAULT','LimitExceededStr')
    if c.get('DEFAULT','NotFoundStr'): NotFoundStr = c.get('DEFAULT','NotFoundStr')
    if c.get('DEFAULT','NumberOfProcesses'): NumberOfProcesses = int(c.get('DEFAULT','NumberOfProcesses'))
    if c.get('DEFAULT','PanelCalibPath'): PanelCalibPath = c.get('DEFAULT','PanelCalibPath')
    if c.get('DEFAULT','PanelCalibrationLogFile'): PanelCalibrationLogFile = c.get('DEFAULT','PanelCalibrationLogFile')
    if c.get('DEFAULT','PanelCalibrationsFormFile'): PanelCalibrationsFormFile = c.get('DEFAULT','PanelCalibrationsFormFile')
    if c.get('DEFAULT','PanelCalibrationsRecordsFile'): PanelCalibrationsRecordsFile = c.get('DEFAULT','PanelCalibrationsRecordsFile')
    if c.get('DEFAULT','PanelsPath'): PanelsPath = c.get('DEFAULT','PanelsPath')
    if c.get('DEFAULT','PlantsFormFile'): PlantsFormFile = c.get('DEFAULT','PlantsFormFile')
    if c.get('DEFAULT','PlantsLogFile'): PlantsLogFile = c.get('DEFAULT','PlantsLogFile')
    if c.get('DEFAULT','PlantsRecordsFile'): PlantsRecordsFile = c.get('DEFAULT','PlantsRecordsFile')
    if c.get('DEFAULT','PlotsFormFile'): PlotsFormFile = c.get('DEFAULT','PlotsFormFile')
    if c.get('DEFAULT','PlotsLogFile'): PlotsLogFile = c.get('DEFAULT','PlotsLogFile')
    if c.get('DEFAULT','PlotsRecordsFile'): PlotsRecordsFile = c.get('DEFAULT','PlotsRecordsFile')
    if c.get('DEFAULT','ProjectWebsitePath'): ProjectWebsitePath = c.get('DEFAULT','ProjectWebsitePath')
    if c.get('DEFAULT','ScriptPath'): ScriptPath = c.get('DEFAULT','ScriptPath')
    if c.get('DEFAULT','SitesFormFile'): SitesFormFile = c.get('DEFAULT','SitesFormFile')
    if c.get('DEFAULT','SitesLogFile'): SitesLogFile = c.get('DEFAULT','SitesLogFile')
    if c.get('DEFAULT','SitesRecordsFile'): SitesRecordsFile = c.get('DEFAULT','SitesRecordsFile')
    if c.get('DEFAULT','SpectroscopyPanelsFormFile'): SpectroscopyPanelsFormFile = c.get('DEFAULT','SpectroscopyPanelsFormFile')
    if c.get('DEFAULT','SpectroscopyPanelsLogFile'): SpectroscopyPanelsLogFile = c.get('DEFAULT','SpectroscopyPanelsLogFile')
    if c.get('DEFAULT','SpectroscopyPanelsRecordsFile'): SpectroscopyPanelsRecordsFile = c.get('DEFAULT','SpectroscopyPanelsRecordsFile')
    if c.get('DEFAULT','SubplotsFormFile'): SubplotsFormFile = c.get('DEFAULT','SubplotsFormFile')
    if c.get('DEFAULT','SubplotsLogFile'): SubplotsLogFile = c.get('DEFAULT','SubplotsLogFile')
    if c.get('DEFAULT','SubplotsRecordsFile'): SubplotsRecordsFile = c.get('DEFAULT','SubplotsRecordsFile')
    if c.get('DEFAULT','WebsitePath'): WebsitePath = c.get('DEFAULT','WebsitePath')
    if c.get('DEFAULT','WebhookID'): WebhookID = c.get('DEFAULT','WebhookID')
    if c.get('DEFAULT','CaboWebsite'): CaboWebsite = c.get('DEFAULT','CaboWebsite')

# Arguments
##############################################
def get_arguments():
  global Debug
  global IsParallel
 
  parser = argparse.ArgumentParser(description='Options Fulcrum Backup.')
  parser._action_groups.pop()

  #required = parser.add_argument_group('optional arguments')
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
  optional.add_argument('-fi', '--file', type=str,
    dest="file", help="Choose a file for bulk import")
  
  '''
  exclusive1 = parser.add_mutually_exclusive_group()
  exclusive1.add_argument('--debug', action='store_true',
    dest="debug", help="Enable debug")
  exclusive1.add_argument('--no-debug', action='store_false',
    dest="debug", help="Disable debug")
  if Debug and ( Debug == "True" or Debug == "False"):
    parser.set_defaults(debug=Debug)
  else:
    parser.set_defaults(debug=False)

  exclusive2 = parser.add_mutually_exclusive_group()
  exclusive2.add_argument('--parallel', action='store_true',
    dest="parallel", help="Enable parrallelisation")
  exclusive2.add_argument('--no-parallel', action='store_false',
    dest="parallel", help="disable parrallelisation")
  if IsParallel and ( IsParallel == "True" or IsParallel == "False"):
    parser.set_defaults(parallel=IsParallel)
  else:
    parser.set_defaults(parallel=False)
  '''
  
  exclusive = parser.add_mutually_exclusive_group()
  exclusive.add_argument('-f', '--form', nargs='+',
    dest="form", help="Fulcrum Backup: Load all records from Selected Leaf Spectra form(s) and process them")
  exclusive.add_argument('-w', '--webhooks', action='store_true',
    dest="webhooks", help="Load all records from All Leaf Spectra from webhooks")
  exclusive.add_argument('-r', '--records', nargs='+',
    dest="records", help="From Fulcrum Backup: Load record(s) and process them")
  exclusive.add_argument('-j', '--projects', nargs='+',
    dest="projects", help="From Fulcrum Backup: Load porject(s) and process them")

  args = parser.parse_args()

  '''
  if args.debug:
    Debug = "True"
  elif not args.debug:
    Debug = "False"

  if args.parallel:
    IsParallel = "True"
  elif not args.parallel:
    IsParallel = "False"
  '''

  if args.form and len(args.form)>0:
    global FulcrumForms
    FulcrumForms = args.form
  
  if args.projects and len(args.projects)>0:
    global FulcrumProjects
    FulcrumProjects = args.projects

  if args.webhooks:
    global WebhookProcess
    WebhookProcess = True
    global FormsProcess
    FormsProcess = False
    global LogTitle
    LogTitle = "webhook" 
    #global NumberOfProcesses
    #NumberOfProcesses = 1
  
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

  if args.file:
    if (os.path.isfile(args.file)):
      global FulcrumBulkFile
      print('Pssst: Fulcrum Bulk File is {}'.format(args.file))
      FulcrumBulkFile = args.file
    else:
      print('ERROR: Fulcrum Bulk File is not a file {}'.format(args.file))
      wrong_parameters()

def print_arguments():
  if Debug == 'True':
    print('Debug is enabled')
  else:
    print('Debug is disable')

  if IsParallel == 'True':
    print('Parallelisation is enabled')
  else:
    print('Parallelisation is disable')

  if TOFA.test_fulcrum_access():
    print('Fulcrum is accessible')


