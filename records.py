#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
import parameters as PA
import forms as FO
import photos as PH
import projects as PR
import tools as TO
import tools_fulcrum_api as TOFA
import tools_db as TDB
import logs as LO
from psycopg2.extensions import AsIs


# System
import sys, copy, time
import multiprocessing as mp

##############################################
# Record
##############################################

# OBJECTS
#########################
class Records(object):
  def __init__(self):
    self.records=[]
    self.recordsInvalid=[]
    self.recordsDict={}
    self.cleanAfter=3000
    self.numCleaned=0
    self.ttCount=0
    
  def __len__(self):
    return len(self.records)
    
  def get_records(self):
    return self.records
  
  def __str__(self):
    tp = ""
    for record in self.records:
      print(record)
      '''
      if tp:
        tp += '\n{}'.format(record)
      else:
        tp = record
      '''
    return tp

  def to_csv(self):
    tp = []
    for record in self.records:
      tp.append(record.to_csv())
    return tp
  
  def add_record(self,record_raw):
    if record_raw.isValid:
      if record_raw.id in self.recordsDict:
        # check the version keep only the latest
        savedRec = self.recordsDict[record_raw.id]
        if savedRec.version < record_raw.version:
          # you keep record_raw
          # you have to change the version and remove it from table
          self.recordsDict[record_raw.id] = record_raw
          self.records.remove(savedRec)
          self.records.append(record_raw)
      else:
        self.records.append(record_raw)
        self.recordsDict[record_raw.id]=record_raw
    else:
      self.recordsInvalid.append(record_raw)

  def append_record(self,record_raw):
    if record_raw.isValid:
      self.records.append(record_raw)
    else:
      self.recordsInvalid.append(record_raw)
  
  def number_of_valid(self):
    number_of_valid = 0
    for rec in self.records[:]:
      if rec.isValid:
        number_of_valid = number_of_valid + 1
    return number_of_valid
    
  def clean_records(self):
    self.records = []
    self.recordsDict = {}
    
  def to_json(self):
    return [rec.__dict__ for rec in self.records[:]]


class Record(object):
  def __init__(self, Raltitude= "", RassignedTo= "", RassignedToId= "", RclientCreatedAt= "", RclientUpdatedAt= "", Rcourse= "", RcreatedAt= "", RcreatedBy= "", RcreatedById= "", RcreatedDuration= "", RcreatedLocation= "", ReditedDuration= "", RformId= "", RformName= "", RformValues= "", RhorizontalAccuracy= "", RID= "", Rlatitude= "", Rlongitude= "", RprojectId= "", Rspeed= "", Rstatus= "", RupdatedAt= "", RupdatedBy= "", RupdatedById= "", RupdatedDuration= "", RupdatedLocation= "", Rversion= "", RverticalAccuracy= "", RprojectName=''):
    self.altitude = Raltitude
    self.gps_altitude = self.altitude
    self.assigned_to = RassignedTo
    self.assigned_to_id = RassignedToId
    self.client_created_at = RclientCreatedAt
    self.client_updated_at = RclientUpdatedAt
    self.course = Rcourse
    self.gps_course = self.course
    self.created_at = RcreatedAt
    self.created_by = RcreatedBy
    self.created_by_id = RcreatedById
    self.created_duration = RcreatedDuration
    self.created_location = RcreatedLocation
    self.edited_duration = ReditedDuration
    self.form_id = RformId
    self.form_name = RformName
    self.form_values = RformValues
    self.horizontal_accuracy = RhorizontalAccuracy
    self.gps_horizontal_accuracy = self.horizontal_accuracy
    self.id = RID
    self.fulcrum_id = self.id
    self.latitude = Rlatitude
    self.longitude = Rlongitude
    self.project_id = RprojectId
    self.speed = Rspeed
    self.gps_speed = self.speed
    self.status = Rstatus
    self.updated_at = RupdatedAt
    self.updated_by = RupdatedBy
    self.updated_by_id = RupdatedById
    self.updated_duration = RupdatedDuration
    self.updated_location = RupdatedLocation
    self.version = Rversion
    self.vertical_accuracy = RverticalAccuracy
    self.gps_vertical_accuracy = self.vertical_accuracy
    self.project_name = RprojectName
    self.isValid = True
    self.logInfo = ""

  def __str__(self):
    return '>{}'.format(["altitude:",self.altitude,"gps_altitude:",self.gps_altitude,"assigned_to:",self.assigned_to,"assigned_to_id:",self.assigned_to_id,"client_created_at:",self.client_created_at,"client_updated_at:",self.client_updated_at,"course:",self.course,"gps_course:",self.gps_course,"created_at:",self.created_at,"created_by:",self.created_by,"created_by_id:",self.created_by_id,"created_duration:",self.created_duration,"created_location:",self.created_location,"edited_duration:",self.edited_duration,"form_id:",self.form_id,"form_name:",self.form_name,"form_values:",self.form_values,"horizontal_accuracy:",self.horizontal_accuracy,"gps_horizontal_accuracy:",self.gps_horizontal_accuracy,"id:",self.id,"fulcrum_id:",self.fulcrum_id,"latitude:",self.latitude,"longitude:",self.longitude,"project_id:",self.project_id,"speed:",self.speed,"gps_speed:",self.gps_speed,"status:",self.status,"updated_at:",self.updated_at,"updated_by:",self.updated_by,"updated_by_id:",self.updated_by_id,"updated_duration:",self.updated_duration,"updated_location:",self.updated_location,"version:",self.version,"vertical_accuracy:",self.vertical_accuracy,"gps_vertical_accuracy:",self.gps_vertical_accuracy,"project_name:",self.project_name,"isValid:",self.isValid,"logInfo:",self.logInfo])

  def to_csv(self):
    return [self.altitude, self.assigned_to, self.assigned_to_id, self.client_created_at, self.client_updated_at, self.course, self.created_at, self.created_by, self.created_by_id, self.created_duration, self.created_location, self.edited_duration, self.form_id, self.horizontal_accuracy, self.id, self.latitude, self.longitude, self.project_id, self.speed, self.status, self.updated_at, self.updated_by, self.updated_by_id, self.updated_duration, self.updated_location, self.version, self.vertical_accuracy]

  def to_info(self):
    return []

  def whoami(self):
    print(type(self).__name__)
    
  def is_record(self):
    if self.id and self.form_id:
      return True
    else:
      LO.l_debug('The record has no ID ({}) and/or "form_id" ({}). We will not be able to process it.'.format(self.id,self.form_id))
      self.add_toLog('The record has no ID ({}) and/or "form_id" ({}). We will not be able to process it.'.format(self.id,self.form_id))
      return False
      
  def add_toLog(self, st):
    self.logInfo += "\n"+st

  def is_record_has_project(self):
    if (self.project_id == '') or (self.project_id is None):
      self.isValid = False
      LO.l_war('The record id {} will not be used because it has no associated project.'.format(self.id))
      self.add_toLog('The record id {} will not be used because it has no associated project.'.format(self.id))
      return False
    return True
  
  def to_json(self):
    #return json.dumps(self.__dict__)
    return self.__dict__


##############################################
# Records Functions
##############################################
def create_record(record_raw,forms=[],projects=[]):
  Raltitude, RassignedTo, RassignedToId, RclientCreatedAt, RclientUpdatedAt, Rcourse, RcreatedAt, RcreatedBy, RcreatedById, RcreatedDuration, RcreatedLocation, ReditedDuration, RformId, RformName, RhorizontalAccuracy, RID, Rlatitude, Rlongitude, RprojectId, Rspeed, Rstatus, RupdatedAt, RupdatedBy, RupdatedById, RupdatedDuration, RupdatedLocation, Rversion, RverticalAccuracy, RformValues, RprojectName = ("",)*30
  if 'altitude'           in record_raw:  Raltitude = record_raw['altitude']
  if 'assigned_to'        in record_raw:  RassignedTo = record_raw['assigned_to']
  if 'assigned_to_id'     in record_raw:  RassignedToId = record_raw['assigned_to_id']
  if 'client_created_at'  in record_raw:  RclientCreatedAt = record_raw['client_created_at']
  if 'client_updated_at'  in record_raw:  RclientUpdatedAt = record_raw['client_updated_at']
  if 'course'             in record_raw:  Rcourse = record_raw['course']
  if 'created_at'         in record_raw:  RcreatedAt = record_raw['created_at']
  if 'created_by'         in record_raw:  RcreatedBy = record_raw['created_by']
  if 'created_by_id'      in record_raw:  RcreatedById = record_raw['created_by_id']
  if 'created_duration'   in record_raw:  RcreatedDuration = record_raw['created_duration']
  if 'created_location'   in record_raw:  RcreatedLocation = record_raw['created_location']
  if 'edited_duration'    in record_raw:  ReditedDuration = record_raw['edited_duration']
  if 'form_id'            in record_raw:
    RformId = record_raw['form_id']
    RformName = FO.get_formName_from_formid(RformId,forms)
  if 'form_values'        in record_raw:  RformValues = record_raw['form_values']
  if 'horizontal_accuracy' in record_raw: RhorizontalAccuracy = record_raw['horizontal_accuracy']
  if 'id'                 in record_raw:  RID = record_raw['id']
  if 'latitude'           in record_raw:  Rlatitude = record_raw['latitude']
  if 'longitude'          in record_raw:  Rlongitude = record_raw['longitude']
  if 'project_id'         in record_raw:  RprojectId = record_raw['project_id']
  if 'speed'              in record_raw:  Rspeed = record_raw['speed']
  if 'status'             in record_raw:  Rstatus = record_raw['status']
  if 'updated_at'         in record_raw:  RupdatedAt = record_raw['updated_at']
  if 'updated_by'         in record_raw:  RupdatedBy = record_raw['updated_by']
  if 'updated_by_id'      in record_raw:  RupdatedById = record_raw['updated_by_id']
  if 'updated_duration'   in record_raw:  RupdatedDuration = record_raw['updated_duration']
  if 'updated_location'   in record_raw:  RupdatedLocation = record_raw['updated_location']
  if 'version'            in record_raw:  Rversion = record_raw['version']
  if 'vertical_accuracy'  in record_raw:  RverticalAccuracy = record_raw['vertical_accuracy']
  
  record = Record(Raltitude, RassignedTo, RassignedToId, RclientCreatedAt, RclientUpdatedAt, Rcourse, RcreatedAt, RcreatedBy, RcreatedById, RcreatedDuration, RcreatedLocation, ReditedDuration, RformId, RformName, RformValues, RhorizontalAccuracy, RID, Rlatitude, Rlongitude, RprojectId, Rspeed, Rstatus, RupdatedAt, RupdatedBy, RupdatedById, RupdatedDuration, RupdatedLocation, Rversion, RverticalAccuracy,RprojectName)
  
  if not RID and not RformId:
    LO.l_debug('record_raw')
    LO.l_debug(record_raw)
  
  LO.l_debug('The record id is :{}'.format(RID))
  
  if not RID and not RformId:
    LO.l_debug('The record is not valid. Record Values:\n{}'.format(record))
    record.isValid=False
  else:
    is_form_project_enabled = FO.get_projects_enabled_status(record.form_id,forms)
    if is_form_project_enabled:
      record.project_name = PR.get_project_name_from_id(record.project_id,projects)
      if record.project_name == "":
        sNoP = 'Form id {} (name: {}), The record id {} is not associated project name with a project name and it has the project id {}.'.format(record.form_id, record.form_name,record.id,record.project_id)
        LO.l_war(sNoP)
        record.add_toLog(sNoP)
      else:
        LO.l_debug('Form id {} (name: {}), The record id "{}" has an associated project name with a project name ({}) and id ({}).'.format(record.form_id, record.form_name, record.id,record.project_name, record.project_id))
    else:
      LO.l_debug('Form id {} (name: {}) has not its project enabled.'.format(record.form_id, record.form_name,record.id,record.project_id))
    
    if Rstatus and 'deleted' in Rstatus:
      sdel = 'Form id {} (name: {}), Project id {} (name: {}), the record id {} will not be used because its status is deleted.'.format(record.form_id, record.form_name,record.project_id,record.project_name,record.id)
      LO.l_err(sdel)
      record.add_toLog(sdel)
      record.isValid=False
  return record

def get_records_from_files_list(listFileRecords):
  records = Records()
  for fileRecord in listFileRecords:
    record_raw = record_from_fileName(fileRecord)
    if record_raw.isValid:
      records.add_record(record_raw)
  return records

def record_from_fileName(fileName):
  record_raw = TO.load_json_file(fileName)
  return create_record(record_raw)

def get_list_records_from_file(fileName):
  return TO.load_json_file(fileName)

def get_record_from_raw_record(record_raw,forms=[],projects=[]):
  if len(projects)<1:
    projects = PR.load_projects()
  if len(forms)<1:
    forms = FO.load_forms()
  return create_record(record_raw,forms,projects)

def get_records_from_list(listRecords,forms=[],projects=[]):
  # preload projects and forms if they are empty
  if len(projects)<1:
    projects = PR.load_projects()
  if len(forms)<1:
    forms = FO.load_forms()
  records = Records()
  for record_raw in listRecords[:]:
    record = create_record(record_raw,forms,projects)
    if (PR.test_if_project_id(record.project_id,projects)) or (not record.project_id):
      records.add_record(record)
  return records

##############################################
# Backup Records latest version From Forms
##############################################
def backup_records_from_fulcrumforms():
  # Backup projects
  PR.backup_projects_from_Fulcrum()
  # Backup Forms (Applications)
  formsO = FO.load_fulcrum_formsJson()
  #for form in formsO.forms[:]:
  #  mp_backup_records_from_form(form)
  mp_backup_records_from_forms(formsO)
  TOFA.print_num_of_request()

def backup_records_from_webhookforms():
  # Backup projects
  PR.backup_projects_from_Fulcrum()
  # Backup Forms (Applications)
  load = FO.load_webhook_forms()
  webhookForms = load[0]
  webhookFiles = load[1]
  for form in formsO.forms[:]:
    mp_backup_records_from_form(form)
  #mp_backup_records_from_forms(webhookForms)
  TOFA.print_num_of_request()
  if len(webhookFiles) > 0:
    for f in webhookFiles:
      TO.delete_a_file(f)

def mp_backup_records_from_forms(formsO = FO.Forms()):
  """
  This parallelisation of backup_form
  """
  wraps = []
  if PA.IsParallel == 'True':
    LO.l_debug("mp_backup_records_from_forms parallelisation")
    output = mp.Queue()
    pool = mp.Pool(processes=PA.NumberOfProcesses)
    results = [pool.apply_async(mp_backup_records_from_form, args=(form_raw,)) for form_raw in formsO.forms[:]]
    pool.close()
    pool.join()
    for r in results:
      record = r.get()
      if record:
        wraps.append(record)
  else:
    LO.l_debug("mp_backup_records_from_forms linear")
    for form_raw in formsO.forms[:]:
      record = mp_backup_records_from_form(form_raw)
      if record:
        wraps.append(record)
  return wraps

def mp_backup_records_from_form(form = FO.Form()):
  formName = form.fulcrum_name_cleaned
  formID   = form.id
  start = time.time()
  if formID:
    # Backup records
    LO.l_info('Start backup for the form "{}" with {} records'.format(formName,form.record_count))
    records = load_records_from_fulcrum(form)
    fbase = TO.get_FormsPath()+formName+'/'
    # Backup raw records 
    fname = fbase+formName+'_records.json'
    dirRecs = fbase+'records/'
    TO.create_directory(dirRecs)
    
    TO.save_in_json_file(fname,records.to_json())
    for rec in records.records[:]:
      recName = dirRecs+rec.id+'.json'
      TO.save_in_json_file(recName,rec.to_json())
    
    # Backup records with datanames
    update_records_with_dataname(form.dictKeysDataName,records.records)
    fname = fbase+'_records_with_dataname.json'
    TO.save_in_json_file(fname,records.to_json())
    for rec in records.records[:]:
      recName = dirRecs+rec.id+'_with_dataname.json'
      TO.save_in_json_file(recName,rec.to_json())
    
    LO.l_info('End backup for the form "{}", there are {} records available'.format(formName,len(records)))

    # Backup images
    LO.l_info('Start backup images for the form "{}" with {} records'.format(formName,len(records)))
    PH.backup_photos_from_records(form,records)
    LO.l_info('End backup images for the form "{}"'.format(formName))

    endtime = time.time()
    print(('########################\nTime to backup form {} ({}) IS {}\n########################\n'.format(formName,formID,endtime-start)))

    return formID

##############################################
# Clean Webhook Records
##############################################
def clean_webhook_records(records):
  for rec in records[:]:
    fname = TO.get_WebhookRecordsPath()+''+rec.id+''
    boo = TO.delete_a_file(fname)
    if boo:
      LO.l_info('The file {} has been deleted'.format(fname))
    else:
      LO.l_err('The file {} has NOT been deleted'.format(fname))

##############################################
# Backup Records Versions From Forms
##############################################
def backup_records_versions_from_forms():
  PA.set_parameters()
  LO.create_log('backup_fulcrum_versions')
  TOFA.check_fulcrum_version()
  # Backup projects
  PR.backup_projects_from_Fulcrum()
  # Backup Forms (Applications)
  formsO = FO.load_fulcrum_formsJson()
  for form in formsO.forms[:]:
    mp_backup_records_versions_from_form(form)
  #mp_backup_records_from_forms(formsO)
  TOFA.print_num_of_request()

def mp_backup_records_versions_from_forms(formsO = FO.Forms()):
  """
  This parallelisation of backup_form
  """
  wraps = []
  if PA.IsParallel == 'True':
    LO.l_debug("mp_backup_records_versions_from_form parallelisation")
    output = mp.Queue()
    pool = mp.Pool(processes=PA.NumberOfProcesses)
    results = [pool.apply_async(mp_backup_records_versions_from_form, args=(form_raw,)) for form_raw in formsO.forms[:]]
    pool.close()
    pool.join()
    for r in results:
      record = r.get()
      if record:
        wraps.append(record)
  else:
    LO.l_debug("mp_backup_records_versions_from_form linear")
    for form_raw in formsO.forms[:]:
      record = mp_backup_records_versions_from_form(form_raw)
      if record:
        wraps.append(record)
  return wraps

def mp_backup_records_versions_from_form(form = FO.Form()):
  formName = form.fulcrum_name_cleaned
  formID   = form.id
  start = time.time()
  if formID:
    # Backup records versions
    fbase = TO.get_FormsPath()+formName+'/'+formName
    # Backup raw records 
    fname = fbase+'_records.json'

    if form.script and '/* SAVE VERSIONS */' in form.script:
      bName = TO.get_FormsPath()+formName+''
      
      # preload projects and forms
      projects = PR.load_projects()
      forms = FO.load_forms()
      recs = load_records_from_json(fname)
      #recs = load_records_from_fulcrum(form)
      
      LO.l_info('Start backup version for the form "{}" with {} records'.format(formName,len(recs)))
      LO.l_debug('size of recs {} before version'.format(len(recs)))
      
      recordsV = Records()
      for record in list(recs.recordsDict.values()):
        currentVersion = record.version
        recordID      = record.id
        fname         = bName+'/versions/'+recordID+'_versions.json'
        recordsHistory= TO.load_json_file(fname)
        versionIsUpToDate = False

        if len(recordsHistory)>0:
          latestHistoryVersion = get_record_latest_history_version(recordsHistory)
          if (currentVersion == latestHistoryVersion):
            versionIsUpToDate = True
        
        if not versionIsUpToDate and currentVersion > 1:
          recordsHistory = TOFA.get_record_history(recordID)
          LO.l_debug('recordsHistory')
          LO.l_debug(len(recordsHistory))
          
        recordsV.append_record(record)
          
        if recordsHistory:
          TO.save_in_json_file(fname,recordsHistory)
          for recordHistoryTemp in recordsHistory[:]:
            recHT = create_record(recordHistoryTemp,forms,projects)
            if recHT.version != currentVersion:
              LO.l_debug('add_record {} version {}'.format(recHT.id,recHT.version))
              recordsV.append_record(recHT)
        
        if len(recordsV)>recordsV.cleanAfter:
          jocker = "w"
          if recordsV.numCleaned>0:
            jocker = "a"
          fname = fbase+'_records_versions.json'
          TO.save_in_json_file(fname,recordsV.to_json(),"main",jocker)
          
          fname = fbase+'_records_versions_with_dataname.json'
          update_records_with_dataname(form.dictKeysDataName,recordsV.records)
          TO.save_in_json_file(fname,recordsV.to_json(),"main",jocker)
          recordsV.ttCount += len(recordsV.records)
          recordsV.records[:] = []
          recordsV.numCleaned += 1
      
      jocker = "w"
      if recordsV.numCleaned>0:
        jocker = "a"
      
      fname = fbase+'_records_versions.json'
      TO.save_in_json_file(fname,recordsV.to_json(),"main",jocker)
      
      fname = fbase+'_records_versions_with_dataname.json'
      update_records_with_dataname(form.dictKeysDataName,recordsV.records)
      TO.save_in_json_file(fname,recordsV.to_json(),"main",jocker)
      
      recordsV.ttCount += len(recordsV.records)
      LO.l_info('End backup version for the form "{}", there are {} records available'.format(formName,recordsV.ttCount))
    else:
      LO.l_war("No records versions for {st} will not be saved.\n\
                If you need to saved records versions for {st}.\n\
                Please add /* SAVE VERSIONS */ in the top of it's 'data events'\n\
                ".format(st=formName))
    
    endtime = time.time()
    print(('########################\nTime to backup form {} ({}) IS {}\n########################\n'.format(formName,formID,endtime-start)))
    #return records
    return formID

# Record history
def get_record_latest_history_version(records):
  latestVersion = 0
  for record in records:
    if record['version'] > latestVersion:
      latestVersion = record['version']
  return latestVersion

##############################################
# Update Record with dataname
##############################################
def record_add_dataname_from_formFile(record,formFile):
  form_raw = FO.load_form_from_json_file(formFile)
  #dictKeysDataname = form_raw['dictKeysDataname']
  dictKeysDataname = form_raw.dictKeysDataName
  if 'form_values' in record:
    update_record_with_dataname(dictKeysDataname,record['form_values'])

# Records sub functions
# Recursive search for keys to dataname
def search_datanames_keys_recu(dictKeysDataname,info):
  if isinstance(info, list):
    for v in info:
      if v:
        search_for_keys_recu(dictKeysDataname,v)
  elif isinstance(info, dict):
    for k in list(info.keys()):
      if k in dictKeysDataname:
        info[dictKeysDataname[k]] = info.pop(k)
    for v in list(info.values()):
      search_for_keys_recu(dictKeysDataname,v)

def update_records_with_dataname_old(recs):
  recordsTemp = copy.deepcopy(recs.records)
  for recordTemp in recordsTemp:
    dictKeysDataName = FO.get_dictKeysDataName_from_formid(recordTemp.form_id)
    if recordTemp.form_values:
      search_for_keys_recu(dictKeysDataName,recordTemp.form_values)
  recs.clean_records()
  for recordTemp in recordsTemp:
    recs.add_record(recordTemp)

def update_records_with_dataname(dictKeysDataName,records):
  for record in records:
    if record.form_values:
      search_for_keys_recu(dictKeysDataName,record.form_values)

def update_record_with_dataname(dictKeysDataName,record):
  if record.form_values:
    search_for_keys_recu(dictKeysDataName,record.form_values)

# Records sub functions
# Recursive search for keys to dataname
def search_for_keys_recu(dictKeysDataName,info):
  if isinstance(info, list):
    for v in info:
      if v:
        search_for_keys_recu(dictKeysDataName,v)
  elif isinstance(info, dict):
    for k in list(info.keys()):
      if k in dictKeysDataName:
        info[dictKeysDataName[k]] = info.pop(k)
    for v in list(info.values()):
      search_for_keys_recu(dictKeysDataName,v)

def update_json_record_from_dataname_to_keys(record,recordjson):
  dataNameToKey = FO.get_Keys_from_formId(record.form_id)
  search_for_dataName_recu(dataNameToKey,recordjson)
  return recordjson
    
# Records sub functions
# Recursive search for keys to dataname
def search_for_dataName_recu(dataNameToKey,rjson):
  if isinstance(rjson, list):
    for v in rjson:
      if v:
        search_for_dataName_recu(dataNameToKey,v)
  elif isinstance(rjson, dict):
    for k in list(rjson.keys()):
      if k in dataNameToKey:
        info[dataNameToKey[k]] = info.pop(k)
    for v in list(rjson.values()):
      search_for_dataName_recu(dataNameToKey,v)

##############################################
# LOAD RECORDS
##############################################

# Error load
##############################################
def error_load(st):
  LO.l_err('The file {} is not available. A default empty Records will be loaded'.format(st))
  return Records()

# Load records from Webhooks
def load_webhook_records():
  records_files = TO.get_files_from_path(PA.FulcrumWebhook+"records/")
  return get_records_from_files_list(records_files)

def load_webhook_records_with_formID_from_formFile(formFile):
  recsTmp = load_webhook_records()
  recs = Records()
  if len(recsTmp)>0:
    formJson = TO.load_json_file(formFile)
    if 'id' in formJson:
      formId = formJson['id']
      for record in recsTmp.records[:]:
        if record.form_id == formId:
          recs.add_record(record)
  return recs

# Load records from File Name
##############################################
def load_records_from_json(fileName):
  records_raw = get_list_records_from_file(fileName)
  return get_records_from_list(records_raw)

# Load records from backup
# (very similar to previous one)
##############################################
def load_records_from_form(form):
  records_raw = get_list_records_from_file(form.backup_file)
  return get_records_from_list(records_raw)

# Load records from fulcrum
##############################################
def load_records_from_fulcrum(form):
  records_raw = TOFA.get_fulcrum_records(form.id,form.fulcrum_name_cleaned)
  if records_raw:
    return get_records_from_list(records_raw)
  else:
    return records()

##############################################
# RECORDS TO DATABASE
##############################################
def prepare_record_values(record):
  common_fields_sub = [
    "created_at", 
    "created_by", 
    "updated_at", 
    "updated_by", 
    "version", 
  ]

  common_fields_main = common_fields_sub + [
    "fulcrum_id",
    "assigned_to",
    "latitude",
    "longitude",
    "status",
    "gps_horizontal_accuracy",
    "gps_vertical_accuracy",
    "gps_speed",
    "gps_course",
    "gps_altitude"
  ]

  vals={}
  FF = FO.get_form_from_formid(record.form_id)
  recu_map_values(vals, TO.fulcrum_clean_name(FF.name), record.form_values, record, FF.dictKeysTypes, FF.dictKeysDataName, common_fields_main, common_fields_sub, 0)
  return vals

def recu_map_values(vals, tblName, values, record, keysTypes, keysDataNames, common_fields_main, common_fields_sub, id):
  kv = {}
  if id == 0: #The main form table
    for f in common_fields_main:
      kv[f] = getattr(record, f)
  else: # Sub tables
    kv["fulcrum_parent_id"] = record.id
    kv["fulcrum_record_id"] = record.id
    kv['fulcrum_id'] = id
    for f in common_fields_sub:
      kv[f] = getattr(record, f)
              
  for v in values:
    if v in keysTypes:
      if keysTypes[v] in ['TextField','CalculatedField','BarcodeField','Label','DateTimeField','YesNoField','TimeField','ClassificationField','HyperlinkField']:
        kv[keysDataNames[v]] = values[v]
      elif keysTypes[v] in ['RecordLinkField']:
        rf=[]
        for r in values[v]:
          rf.append(r['record_id'])
        kv[keysDataNames[v]] = ",".join(rf)
      elif keysTypes[v] in ['ChoiceField']:
        kv[keysDataNames[v]] = ",".join(values[v]['choice_values'])
      elif keysTypes[v] in ['Repeatable']:
        for rep in values[v]:
          recu_map_values(vals, tblName + '_' + keysDataNames[v], rep['form_values'], record, keysTypes, keysDataNames, common_fields_main, common_fields_sub, rep['id'])
      elif keysTypes[v] in ['PhotoField']:
        photos=[]
        captions=[]
        for p in values[v]:
          if p['photo_id'] is not None:
            photos.append(p['photo_id'])
          if p['caption'] is not None:
            captions.append(p['caption'])
        kv[keysDataNames[v]] = ",".join(photos)
        kv[keysDataNames[v]+"_caption"] = ",".join(captions)
    else:
      LO.l_war('WARNING FIELD {} NOT MAPPED! '.format(v))
  if tblName not in vals:
    vals[tblName]=[kv]
  else:
    vals[tblName].append(kv)


def check_record(conn, table, id):
  return TDB.query_to_db(conn, "SELECT fulcrum_id FROM %s WHERE fulcrum_id = %s", (AsIs(table),id))

def insert_record(values):
  conn = TDB.get_access_to_db()
  res = False
  if conn != None:
    for table in values:
      for r in values[table]:
        isdel=False
        if check_record(conn, table, r['fulcrum_id']):
          isdel = TDB.query_to_db(conn,"DELETE FROM %s WHERE fulcrum_id = %s", (AsIs(table),r['fulcrum_id']))
        columns = list(r.keys())
        val = [r[column] for column in columns]
        insert_statement = 'INSERT INTO %s (%s) VALUES %s'
        res = TDB.query_to_db(conn, insert_statement, (AsIs(table), AsIs(','.join(columns)), tuple(val)))
        if res and isdel:
          LO.l_debug('Record {} updated in DB'.format(r['fulcrum_id']))
        elif res:
          LO.l_debug('Record {} inserted in DB'.format(r['fulcrum_id']))
        else:
          LO.l_war('Error inserting Record {} in DB'.format(r['fulcrum_id']))
  else:
    LO.l_war('Could not connect to database')
  conn.close()
  return res

def record_webhook_to_db():
  recsTmp = load_webhook_records()
  if len(recsTmp)>0:
    leafSpectraForm = FO.load_form_from_json_file(PA.LeafSpectraFormFile)
    leafSpectraFormID = leafSpectraForm.id
    projects = PR.load_projects()
    forms = FO.load_forms()
    for recTmp in recsTmp.records[:]:
      rec_fulc = TOFA.get_record(recTmp.id)
      fname = TO.get_WebhookRecordsPath()+recTmp.id+''
      if rec_fulc:
        record = get_record_from_raw_record(rec_fulc,forms,projects)
        if record.isValid:
            res = insert_record(prepare_record_values(record))
            if not res:
              LO.l_info("Failed to update DB, File not deleted {}".format(fname))
            elif record.form_id in leafSpectraFormID:
              LO.l_info("File will be processed in leafspectra {}".format(fname))
            elif record.form_id not in leafSpectraFormID:
              LO.l_info("File to be deleted {}".format(fname))
              TO.delete_a_file(fname)
        else:
          LO.l_info("Unknown Error File will not be deleted {}".format(fname))
      else:
        LO.l_info("This record does not exist on fulcrum\nFile to be deleted {}".format(fname))
        TO.delete_a_file(fname)

    for recTmp in recsTmp.recordsInvalid[:]:
      fname = TO.get_WebhookRecordsPath()+recTmp.id+''
      LO.l_info("File (without a valid record) to be deleted {}".format(fname))
      TO.delete_a_file(fname)
  else:
    LO.l_info("No webhook record")
