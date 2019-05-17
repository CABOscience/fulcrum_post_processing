#!/usr/bin/env python
# -*- coding: utf-8 -*-
import parameters as PA
import logs as LO
# System
import io, os, sys
# files
import csv, codecs, cStringIO, json
# Spectroscopy
#import specdal
# Data Science
import pandas as pd
import numpy as np
np.set_printoptions(threshold='nan')
import urllib3
import fulcrum
from fulcrum import Fulcrum
from fulcrum.exceptions import NotFoundException, InvalidAPIVersionException, UnauthorizedException, InternalServerErrorException, RateLimitExceededException

import requests
#from packaging import version
from pkg_resources import parse_version as ParseVersion

'''
# For packaging and version
$ sudo apt install python-setuptools

FULCRUM API

Command lines to install fulcrum api
$ sudo apt-get update
$ sudo apt-get install git
$ git clone https://github.com/fulcrumapp/fulcrum-python.git
$ cd fulcrum-python/
$ python setup.py build
$ sudo python setup.py install

Object:
fulcrumApp = connection to fulcrum
forms      = [] a json like https://developer.fulcrumapp.com/endpoints/forms/#form-properties
records    = [] a json like https://developer.fulcrumapp.com/endpoints/records/#record-properties
images     = [] a json like https://developer.fulcrumapp.com/endpoints/photos/#photo-properties

It saves logs in a subdirectory ./logs/ 

It creates 4 types of fulcrum backups :
- two types of fulcrum backups (with and without version)
- two types of fulcrum backups (with and without dataname)

Structure of a saved form:
[fulcrumPath]/form-name
[fulcrumPath]/form-name/images
[fulcrumPath]/form-name/versions

'''
NumberOfRequest   = 0

##############################################
# Tools fulcrum api
##############################################

def get_fulcrum_version():
  return fulcrum.__version__
  
def check_fulcrum_version():
  if ParseVersion(PA.FulcrumVersion) == ParseVersion(get_fulcrum_version()):
    return True
  else:
    if ParseVersion(PA.FulcrumVersion) < ParseVersion(get_fulcrum_version()):
      LO.l_war('Your fulcrum version is more advanced than requiered (Need: {} vs Current: {}). Hope legacy is working'.format(PA.FulcrumVersion,get_fulcrum_version()))
    if ParseVersion(PA.FulcrumVersion) > ParseVersion(get_fulcrum_version()):
      LO.l_war('Your fulcrum version need to be updated (Need: {} vs Current: {}). Hope all function are already there.'.format(PA.FulcrumVersion,get_fulcrum_version()))

def exception_api(e,s):
  if isinstance(e, NotFoundException):
    LO.l_war('{} {}'.format(s,PA.NotFoundStr))
  elif isinstance(e, RateLimitExceededException):
    LO.l_err('{} {}'.format(s,PA.LimitExceededStr))
    print_num_of_request()
  else:
    LO.l_err('The error is:\n{}'.format(s))
  return False

#
# Fulcrum functions
#
def get_fulcrum_access():
  return Fulcrum(key=PA.FulcrumApiKey)
  
def test_fulcrum_access():
  fulcrumApp  = get_fulcrum_access()
  s = 'Search in Fulcrum by forms has failed'
  try:
    fulcrumApp.forms.search()['forms']
    return True
  except (UnauthorizedException,
          InvalidAPIVersionException,
          InternalServerErrorException
          ):
    if not PA.FulcrumApiKey:
      print("A Fulcrum API is needed")
      print parser.print_help()
    else:
      t = 'Connexion to Fulcrum has failed due to'
      endString = ''
      if UnauthorizedException:
        endString = 'unauthorized API Key.'
      elif InvalidAPIVersionException:
        endString = 'invalid API version.'
      elif InternalServerErrorException:
        endString = 'internal server error.'
      print(t+' '+endString)
    sys.exit(1)
  except NotFoundException as n:
    print('{} {}'.format(s,PA.NotFoundStr))
    sys.exit(1)
  except RateLimitExceededException as r:
    print('{} {}'.format(s,PA.LimitExceededStr))
    sys.exit(1)

# get forms
def get_fulcrum_forms(logName="main"):
  try:
    fulcrumApp = get_fulcrum_access()
    formsTmp = fulcrumApp.forms.search()['forms']
    increase_num_of_request_by(1)
    forms = []
    
    if PA.FulcrumForms:
      for form in formsTmp[:]:
        for fulcrumForm in PA.FulcrumForms:
          if form['id'] == fulcrumForm:
            forms.append(form)
          if form['name'] == fulcrumForm:
            forms.append(form)
    else:
      for form in formsTmp[:]:
        forms.append(form)
      
    LO.l_info('The number of backuped forms will be {}'.format(len(forms)))
    return forms
  except (NotFoundException, RateLimitExceededException) as e:
    s = 'Search forms has failed'
    exception_api(e,s)
    sys.exit(1)


def find_forms_from_ID(formID,logName="main"):
  try:
    fulcrumApp = get_fulcrum_access()
    formjson = fulcrumApp.forms.find(formID)
    increase_num_of_request_by(1)
    return formjson
  except (NotFoundException, RateLimitExceededException) as e:
    s = 'Search project has failed for project {}'.format(formID)
    return exception_api(e,s)

# get records from a form
def get_fulcrum_records(formID,formName,logName="main"):
  try:
    fulcrumApp = get_fulcrum_access()
    records = fulcrumApp.records.search(url_params={'form_id': formID})['records']
    increase_num_of_request_by(1)
    return records
  except (NotFoundException, RateLimitExceededException) as e:
    s = 'Search records has failed for form {}'.format(formName)
    return exception_api(e,s)
    
def get_record_history_2(recordID,logName="main"):
  url = FulcrumApiURL+'/records/'+recordID+'/history.json?token='+FulcrumApiKey
  r = requests.get(url)

  if '200' in str(r):
    increase_num_of_request_by(1)
    return r.json()['records']
  else:
    LO.l_war('The version request has not working for {}'.format(recordID))
    return []

def get_record_history(recordID,logName="main"):
  try:
    fulcrumApp = get_fulcrum_access()
    record_history = fulcrumApp.records.history(recordID)['records']
    increase_num_of_request_by(1)
    return record_history
  except (NotFoundException, RateLimitExceededException) as e:
    s = 'Search records has failed for form {}'.format(formName)
    return exception_api(e,s)

def find_project_from_project_ID(projectID,logName="main"):
  try:
    fulcrumApp = get_fulcrum_access()
    project = fulcrumApp.projects.find(projectID)
    increase_num_of_request_by(1)
    return project
  except (NotFoundException, RateLimitExceededException) as e:
    s = 'Search project has failed for project {}'.format(projectID)
    return exception_api(e,s)
 
def get_projects(logName="main"):
  try:
    fulcrumApp = get_fulcrum_access()
    projects = fulcrumApp.projects.search()['projects']
    increase_num_of_request_by(1)
    return projects
  except (NotFoundException, RateLimitExceededException) as e:
    s = 'Search projects has failed'
    return exception_api(e,s)

def donwload_photo_meta(fname,fulcrumApp,photoID,logName="main"):
  url = FulcrumApiURL+'/photos/'+photoID+'.json?token='+FulcrumApiKey
  r = requests.get(url)
  increase_num_of_request_by(1)
  
  if '200' in str(r):
    return r.json()["photo"]
  else:
    LO.l_war('The metadata request has not working for photo {}'.format(photoID))
    return []

def get_photo_meta(photoID,logName="main"):
  try:
    fulcrumApp = get_fulcrum_access()
    record_history = fulcrumApp.photos.find(photoID)['photo']
    increase_num_of_request_by(1)
    return record_history
  except (NotFoundException, RateLimitExceededException) as e:
    s = 'Search Photos Meta has failed for form {}'.format(formName)
    return exception_api(e,s)

def get_photo_file(photoID,logName="main"):
  try:
    fulcrumApp = get_fulcrum_access()
    photo = fulcrumApp.photos.media(photoID)
    increase_num_of_request_by(1)
    return photo
  except (NotFoundException, RateLimitExceededException) as e:
    s = 'Search photos has failed for photo id {}'.format(photoID)
    return exception_api(e,s)



##############################################
# Request
##############################################
def increase_num_of_request_by(n):
  if not n:
    n = 1
  global NumberOfRequest
  NumberOfRequest += n
  
def print_num_of_request(logName="main"):
  s = 'the number of request is {}'.format(NumberOfRequest)
  LO.l_info(s,logName)

