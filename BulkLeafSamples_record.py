#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
import parameters as PA
import records as RE
import tools as TO
import logs as LO
import LeafSpectra_measurements as LSM
import SpectroscopyPanels_calibrations as SPC

# System
import os, sys
import multiprocessing as mp
# Data Science
import math
import pandas as pd
import numpy as np
np.set_printoptions(threshold=sys.maxsize)

##############################################
# Record
##############################################

# OBJECT
#########################

class BulkLeaveSamples(RE.Records):
  """ Leaf spectrum object
  Leaf spectrum object is containing a list of LeafSpectra Object
  """
  def add_record(self,BulkLeaveSample):
    self.records.append(BulkLeaveSample)

class BulkLeaveSample(RE.Record):
  """ Leaf spectra object
  Leaf spectra object is a Records + its form values
  """
  def __init__(self, record):
    super(BulkLeaveSample,self).__init__(record.altitude, record.assigned_to, record.assigned_to_id, record.client_created_at, record.client_updated_at, record.course, record.created_at, record.created_by, record.created_by_id, record.created_duration, record.created_location, record.edited_duration, record.form_id, record.form_values, record.horizontal_accuracy, record.id, record.latitude, record.longitude, record.project_id, record.speed, record.status, record.updated_at, record.updated_by, record.updated_by_id, record.updated_duration, record.updated_location, record.version, record.vertical_accuracy, record.project_name)
    self.fv_approbation = ''
    self.fv_approved_by = ''
    self.fv_data_quality_control = ''
    self.fv_date_approved = ''
    self.fv_date_deleted = ''
    self.fv_date_published = ''
    self.fv_date_rejected = ''
    self.fv_date_sampled = '' #
    self.fv_date_submitted = ''
    self.fv_date_verified = ''
    self.fv_deleted = ''
    self.fv_deleted_by = ''
    self.fv_filter_plot = ''
    self.fv_filter_plot_id = ''
    self.fv_filter_site = ''
    self.fv_filter_site_id = ''
    self.fv_hidden_variables = ''
    self.fv_number_of_rejections = ''
    self.fv_plant = '' #
    self.fv_plant_id = ''
    self.fv_plant_remarks = ''
    self.fv_plant_tag_id = ''
    self.fv_plant2 = '' #
    self.fv_publication = ''
    self.fv_published_by = ''
    self.fv_rejected_by = ''
    self.fv_rejection = ''
    self.fv_sample = ''
    self.fv_sample_barcode = ''
    self.fv_sample_id = ''
    self.fv_sample_photos = ''
    self.fv_sample_remarks = ''
    self.fv_sampled_by = '' #*
    self.fv_sampled_plant = ''
    self.fv_sampling_event = ''
    self.fv_scientific_name = ''
    self.fv_site_id = ''
    self.fv_submission = ''
    self.fv_submitted_by = ''
    self.fv_time_sampled = ''
    self.fv_verification = ''
    self.fv_verified_by = ''
    
  def to_csv(self):
    return []

  def to_info(self):
    return []

  def whoami(self):
    return type(self).__name__
    
  def add_toLog(self, st):
    self.logInfo += "\n"+st

##############################################
# LOAD Record
##############################################
def load_bulkleafsample_webhook_Records(calibrations,projects):
  """ This will load Leaf spectra object from webhook
  
  :param arg1: calibrations
  :type arg1: Calibrations object

  :param arg2: projects dictionnary
  :type arg2: projects[projectID] = projectName

  :return: LeafSpectrum object full of LeafSpectra processible
  :rtype: LeafSpectrum
  """
  leafSpectraForm = TO.load_json_file(PA.LeafSpectraFormFile)
  leafSpectraFormID = leafSpectraForm['id']
  webhookRecords = RE.load_webhook_records(projects)
  spectrum = LeafSpectrum()
  for record_raw in webhookRecords.records[:]:
    if leafSpectraFormID not in record.form_id:
      LO.l_info('The record {} will not be used because it is not a leaf spectra record'.format(record_raw.id))
    else:
      record = LeafSpectra(record_raw)
      LO.l_info('Start update record {} with measurments'.format(record.id))
      if extract_leafspectra_record(record):
        LO.l_info('Start update record {} with calibration and date {}'.format(record.id,record.fv_date_measured))
        if link_leafspectra_record_and_calibration(calibrations,record):
          LO.l_war('The record {} is complete for processing'.format(record.id))
          spectrum.add_record(record)
        else:
          LO.l_war('The record {} will not be used'.format(record.id))
      else:
        LO.l_war('The record {} will not be used'.format(record.id))
  return spectrum

def load_bulkleafsample_Records(calibrations,projects):
  """ This will load Leaf spectra object from the Leaf Spectra Backup
  
  :param arg1: calibrations
  :type arg1: Calibrations object

  :param arg2: projects dictionnary
  :type arg2: projects[projectID] = projectName

  :return: LeafSpectrum object full of LeafSpectra processible
  :rtype: LeafSpectrum
  """
  spectrum = LeafSpectrum()
  fileName = PA.LeafSpectraRecordsFile
  rec = RE.load_records_from_json(fileName,projects)
  my_list = add_Records_in_spectrum(calibrations,rec)
  
  my_list2 = []
  if len(my_list)>0:
    my_list2 = update_leafspectra_records_measurements(my_list)

  if len(my_list2)>0:
    for wrap in my_list2[:]:
      spectrum.add_record(wrap)
  
  return spectrum

#########################
# Add
#########################
def add_Records_in_bulkLeafSamples(calibrations,rec):
  """
  This parallelisation of add_Record_in_spectrum
  """
  output = mp.Queue()
  my_list = []
  pool = mp.Pool(processes=3)
  results = [pool.apply_async(add_Record_in_spectrum, args=(calibrations,record_raw)) for record_raw in rec.records[:]]
  pool.close()
  pool.join()
  for r in results:
    b = r.get()
    if b:
      my_list.append(b)
  return my_list
  
def add_Record_in_BulkLeafSamples(calibrations,record_raw):
  """ This will add a valid leaf spectra record
  
  :param arg1: calibrations
  :type arg1: Calibrations object

  :param arg2: a record
  :type arg2: Record Object

  :return: Valid LeafSpectra
  :rtype: LeafSpectra Object
  """
  record = LeafSpectra(record_raw)
  validate_leafspectra_record(calibrations,record)
  if record.isValid:
    LO.l_info('The record id {} is complete for processing'.format(record.id))
    record.add_toLog('The record id {} is complete for processing'.format(record.id))
  else:
    LO.l_war('The record id {} is incomplete and will not be used'.format(record.id))
    record.add_toLog('The record id {} is incomplete and will not be used'.format(record.id))
  return record

##
def validate_bulkLeafSamples_record(calibrations,record):
  """ This will validate a record a leaf spectra record
  
  :param arg1: calibrations
  :type arg1: Calibrations object

  :param arg2: a record
  :type arg2: Record Object

  :return: True if is a valid record False if it's not a LeafSpectra record
  :rtype: boolean (True,False)
  """
  extract_leafspectra_record(record)
  link_leafspectra_record_and_calibration(calibrations,record)
  validate_leafspectra_record_measurements(record)
  return record.isValid

###
def extract_bulkLeafSamples_record(record):
  """ This will append a leaf spectra record data from a record "form values" if it's a valid leaf spectra record
  
  :param arg1: a LeafSpectra to be tested
  :type arg1: LeafSpectra

  :return: True if is a valid record False if it's not a LeafSpectra record
  :rtype: boolean (True,False)
  """
  LO.l_info('Start extract leaf spectra recordid {}'.format(record.id))
  rv  = record.form_values
  if 'date_sampled' in rv \
    and ('plant' in rv or 'plant2' in rv) \
    and 'sampled_by' in rv:
    if 'approbation' in rv: record.fv_approbation = rv['approbation']
    if 'approved_by' in rv: record.fv_approved_by = rv['approved_by']
    if 'data_quality_control' in rv: record.fv_data_quality_control = rv['data_quality_control']
    if 'date_approved' in rv: record.fv_date_approved = rv['date_approved']
    if 'date_deleted' in rv: record.fv_date_deleted = rv['date_deleted']
    if 'date_published' in rv: record.fv_date_published = rv['date_published']
    if 'date_rejected' in rv: record.fv_date_rejected = rv['date_rejected']
    if 'date_sampled' in rv: record.fv_date_sampled = rv['date_sampled']
    if 'date_submitted' in rv: record.fv_date_submitted = rv['date_submitted']
    if 'date_verified' in rv: record.fv_date_verified = rv['date_verified']
    if 'deleted' in rv: record.fv_deleted = rv['deleted']
    if 'deleted_by' in rv: record.fv_deleted_by = rv['deleted_by']
    if 'filter_plot' in rv: record.fv_filter_plot = rv['filter_plot']
    if 'filter_plot_id' in rv: record.fv_filter_plot_id = rv['filter_plot_id']
    if 'filter_site' in rv: record.fv_filter_site = rv['filter_site']
    if 'filter_site_id' in rv: record.fv_filter_site_id = rv['filter_site_id']
    if 'hidden_variables' in rv: record.fv_hidden_variables = rv['hidden_variables']
    if 'number_of_rejections' in rv: record.fv_number_of_rejections = rv['number_of_rejections']
    if 'plant' in rv: record.fv_plant = rv['plant']
    if 'plant_id' in rv: record.fv_plant_id = rv['plant_id']
    if 'plant_remarks' in rv: record.fv_plant_remarks = rv['plant_remarks']
    if 'plant_tag_id' in rv: record.fv_plant_tag_id = rv['plant_tag_id']
    if 'plant2' in rv: record.fv_plant2 = rv['plant2']
    if 'publication' in rv: record.fv_publication = rv['publication']
    if 'published_by' in rv: record.fv_published_by = rv['published_by']
    if 'rejected_by' in rv: record.fv_rejected_by = rv['rejected_by']
    if 'rejection' in rv: record.fv_rejection = rv['rejection']
    if 'sample' in rv: record.fv_sample = rv['sample']
    if 'sample_barcode' in rv: record.fv_sample_barcode = rv['sample_barcode']
    if 'sample_id' in rv: record.fv_sample_id = rv['sample_id']
    if 'sample_photos' in rv: record.fv_sample_photos = rv['sample_photos']
    if 'sample_remarks' in rv: record.fv_sample_remarks = rv['sample_remarks']
    if 'sampled_by' in rv: record.fv_sampled_by = rv['sampled_by']
    if 'sampled_plant' in rv: record.fv_sampled_plant = rv['sampled_plant']
    if 'sampling_event' in rv: record.fv_sampling_event = rv['sampling_event']
    if 'scientific_name' in rv: record.fv_scientific_name = rv['scientific_name']
    if 'site_id' in rv: record.fv_site_id = rv['site_id']
    if 'submission' in rv: record.fv_submission = rv['submission']
    if 'submitted_by' in rv: record.fv_submitted_by = rv['submitted_by']
    if 'time_sampled' in rv: record.fv_time_sampled = rv['time_sampled']
    if 'verification' in rv: record.fv_verification = rv['verification']
    if 'verified_by' in rv: record.fv_verified_by = rv['verified_by']
  else:
    tab = ['date_sampled', 'plant', 'sampled_by']
    s = ""
    for t in tab:
      if t in 'plant':
        #if ('plant' in rv or 'plant2' in rv):
        if s:
          s+=', '
        s += t
      if not t in rv and t not in 'plant':
        if s:
          s+=', '
        s += t
    LO.l_war('Project {}, the record id {} will not be used because it has no {}.'.format(record.project_name,record.id,s))
    record.isValid = False
    record.add_toLog('Project {}, the record id {} will not be used because it has no {}.'.format(record.project_name,record.id,s))

