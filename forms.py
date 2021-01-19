#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
import parameters as PA
import tools as TO
import tools_fulcrum_api as TOFA
import logs as LO

# System
import sys, os
import json

##############################################
# Forms = fulcrumapp in Fulcrum
##############################################

# OBJECTS
#########################
class Forms(object):
  def __init__(self):
    self.forms=[]
    self.formsDictID={}
    self.formsDictName={}
    self.formsDictIDName={}
    
  def __len__(self):
    return len(self.forms)
    
  def get_forms(self):
    return self.forms
  
  def __str__(self):
    tp = ""
    for form in self.forms:
      if tp:
        tp += '\n {}'.format(form)
      else:
        tp = '{}'.format(form)
    return tp

  def to_csv(self):
    tp = []
    for form in self.forms:
      tp.append(form.to_csv())
    return tp
  
  def add_form(self,form):
    self.forms.append(form)
    self.formsDictID[form.id]=form
    self.formsDictName[form.name]=form
    self.formsDictIDName[form.id]=form.name

  def backup_forms(self):
    for form in self.forms[:]:
      form.backup_form()


class Form(object):
  def __init__(self, assignment_enabled = '', auto_assign = '', bounding_box = '', created_at = '', description = '', dictKeysDataName = '', elements = '', geometry_required = '', geometry_types = '', hidden_on_dashboard = '', ID = '', image = '', image_large = '', image_small = '', image_thumbnail = '', name = '', name_cleaned = '', projects_enabled = '', record_count = '', record_title_key = '', script = '', status_field = '', title_field_keys = '', updated_at = '', version = '', backup_file = ''):
    self.assignment_enabled = assignment_enabled
    self.auto_assign = auto_assign
    self.bounding_box = bounding_box
    self.created_at = created_at
    self.description = description
    self.dictKeysDataName= dictKeysDataName
    self.dictDataNameKeys= {}
    self.backup_file = backup_file
    self.elements = elements
    self.geometry_required = geometry_required
    self.geometry_types = geometry_types
    self.hidden_on_dashboard = hidden_on_dashboard
    self.id = ID
    self.image = image
    self.image_large = image_large
    self.image_small = image_small
    self.image_thumbnail = image_thumbnail
    self.name = name
    self.name_cleaned = name_cleaned
    self.projects_enabled = projects_enabled
    self.record_count = record_count
    self.record_title_key = record_title_key
    self.script = script
    self.status_field = status_field
    self.title_field_keys = title_field_keys
    self.updated_at = updated_at
    self.version = version
    self.logInfo = ""
    self.isValid = True

  def __str__(self):
    return '>{} - {}'.format(self.id, self.name)

  def to_csv(self):
    return []

  def to_info(self):
    return []

  def whoami(self):
    print type(self).__name__
    
  def is_form(self):
    if self.id and self.name:
      return True
    else:
      LO.l_war('The form has no ID and/or name. We will not be able to process it.')
      self.add_toLog('The form has no ID and/or name. We will not be able to process it.')
      self.isValid = False
      return False
      
  def add_toLog(self, st):
    self.logInfo += "\n"+st
  
  def set_KeysDataName(self):
    if len(self.dictKeysDataName)<1:
      dictKeysDataName = {}
      search_for_keys_form_recu(dictKeysDataName,self.elements)
      self.dictKeysDataName = dictKeysDataName
      st = 'The form {} has now a dictKeysDataName'.format(self.name_cleaned)
      LO.l_debug(st)
      self.add_toLog(st)

  def set_dictDataNameKeys(self):
    if len(self.dictKeysDataName)>0:
      self.dictDataNameKeys = from_DataName_to_Keys(self.dictKeysDataName)
      st = 'The form {} has now a dictDataNameKeys'.format(self.name_cleaned)
      LO.l_debug(st)
      self.add_toLog(st)

  def set_NameCleaned(self):
    if not self.name_cleaned:
      self.name_cleaned = TO.clean_name(self.name)
    
  # Extract Forms
  def backup_form(self):
    formName = self.name_cleaned
    # Create directories for formName
    create_form_directories(formName)
    fname = TO.get_FormsPath()+formName+'/'+formName+'_form.json'
    LO.l_debug('The form file name is {}'.format(fname))
    self.add_toLog('The form file name is {}'.format(fname))
    self.backup_file = fname
    TO.save_in_json_file(fname,self.__dict__)
    LO.l_debug('The form {} is saved'.format(formName))
    self.add_toLog('The form {} is saved'.format(formName))
    # Create forms uid
    create_form_uid_directories()
    fname = TO.get_FormsPath()+"uid"+'/'+self.id+'_form.json'
    TO.save_in_json_file(fname,self.__dict__)
    LO.l_debug('The form uid {} is saved'.format(formName))
    self.add_toLog('The form uid {} is saved'.format(formName))


# Forms sub functions
# Recursive search for keys to dataname
def search_for_keys_form_recu(dictKeysDataName,info):
  if isinstance(info, list):
    for v in info:
      if v:
        search_for_keys_form_recu(dictKeysDataName,v)
  elif isinstance(info, dict):
    if 'elements' in info:
      search_for_keys_form_recu(dictKeysDataName,info['elements'])
    if 'data_name' in info and 'key' in info:
      dictKeysDataName[info['key']]=info['data_name']
    for vs in info.values():
      if isinstance(vs, list):
        for v in vs:
          if v:
            search_for_keys_form_recu(dictKeysDataName,v)

def create_form_directories(formName):
  directories = ['versions', 'images']
  for directory in directories:
    directory = TO.get_FormsPath()+formName+'/'+directory
    if not os.path.exists(directory):
      os.makedirs(directory)

def create_form_uid_directories():
  directory = TO.get_FormsPath()+"uid"+'/'
  if not os.path.exists(directory):
    os.makedirs(directory)


def from_DataName_to_Keys(dictKeysDataName):
  dictDataNameKeys = {}
  for k in dictKeysDataName.keys():
    dictDataNameKeys[dictKeysDataName[k]] = k
  return dictDataNameKeys

##############################################
# Forms Functions
##############################################
def create_form_from_json(form_raw):
  assignment_enabled, auto_assign, bounding_box, created_at, description, dictKeysDataName, elements, geometry_required, geometry_types, hidden_on_dashboard, ID, image, image_large, image_small, image_thumbnail, name, name_cleaned, projects_enabled, record_count, record_title_key, script, status_field, title_field_keys, updated_at, version, backup_file = ("",)*26
  if 'assignment_enabled' in form_raw:  assignment_enabled = form_raw['assignment_enabled']
  if 'auto_assign'        in form_raw:  auto_assign = form_raw['auto_assign']
  if 'bounding_box'       in form_raw:  bounding_box = form_raw['bounding_box']
  if 'backup_file'        in form_raw:  backup_file = form_raw['backup_file']
  if 'created_at'         in form_raw:  created_at = form_raw['created_at']
  if 'description'        in form_raw:  description = form_raw['description']
  if 'dictKeysDataName'   in form_raw:  dictKeysDataName = form_raw['dictKeysDataName']
  if 'elements'           in form_raw:  elements = form_raw['elements']
  if 'geometry_required'  in form_raw:  geometry_required = form_raw['geometry_required']
  if 'geometry_types'     in form_raw:  geometry_types = form_raw['geometry_types']
  if 'hidden_on_dashboard' in form_raw:  hidden_on_dashboard = form_raw['hidden_on_dashboard']
  if 'id'                 in form_raw:  ID = form_raw['id']
  if 'image'              in form_raw:  image = form_raw['image']
  if 'image_large'        in form_raw:  image_large = form_raw['image_large']
  if 'image_small'        in form_raw:  image_small = form_raw['image_small']
  if 'image_thumbnail'    in form_raw:  image_thumbnail = form_raw['image_thumbnail']
  if 'name'               in form_raw:  name = form_raw['name']
  if 'name_cleaned'       in form_raw:  name_cleaned = form_raw['name_cleaned']
  if 'projects_enabled'   in form_raw:  projects_enabled = form_raw['projects_enabled']
  if 'record_count'       in form_raw:  record_count = form_raw['record_count']
  if 'record_title_key'   in form_raw:  record_title_key = form_raw['record_title_key']
  if 'script'             in form_raw:  script = form_raw['script']
  if 'status_field'       in form_raw:  status_field = form_raw['status_field']
  if 'title_field_keys'   in form_raw:  title_field_keys = form_raw['title_field_keys']
  if 'updated_at'         in form_raw:  updated_at = form_raw['updated_at']
  if 'version'            in form_raw:  version = form_raw['version']
  form = Form(assignment_enabled, auto_assign, bounding_box, created_at, description, dictKeysDataName, elements, geometry_required, geometry_types, hidden_on_dashboard, ID, image, image_large, image_small, image_thumbnail, name, name_cleaned, projects_enabled, record_count, record_title_key, script, status_field, title_field_keys, updated_at, version, backup_file)
  form.set_NameCleaned()
  form.set_KeysDataName()
  form.set_dictDataNameKeys()
  return form

def backup_fulcrum_forms(formsJson):
  TO.save_in_json_file(TO.get_FormsFile(),formsJson)

def get_forms_from_form_files_list(formFiles):
  forms = Forms()
  for formFile in formFiles:
    form = get_form_from_fileName(formFile)
    if form:
      forms.add_form(form)
  return forms

def get_form_from_fileName(fileName):
  form_raw = TO.load_json_file(fileName)
  return create_form_from_json(form_raw)


def get_forms_from_formsJson(formsJson):
  forms = Forms()
  for form_raw in formsJson:
    form = create_form_from_json(form_raw)
    forms.add_form(form)
  return forms

def get_dictKeysDataName_from_formid(form_id):
  fs = load_forms()
  if form_id in fs.formsDictID:
    return fs.formsDictID[form_id].dictKeysDataName

def get_formName_from_formid(form_id,fs=[],n=0):
  if isinstance(fs, Forms):
    if form_id in fs.formsDictIDName:
      return fs.formsDictIDName[form_id]
  elif len(fs)<1 and n<1:
    return get_formName_from_formid(form_id,load_forms(),1)
  else:
    return ""

def get_projects_enabled_status(form_id,fs=[],n=0):
  if isinstance(fs, Forms):
    if form_id in fs.formsDictID:
      return fs.formsDictID[form_id].projects_enabled
  elif len(fs)<1 and n<1:
    return get_projects_enabled_status(form_id,load_forms(),1)
  LO.l_war('get_projects_enabled_status : The form {} was not found in formsDictID'.format(form_id))
  return ""

def get_Keys_from_DataNames(formId, dataNames = []):
  forms = load_forms()
  form = forms.formsDictID[formId]
  keyValues = {}
  for dataName in dataNames[:]:
    if dataName in form.dictDataNameKeys:
      keyValues[dataName] = form.dictDataNameKeys[dataName]
  return keyValues

def get_Keys_from_formId(formId):
  forms = load_forms()
  form = forms.formsDictID[formId]
  keyValues = {}
  for dataName in dataNames[:]:
    if dataName in form.dictDataNameKeys:
      keyValues[dataName] = form.dictDataNameKeys[dataName]
  return keyValues

##############################################
# LOAD SOURCES
##############################################

# Load from Webhooks
def load_webhook_forms():
  webhookForms = TO.get_files_from_path(TO.get_WebhookFormsPath())
  return get_forms_from_form_files_list(webhookForms)

# Load from File Name
def load_forms_from_json_file(fileName):
  formsJson = TO.load_json_file(fileName)
  return get_forms_from_formsJson(formsJson)

# Load from File Name
def load_form_from_json_file(fileName):
  form_raw = TO.load_json_file(fileName)
  return create_form_from_json(form_raw)

# Load from Fulcrum
def load_form_from_fulcrum():
  return TOFA.get_fulcrum_forms()

# Load Forms From Backuped File
def load_backuped_json_forms():
  backupedFiles = TO.get_files_from_path_recu_with_eof(TO.get_FormsPath(),'_form.json')
  return get_forms_from_form_files_list(backupedFiles)

# Load Forms in json
def load_fulcrum_formsJson():
  formsJson = load_form_from_fulcrum()
  backup_fulcrum_forms(formsJson)
  fs = get_forms_from_formsJson(formsJson)
  fs.backup_forms()
  return fs
  
# Load Forms
def load_forms():
  fs = load_backuped_json_forms()
  if len(fs.forms) < 1:
    fs = load_fulcrum_formsJson()
  return fs
