#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
import parameters as PA
import tools as TO
import logs as LO

# System
import sys

##############################################
# Record
##############################################

# OBJECTS
#########################
class Records(object):
  def __init__(self):
    self.records=[]
    self.recordsDict={}
    
  def __len__(self):
    return len(self.records)
    
  def get_records(self):
    return self.records
  
  def __str__(self):
    tp = ""
    for record in self.records:
      if tp:
        tp += '\n'+record
      else:
        tp = record
    return tp

  def to_csv(self):
    tp = []
    for record in self.records:
      tp.append(record.to_csv())
    return tp
  
  def add_record(self,record_raw):
    self.records.append(record_raw)
    self.recordsDict[record_raw.ID]=record_raw


class Record(object):
  def __init__(self, Raltitude= "", RassignedTo= "", RassignedToId= "", RclientCreatedAt= "", RclientUpdatedAt= "", Rcourse= "", RcreatedAt= "", RcreatedBy= "", RcreatedById= "", RcreatedDuration= "", RcreatedLocation= "", ReditedDuration= "", RformId= "", RformValues= "", RhorizontalAccuracy= "", RID= "", Rlatitude= "", Rlongitude= "", RprojectId= "", Rspeed= "", Rstatus= "", RupdatedAt= "", RupdatedBy= "", RupdatedById= "", RupdatedDuration= "", RupdatedLocation= "", Rversion= "", RverticalAccuracy= "", RprojectName=''):
    self.altitude = Raltitude
    self.assigned_to = RassignedTo
    self.assigned_to_id = RassignedToId
    self.client_created_at = RclientCreatedAt
    self.client_updated_at = RclientUpdatedAt
    self.course = Rcourse
    self.created_at = RcreatedAt
    self.created_by = RcreatedBy
    self.created_by_id = RcreatedById
    self.created_duration = RcreatedDuration
    self.created_location = RcreatedLocation
    self.edited_duration = ReditedDuration
    self.form_id = RformId
    self.form_values = RformValues
    self.horizontal_accuracy = RhorizontalAccuracy
    self.ID = RID
    self.latitude = Rlatitude
    self.longitude = Rlongitude
    self.project_id = RprojectId
    self.speed = Rspeed
    self.status = Rstatus
    self.updated_at = RupdatedAt
    self.updated_by = RupdatedBy
    self.updated_by_id = RupdatedById
    self.updated_duration = RupdatedDuration
    self.updated_location = RupdatedLocation
    self.version = Rversion
    self.vertical_accuracy = RverticalAccuracy
    self.project_name = RprojectName
    self.isValid = True
    self.logInfo = ""
     

  def __str__(self):
    return '>{} - {}'.format(self.ID, self.form_id)

  def to_csv(self):
    return [self.altitude, self.assigned_to, self.assigned_to_id, self.client_created_at, self.client_updated_at, self.course, self.created_at, self.created_by, self.created_by_id, self.created_duration, self.created_location, self.edited_duration, self.form_id, self.horizontal_accuracy, self.ID, self.latitude, self.longitude, self.project_id, self.speed, self.status, self.updated_at, self.updated_by, self.updated_by_id, self.updated_duration, self.updated_location, self.version, self.vertical_accuracy]

  def to_info(self):
    return []

  #def whoami(self):
  #  print type(self).__name__
    
  def is_record(self):
    if self.ID and self.form_id:
      return True
    else:
      LO.l_war('The record id {} has no ID and/or "form_id" ({}). We will not be able to process it.'.format(self.ID,self.form_id))
      self.add_toLog('The record id {} has no ID and/or "form_id" ({}). We will not be able to process it.'.format(self.ID,self.form_id))
      return False
      
  def add_toLog(self, st):
    if not isinstance(st, basestring):
      print 'st'
      print st
    else:
     self.logInfo += "\n"+st

##############################################
# Records Functions
##############################################

def get_records_from_files_list(listFileRecords,projects=[]):
  records = Records()
  for fileRecord in listFileRecords:
    record_raw = record_from_fileName(fileRecord)
    if record_raw:
      project_name = projects[record_raw.project_id]
      records.add_record(project_name,record_raw)
  return records

def record_from_fileName(fileName):
  record_raw = TO.load_json_file(fileName)
  return extract_record_from_raw(record_raw)

def get_list_records_from_file(fileName):
  return TO.load_json_file(fileName)

def get_records_from_list(listRecords,projects=[]):
  records = Records()
  for record_raw in listRecords:
    record = extract_record_from_raw(record_raw,projects)
    records.add_record(record)
  return records

def extract_record_from_raw(record_raw,projects):
  Raltitude, RassignedTo, RassignedToId, RclientCreatedAt, RclientUpdatedAt, Rcourse, RcreatedAt, RcreatedBy, RcreatedById, RcreatedDuration, RcreatedLocation, ReditedDuration, RformId, RhorizontalAccuracy, RID, Rlatitude, Rlongitude, RprojectId, Rspeed, Rstatus, RupdatedAt, RupdatedBy, RupdatedById, RupdatedDuration, RupdatedLocation, Rversion, RverticalAccuracy, RformValues = ("",)*28
  if 'altitude' in record_raw:  Raltitude = record_raw['altitude']
  if 'assigned_to' in record_raw:  RassignedTo = record_raw['assigned_to']
  if 'assigned_to_id' in record_raw:  RassignedToId = record_raw['assigned_to_id']
  if 'client_created_at' in record_raw:  RclientCreatedAt = record_raw['client_created_at']
  if 'client_updated_at' in record_raw:  RclientUpdatedAt = record_raw['client_updated_at']
  if 'course' in record_raw:  Rcourse = record_raw['course']
  if 'created_at' in record_raw:  RcreatedAt = record_raw['created_at']
  if 'created_by' in record_raw:  RcreatedBy = record_raw['created_by']
  if 'created_by_id' in record_raw:  RcreatedById = record_raw['created_by_id']
  if 'created_duration' in record_raw:  RcreatedDuration = record_raw['created_duration']
  if 'created_location' in record_raw:  RcreatedLocation = record_raw['created_location']
  if 'edited_duration' in record_raw:  ReditedDuration = record_raw['edited_duration']
  if 'form_id' in record_raw:  RformId = record_raw['form_id']
  if 'form_values' in record_raw:  RhorizontalAccuracy = record_raw['horizontal_accuracy']
  if 'horizontal_accuracy' in record_raw:  RID = record_raw['id']
  if 'id' in record_raw:  Rlatitude = record_raw['latitude']
  if 'latitude' in record_raw:  Rlongitude = record_raw['longitude']
  if 'longitude' in record_raw:  RprojectId = record_raw['project_id']
  if 'project_id' in record_raw:  Rspeed = record_raw['speed']
  if 'speed' in record_raw:  Rstatus = record_raw['status']
  if 'status' in record_raw:  RupdatedAt = record_raw['updated_at']
  if 'updated_at' in record_raw:  RupdatedBy = record_raw['updated_by']
  if 'updated_by' in record_raw:  RupdatedById = record_raw['updated_by_id']
  if 'updated_by_id' in record_raw:  RupdatedDuration = record_raw['updated_duration']
  if 'updated_duration' in record_raw:  RupdatedLocation = record_raw['updated_location']
  if 'updated_location' in record_raw:  Rversion = record_raw['version']
  if 'version' in record_raw:  RverticalAccuracy = record_raw['vertical_accuracy']
  if 'vertical_accuracy' in record_raw:  RformValues = record_raw['form_values']
    
  record = Record(Raltitude, RassignedTo, RassignedToId, RclientCreatedAt, RclientUpdatedAt, Rcourse, RcreatedAt, RcreatedBy, RcreatedById, RcreatedDuration, RcreatedLocation, ReditedDuration, RformId, RformValues, RhorizontalAccuracy, RID, Rlatitude, Rlongitude, RprojectId, Rspeed, Rstatus, RupdatedAt, RupdatedBy, RupdatedById, RupdatedDuration, RupdatedLocation, Rversion, RverticalAccuracy)
  
  if record.project_id in projects:
    record.project_name = projects[record.project_id]
  else:
    LO.l_war('The record id {} is not associated project name with a project name and it has the project id {}.'.format(RID, record.project_id))
    record.add_toLog('The record id {} is not associated project name with a project name and it has the project id {}.'.format(RID, record.project_id))
  
  if Rstatus and 'deleted' in Rstatus:
    LO.l_err('Project {}, the record id {} will not be used because its status is deleted.'.format(RprojectId,RID))
    record.add_toLog('Project {}, the record id {} will not be used because its status is deleted.'.format(RprojectId,RID))
    record.isValid=False
  
  if not record.is_record():
    record.isValid=False
  
  return record


##############################################
# LOAD SOURCES
##############################################

# Load from Webhooks
##############################################
def load_webhook_records(projects=[]):
  webhookRecords = TO.get_files_from_path(PA.FulcrumWebhook+"records/")
  return get_records_from_files_list(webhookRecords,projects)

# Load from File Name
##############################################
def load_records_from_json(fileName,projects=[]):
  listRecords = get_list_records_from_file(fileName)
  return get_records_from_list(listRecords,projects)


##############################################
# Update Record with dataname
##############################################
def record_add_dataname_from_formFile(record,formFile):
  form_raw = TO.load_json_file(formFile)
  dictKeysDataname = form_raw['dictKeysDataname']
  if 'form_values' in record:
    search_datanames_keys_recu(dictKeysDataname,record['form_values'])

# Records sub functions
# Recursive search for keys to dataname
def search_datanames_keys_recu(dictKeysDataname,info):
  if isinstance(info, list):
    for v in info:
      if v:
        search_for_keys_recu(dictKeysDataname,v)
  elif isinstance(info, dict):
    for k in info.keys():
      if k in dictKeysDataname:
        info[dictKeysDataname[k]] = info.pop(k)
    for v in info.values():
      search_for_keys_recu(dictKeysDataname,v)

