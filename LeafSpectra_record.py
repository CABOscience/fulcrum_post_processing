#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
import parameters as PA
import records as RE
import tools as TO
import tools_plots as TOP
import tools_fulcrum_api as TOFA
import logs as LO
import LeafSpectra_measurements as LSM
import SpectroscopyPanels_record as SPR
import forms as FO

# System
import os, sys
import multiprocessing as mp
# Data Science
import math
import pandas as pd
import numpy as np
np.set_printoptions(threshold='nan')

##############################################
# Record
##############################################

# OBJECT
#########################

class LeafSpectrum(RE.Records):
  """ Leaf spectrum object
  Leaf spectrum object is containing a list of LeafSpectra Object
  """

class LeafSpectra(RE.Record):
  """ Leaf spectra object
  Leaf spectra object is a Records + its form values
  """
  def __init__(self, record, bfn='',dm='',ii='',lltp='',lsm='',manu='',mb='',measurements=[],paID='',pdir='',pm='',sai='',sn='',spi='',stt='',wf=''):
    super(LeafSpectra,self).__init__(record.altitude, record.assigned_to, record.assigned_to_id, record.client_created_at, record.client_updated_at, record.course, record.created_at, record.created_by, record.created_by_id, record.created_duration, record.created_location, record.edited_duration, record.form_id, record.form_name, record.form_values, record.horizontal_accuracy, record.id, record.latitude, record.longitude, record.project_id, record.speed, record.status, record.updated_at, record.updated_by, record.updated_by_id, record.updated_duration, record.updated_location, record.version, record.vertical_accuracy, record.project_name)
    self.fv_base_file_name = bfn
    self.fv_calibration = SPR.get_empty_calib()
    self.fv_date_measured = dm
    self.fv_figs = []
    self.fv_instrumentation_id = ii
    self.fv_leaf_larger_than_port = lltp
    self.fv_leaf_sides_measured = lsm
    self.fv_manufacturer_short_name_sphere = manu
    self.fv_measured_by = mb
    self.fv_measurements = measurements
    self.fv_panel_id = paID
    self.fv_parent_directory = pdir
    self.fv_properties_measured = pm
    self.fv_reflecAverage = pd.Series()
    self.fv_reflecDiffRef = pd.Series()
    self.fv_reflecLeaves  = {}
    self.fv_reflecRef     = pd.Series()
    self.fv_reflecStadDev = pd.Series()
    self.fv_sample_id = sai
    self.fv_scientific_name = sn
    self.fv_spectroradiometer_id = spi
    self.fv_spectroradiometer_start_time = stt
    self.fv_working_folder = wf
    self.fv_transAverage  = pd.Series()
    self.fv_transDiffRef  = pd.Series()
    self.fv_transLeaves    = {}
    self.fv_transStadDev  = pd.Series()
    self.fv_processedPath = "" # it will be PA.ProjectWebsitePath+self.project_name+'/spectra/processed/'+self.fv_working_folder+'/'+self.fv_sample_id
    self.fv_extFile = ""
    self.fv_measureType = ""
    self.fv_event_remarks = ''
    self.fv_computer = ''
    self.fv_computer_type = ''
    self.fv_serial_number = ''
    self.fv_instrumentation_type = ''
    self.fv_manufacturer_short_name = ''
    self.fv_protocol = ''
    self.fv_protocols = ''
    self.fv_protocol_url = ''
    self.fv_leaf_photos = ''
    self.fv_number_of_measurements = ''
    self.fv_deleted_by = ''
    self.fv_date_deleted = ''
    self.fv_rejected_by = ''
    self.fv_date_rejected = ''
    self.fv_verified_by = ''
    self.fv_date_verified = ''
    self.fv_submitted_by = ''
    self.fv_date_submitted = ''
    self.fv_approved_by = ''
    self.fv_date_approved = ''
    self.fv_published_by = ''
    self.fv_date_published = ''
    self.leaves_plot = ''
    
  def to_csv_all(self):
    #return super(LeafSpectra, self).to_csv()+[self.id, self.fv_sample_id, self.fv_scientific_name, self.fv_date_measured, self.fv_measured_by, self.fv_spectroradiometer_start_time, self.fv_spectroradiometer_id, self.fv_instrumentation_id]
    return [self.id, self.fv_sample_id, self.fv_scientific_name, self.fv_date_measured, self.fv_measured_by, self.fv_spectroradiometer_start_time, self.fv_spectroradiometer_id, self.fv_instrumentation_id,self.fv_leaf_sides_measured]

  def to_info(self):
    #return super(LeafSpectra, self).to_info()+[self.id,self.fv_sample_id,self.fv_scientific_name,self.fv_date_measured,self.fv_measured_by]
    return [self.id,self.fv_sample_id,self.fv_scientific_name,self.fv_date_measured,self.fv_measured_by]

  def whoami(self):
    return type(self).__name__
  
  def get_wavelength_max(self):
    wmax = -1
    for measurement in self.fv_measurements:
      wmaxt = measurement.m_get_wavelength_max()
      if wmax == -1:
        wmax = wmaxt
      elif wmaxt < wmax:
        wmax = wmaxt
    return wmax

  def get_wavelength_min(self):
    wmin = -1
    for measurement in self.fv_measurements:
      wmint = measurement.m_get_wavelength_min()
      if wmin == -1:
        wmin = wmint
      elif wmint > wmin:
        wmin = wmint
    return wmin
    

##############################################
# LOAD Record
##############################################
def load_leafspectra_webhook_Records(calibrations):
  """ This will load Leaf spectra object from webhook
  
  :param arg1: calibrations
  :type arg1: Calibrations object

  :return: LeafSpectrum object full of LeafSpectra processible
  :rtype: LeafSpectrum
  """
  leafSpectraForm = TO.load_json_file(PA.LeafSpectraFormFile)
  leafSpectraFormID = leafSpectraForm['id']
  webhookRecords = RE.load_webhook_records()
  spectrum = LeafSpectrum()
  for record_raw in webhookRecords.records[:]:
    if leafSpectraFormID not in record.form_id:
      st = 'The record {} will not be used because it is not a leaf spectra record'.format(record_raw.id)
      LO.l_debug(st)
      record_raw.add_toLog(st)
    else:
      record = LeafSpectra(record_raw)
      st = 'Start update record {} with measurments'.format(record.id)
      LO.l_debug(st)
      record.add_toLog(st)
      if extract_leafspectra_record(record):
        st = 'Start update record {} with calibration and date {}'.format(record.id,record.fv_date_measured)
        LO.l_debug(st)
        record.add_toLog(st)
        if link_leafspectra_record_and_calibration(calibrations,record):
          st = 'The record {} is complete for processing'.format(record.id)
          LO.l_debug(st)
          spectrum.add_record(record)
          record.add_toLog(st)
        else:
          st = 'The record {} will not be used'.format(record.id)
          LO.l_war(st)
          record.add_toLog(st)
      else:
        st = 'The record {} will not be used'.format(record.id)
        LO.l_war(st)
        record.add_toLog(st)
  return spectrum

def load_leafspectra_Records(spectroPanels):
  """ This will load Leaf spectra object from the Leaf Spectra Backup
  
  :param arg1: calibrations
  :type arg1: Calibrations object

  :return: LeafSpectrum object full of LeafSpectra processible
  :rtype: LeafSpectrum
  """
  spectrum = LeafSpectrum()
  # Load records
  rec = load_leafspectra_Records_from_file()
  my_list = []
  #for record_raw in rec.records[:]:
  #  my_list.append(add_Record_in_spectrum(spectroPanels,record_raw))
  my_list = add_Records_in_spectrum(spectroPanels,rec)
  my_list2 = []
  if len(my_list)>0:
    # update measurments
    my_list2 = update_leafspectra_records_measurements(my_list)
  if len(my_list2)>0:
    for record in my_list2[:]:
      # Add in spectrum
      spectrum.add_record(record)
  return spectrum

def load_leafspectra_Records_from_file():
  fname = PA.LeafSpectraRecordsFile
  if TO.file_is_here(fname):
    LO.l_debug('The leaf spectra file is {}'.format(fname))
    return RE.load_records_from_json(fname)
  else:
    LO.l_war('The leaf spectra file ({}) is available. Program will die'.format(fname))
    sys.exit(1)


#########################
# Add
#########################
def add_Records_in_spectrum(calibrations,rec):
  """
  This parallelisation of add_Record_in_spectrum
  """
  output = mp.Queue()
  my_list = []
  pool = mp.Pool(processes=PA.NumberOfProcesses)
  results = [pool.apply_async(add_Record_in_spectrum, args=(calibrations,record_raw)) for record_raw in rec.records[:]]
  #results = []
  #for record_raw in rec.records[:]:
  #  results.append(add_Record_in_spectrum(calibrations,record_raw))
  pool.close()
  pool.join()
  for r in results:
    b = r.get()
    if b:
      my_list.append(b)
  return my_list
  '''
  for record_raw in rec.records[:]:
    add_Record_in_spectrum(calibrations,record_raw)
  sys.exit(1)
  '''
  
def add_Record_in_spectrum(spectroPanels,record_raw):
  """ This will add a valid leaf spectra record
  
  :param arg1: calibrations
  :type arg1: Calibrations object

  :param arg2: a record
  :type arg2: Record Object

  :return: Valid LeafSpectra
  :rtype: LeafSpectra Object
  """
  record = LeafSpectra(record_raw)
  validate_leafspectra_record(spectroPanels,record)
  if record.isValid:
    st = 'The record id {} is complete for processing'.format(record.id)
    LO.l_debug(st)
    record.add_toLog(st)
  else:
    st = 'The record id {} is incomplete and will not be used'.format(record.id)
    LO.l_war(st)
    record.add_toLog(st)
  return record

##
def validate_leafspectra_record(spectroPanels,record):
  """ This will validate a record a leaf spectra record
  
  :param arg1: calibrations
  :type arg1: Calibrations object

  :param arg2: a record
  :type arg2: Record Object

  :return: True if is a valid record False if it's not a LeafSpectra record
  :rtype: boolean (True,False)
  """
  extract_leafspectra_record(record)
  link_leafspectra_record_and_calibration(spectroPanels,record)
  validate_leafspectra_record_measurements(record)
  return record.isValid

###
def extract_leafspectra_record(record):
  """ This will append a leaf spectra record data from a record "form values" if it's a valid leaf spectra record
  
  :param arg1: a LeafSpectra to be tested
  :type arg1: LeafSpectra
  """
  LO.l_debug('Start extract leaf spectra recordid {}'.format(record.id))
  # Pretest because leaf spectra need an associated project
  if record.is_record_has_project():
    rv  = record.form_values
    if 'base_file_name' in rv \
      and 'working_folder' in rv \
      and 'scientific_name' in rv \
      and 'properties_measured' in rv:
      record.fv_base_file_name     = rv['base_file_name']
      record.fv_date_measured      = rv['date_measured']
      record.fv_instrumentation_id = rv['instrumentation_id'][0]['record_id']
      record.fv_leaf_larger_than_port = rv['leaf_larger_than_port']
      #record.fv_leaf_sides_measured   = TO.get_fulcrum_multiple_choice_in_string(rv['leaf_sides_measured'])
      record.fv_leaf_sides_measured   = rv['leaf_sides_measured']['choice_values'][0]
      record.fv_manufacturer_short_name_sphere = rv['manufacturer_short_name_sphere']
      record.fv_measured_by        = TO.get_fulcrum_multiple_choice_in_string(rv['measured_by'])
      record.fv_measurements       = LSM.extract_leaf_spectra_measurements(rv['measurements']) # all measurements
      record.fv_panel_id           = rv['panel_id'][0]['record_id']
      record.fv_parent_directory   = rv['parent_directory']
      record.fv_properties_measured= rv['properties_measured']
      record.fv_sample_id          = rv['sample_id']
      record.fv_scientific_name    = rv['scientific_name']
      record.fv_spectroradiometer_id = rv['spectroradiometer_id'][0]['record_id']
      record.fv_spectroradiometer_start_time = rv['spectroradiometer_start_time']
      record.fv_working_folder = rv['working_folder']
      record.fv_processedPath = PA.ProjectWebsitePath+record.project_name+'/spectra/processed/'+record.fv_working_folder+'/'+record.fv_sample_id
      if 'event_remarks'  in rv: record.fv_event_remarks  = rv['event_remarks']
      if 'computer'       in rv: record.fv_computer  = rv['computer']
      if 'computer_type'  in rv: record.fv_computer_type  = rv['computer_type']
      if 'serial_number'  in rv: record.fv_serial_number  = rv['serial_number']
      if 'instrumentation_type' in rv: record.fv_instrumentation_type  = rv['instrumentation_type']
      if 'manufacturer_short_name' in rv: record.fv_manufacturer_short_name  = rv['manufacturer_short_name']
      if 'protocol'       in rv: record.fv_protocol  = rv['protocol']
      if 'protocols'      in rv: record.fv_protocols  = rv['protocols']
      if 'protocol_url'   in rv: record.fv_protocol_url  = rv['protocol_url']
      if 'leaf_photos'    in rv: record.fv_leaf_photos  = rv['leaf_photos']
      if 'number_of_measurements' in rv: record.fv_number_of_measurements  = rv['number_of_measurements']
      if 'deleted_by'     in rv: record.fv_deleted_by  = rv['deleted_by']
      if 'date_deleted'   in rv: record.fv_date_deleted  = rv['date_deleted']
      if 'rejected_by'    in rv: record.fv_rejected_by  = rv['rejected_by']
      if 'date_rejected'  in rv: record.fv_date_rejected  = rv['date_rejected']
      if 'verified_by'    in rv: record.fv_verified_by  = rv['verified_by']
      if 'date_verified'  in rv: record.fv_date_verified  = rv['date_verified']
      if 'submitted_by'   in rv: record.fv_submitted_by  = rv['submitted_by']
      if 'date_submitted' in rv: record.fv_date_submitted  = rv['date_submitted']
      if 'approved_by'    in rv: record.fv_approved_by  = rv['approved_by']
      if 'date_approved'  in rv: record.fv_date_approved  = rv['date_approved']
      if 'published_by'   in rv: record.fv_published_by  = rv['published_by']
      if 'date_published' in rv: record.fv_date_published  = rv['date_published']    
      if record.fv_manufacturer_short_name_sphere == 'SVC':
        record.fv_extFile = '.sig'
        record.fv_measureType = 'tgt_counts'
      #if '5d3ca27b-c67d-4b85-835c-9d418141fc25' not in record.id:
      #  record.isValid = False
    else:
      tab = ['base_file_name','working_folder','scientific_name','properties_measured']
      s = ""
      for t in tab:
        if not t in rv:
          if s:
            s+=', '
          s += t
      record.isValid = False
      record.fv_processedPath = PA.ProjectWebsitePath+record.project_name+'/rejected_records/'
      st = 'Project {}, the record id {} will not be used because it has no {}.'.format(record.project_name,record.id,s)
      LO.l_war(st)
      record.add_toLog(st)

###
def link_leafspectra_record_and_calibration(spectroPanels,record):
  """ This will link calibration and a leaf spectra record
  
  :param arg1: a Calibrations list
  :type arg1: Calibrations

  :param arg2: a fulcrum measurements list
  :type arg2: LeafSpectra

  :return: True if a calibration has been found, false if the calibration has not been found
  :rtype: boolean (True/False)
  """
  if record.isValid:
    rID     = record.id
    panel_id= record.fv_panel_id
    temp    = record.fv_date_measured
    calib   = SPR.get_calibration_from_panelID(temp, panel_id, spectroPanels)
    st = 'Start update record {} with calibration and date {}'.format(rID,temp)
    LO.l_debug(st)
    record.add_toLog(st)
    
    if calib:
      record.fv_calibration = calib
      st = "The record calibration file path is: {}".format(calib.cFilePath)
      LO.l_debug(st)
      record.add_toLog(st)
    else:
      record.isValid = False
      st = "The record id {} with the time {} with calibration panel {} was not found. Please update calibrations.".format(rID,temp,panel_id)
      LO.l_war(st)
      record.add_toLog(st)

###
def validate_leafspectra_record_measurements(record):
  """ This will validate the leaf spectra record link measurments
  
  :param arg1: a LeafSpectra to be tested
  :type arg1: LeafSpectra

  :return: True if is a valid record False if it's not a LeafSpectra record
  :rtype: boolean (True,False)
  """
  # from record object
  pname = record.project_name
  rid   = record.id
  # from leaf spectra object
  ext  = record.fv_extFile
  measurements=record.fv_measurements
  wf    = record.fv_working_folder
  
  measurmentsDone = True
  tps = 'Start validate record {} measurments'.format(record.id)
  LO.l_debug(tps)
  record.add_toLog(tps)
  
  for measurement in measurements:
    fName = PA.ProjectWebsitePath+''+pname+'/spectra/raw/'+wf+'/'+measurement.file_name+''+ext
    measurement.file_path = fName
    if not TO.file_is_here(fName):
      measurmentsDone = False
      st =  "The record id {} has not {} available.".format(rid,fName)
      LO.l_war(st)
      record.add_toLog(st)
  if not measurmentsDone:
    record.isValid = False

#########################
# Record measurments updated
#########################
def update_leafspectra_records_measurements(records_raw):
  """
  This parallelisation of update_leafspectra_record_measurements
  """
  my_list = []
  pool = mp.Pool(processes=PA.NumberOfProcesses)
  results = [pool.apply_async(update_leafspectra_record_measurements, args=(record_raw,)) for record_raw in records_raw[:]]
  pool.close()
  pool.join()
  for r in results:
    b = r.get()
    if b:
      my_list.append(b)
  return my_list

def update_leafspectra_record_measurements(record):
  """ This will link metadata and data extracted from files of a leaf spectra record
  It will also prepare "interpolated_files" form processing
  
  :param arg1: a LeafSpectra to be tested
  :type arg1: LeafSpectra
  
  :return: a record 
  :rtype: LeafSpectra (with measurments updated)
  """
  if record.isValid:
    # from record object
    pname = record.project_name
    rid   = record.id
    # from leaf spectra object
    ext         = record.fv_extFile
    measurements=record.fv_measurements
    measureType = record.fv_measureType
    wf          = record.fv_working_folder
    
    measurmentsDone = True
    for measurement in measurements:
      fName = measurement.file_path
      if TO.file_is_here(fName):
        LO.l_debug("\tStart spectre extraction for {}".format(fName))
        spect = TO.create_spectrum(fName,measureType)
        measurement.spectre = spect
        measurement.spectre.interpolate(method='cubic')
        TO.create_directory(record.fv_processedPath+'/interpolated_files/')
        spectreProcessed = record.fv_processedPath+'/interpolated_files/'+measurement.file_name+ext+'.txt'
        s = '{}'.format(measurement.spectre)
        s += '###############\nALL DATA\n###############\n'
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
          s += '{}'.format(measurement.spectre.measurement)
        TO.string_to_file(spectreProcessed,'{}'.format(s))
      else:
        st = "The record id {} has not {} available.".format(rid,fName)
        LO.l_war(st)
        record.add_toLog(st)
        measurmentsDone = False
    if not measurmentsDone:
      st = "The record id {} will not be used because it has not all its spectre available.".format(rid)
      LO.l_war(st)
      record.add_toLog(st)
      record.isValid = False
  return record

##############################################
## Process records
##############################################
def process_leafspectra_records(rec):
  """
  This parallelisation of process_record
  """
  """
  spectrum = LeafSpectrum()
  for record in rec.records[:]:
    rec = process_leafspectra_record(record)
    if rec:
      spectrum.add_record(rec)
  return spectrum
      
  """
  # parallelisation here
  output = mp.Queue()
  pool = mp.Pool(processes=PA.NumberOfProcesses)
  results = [pool.apply_async(process_leafspectra_record, args=(record,)) for record in rec.records[:]]
  pool.close()
  pool.join()
  spectrum = LeafSpectrum()
  for r in results:
    record = r.get()
    if record:
      spectrum.add_record(record)
  return spectrum

 
def process_leafspectra_record(record):
  """Process a leaf spectra record
  This function take a leafspectra record object and return a processed leafspectra record processed object
  """
  if record.isValid:
    st = 'Start prepare spectrum data for record {}'.format(record.id)
    LO.l_info(st)
    record.add_toLog(st)
    record = calculate_leafspectra_record(record)
    if record.isProcessed == True:
      st = 'Start prepare csv files for record {}'.format(record.id)
      LO.l_info(st)
      record.add_toLog(st)
      leafspectra_record_to_csv(record)
  return record

# Spectrum Data
##############################################
def calculate_leafspectra_record(record):
  # Check the Protocol choosed
  if record.fv_manufacturer_short_name_sphere == 'SVC':
    LO.l_debug("Start SVC spectrum data for record {}".format(record.id))
    record.isProcessed = True
    if record.fv_leaf_larger_than_port == 'yes':
      LO.l_debug('large leaf')
      record = large_leaf_calculation(record)
    elif record.fv_leaf_larger_than_port == 'no':
      LO.l_debug('small leaf')
      record = small_leaf_calculation(record)
  else:
    record.isProcessed = False
    st = "No known manufacturer short name sphere for record {}".format(record.id)
    LO.l_war(st)
    record.add_toLog(st)
  return record

  ## Spectrum Calculations
  ########################
    ### Large Leaf calculation
    ########################
def large_leaf_calculation(record):
  pm = record.fv_properties_measured
  pmB, pmR, pmT = (False for i in range(3))
  if 'both' in pm:
    pmB = True
  if pmB or 'reflectance' in pm:
    pmR = True
  if pmB or 'transmittance' in pm:
    pmT = True

  wvlMax = record.fv_calibration.cMax
  wvlMin = record.fv_calibration.cMin
  reflTargets, reflStrays, reflRefs = ([] for i in range(3))
  transRefAll, transTargets = ([] for i in range(2))
  
  for measurement in record.fv_measurements:
    # Reflectance
    if 'A:' in measurement.sphere_configuration_svc_large_leaves:
      reflRefs.append(measurement)
      if len(reflRefs)>0:
        # set values max and min from the min of max wvl or max calibration data
        wvl_max = reflRefs[0].spectre.metadata['wavelength_range'][1]
        wvl_min = reflRefs[0].spectre.metadata['wavelength_range'][0]
        if wvl_max < wvlMax:
          wvlMax = wvl_max
        if wvl_min > wvlMin:
          wvlMin = wvl_min
      else:
        st = "The record {} doesn't have any reference. The wvlMax and wvlMin used will come from calibration".format(record.id)
        LO.l_war(st)
        record.add_toLog(st)
    if 'B:' in measurement.sphere_configuration_svc_large_leaves:
      reflStrays.append(measurement) #B: No leaf
    if 'C:' in measurement.sphere_configuration_svc_large_leaves:
      leafNumber = measurement.leaf_number
      if leafNumber:
        reflTargets.append(measurement)
        record.fv_reflecLeaves[leafNumber] = measurement
    #Transmission
    if 'D:' in measurement.sphere_configuration_svc_large_leaves:
      transRefAll.append(measurement) 
    if 'E:' in measurement.sphere_configuration_svc_large_leaves:
      leafNumber = measurement.leaf_number
      if leafNumber:
        transTargets.append(measurement)
        record.fv_transLeaves[leafNumber] = measurement
  
  # Fix the range, if not use of calibration
  if not pmR:
    wvlMax = transRefAll[0].spectre.metadata['wavelength_range'][1]
    wvlMin = transRefAll[0].spectre.metadata['wavelength_range'][0]

  # REFLECTANCE CALCULATION
  # https://www.protocols.io/view/measuring-spectral-reflectance-and-transmittance-3-p8pdrvn?step=67
  if pmR and len(reflStrays)>0 and len(reflRefs)>0 and len(reflTargets)>0:
    # Calibration
    calib = record.fv_calibration.spectre.measurement.sort_index().loc[wvlMin:wvlMax]
    # (A - B):
    divisorsTar = reflRefs[0].spectre.measurement.sub(reflStrays[0].spectre.measurement)
    # Calculations per leafs:
    for reflTarget in reflTargets:
      # (C - B):
      dividendsTar = reflTarget.spectre.measurement.sub(reflStrays[0].spectre.measurement)
      # [ (C - B) ÷ (A - B) ]
      divisionTar = dividendsTar.div(divisorsTar)
      # ([ (C - B) ÷ (A - B) ]) × calib.refl
      mseries = TO.get_monotonic_series(divisionTar)
      for i in range(len(mseries)):
        mserie = mseries[i].sort_index().loc[wvlMin:wvlMax]
        for ind, row in mserie.iteritems():
          mserie.set_value(ind,row*calib.at[ind])
        mseries[i] = mserie
        i+=1
      reflectance = pd.concat(mseries)
      reflTarget.reflectance= reflectance

    # Average and Standard Deviation
    arr     = np.array([reflTarget.reflectance for reflTarget in reflTargets])
    arrIndex= np.array(reflTargets[0].reflectance.index)
    arrMean = np.mean(arr, axis=0)
    arrStd  = np.std(arr, axis=0, ddof=1)
    
    reflecAverage = pd.Series(arrMean, index=arrIndex, name="reflectance_average")
    reflecAverage.index.name = 'wavelength'
    record.fv_reflecAverage = reflecAverage
    reflecStadDev = pd.Series(arrStd, index=arrIndex, name="reflectance_standard_deviation")
    reflecStadDev.index.name = 'wavelength'
    record.fv_reflecStadDev = reflecStadDev

    # Calculation of (A1/A0):
    distA0A1 = pd.Series()
    if len(reflRefs) == 2:
      distA0A1 = reflRefs[1].spectre.measurement.div(reflRefs[0].spectre.measurement)
      record.fv_reflecDiffRef = distA0A1
    else:
      record.isProcessed = False
      st = "The record {} haven't the right number of reference measurments to process the reference of reflectance calculation. Number of A measurments = {} (need to be = 2)".format(record.id,len(reflRefs))
      LO.l_war(st)
      record.add_toLog(st)
    # Calculation of (B0/A0):
    distB0A1 = pd.Series()
    if len(reflStrays) > 0 and len(reflRefs) > 0 :
      distB0A1 = reflStrays[0].spectre.measurement.div(reflRefs[0].spectre.measurement)
      record.fv_reflecRef = distB0A1
    else:
      record.isProcessed = False
      st = "The record {} have just one reference measurments to process the stray light vs reference. Number of D measurments = {}. Number of B measurments = {} (need to be > 0) and Number of A measurments = {} (need to be > 0).".format(record.id,len(reflStrays),len(reflRefs))
      LO.l_war(st)
      record.add_toLog(st)
  else:
    record.isProcessed = False
    st = "The record {} doesn't have all spectrum measurments to process the reflectance calculation. Number of B measurments = {} (need to be > 0) and Number of A measurments = {} (need to be > 0) and Number of C measurments = {} (need to be > 0).".format(record.id,len(reflStrays),len(reflRefs),len(reflTargets))
    LO.l_err(st)
    record.add_toLog(st)
  
  # Transmittance
  # https://www.protocols.io/view/measuring-spectral-reflectance-and-transmittance-3-p8pdrvn?step=68
  if pmT and len(transTargets)>0 and len(transRefAll)>0:
    for transTarget in transTargets:
      trans = transTarget.spectre.measurement.div(transRefAll[0].spectre.measurement)
      # Create the sample (wvl,transmittance)
      transmittance = trans.sort_index().loc[wvlMin:wvlMax]
      transTarget.transmittance = transmittance
      
    # Average and Standard Deviation
    arr = np.array([transTarget.transmittance for transTarget in transTargets])
    arrIndex = np.array(transTargets[0].transmittance.index)
    arrMean = np.mean(arr, axis=0)
    arrStd = np.std(arr, axis=0, ddof=1)

    transAverage = pd.Series(arrMean, index=arrIndex, name="transmittance_average")
    transAverage.index.name = 'wavelength'
    record.fv_transAverage = transAverage
    transStadDev = pd.Series(arrStd, index=arrIndex, name="transmittance_standard_deviation")
    transStadDev.index.name = 'wavelength'
    record.fv_transStadDev = transStadDev

    # Calculation of (D1/D0):
    distD0D1 = pd.Series()
    if len(transRefAll) == 2:
      distD0D1 = transRefAll[1].spectre.measurement.div(transRefAll[0].spectre.measurement)
      record.fv_transDiffRef    = distD0D1
    else:
      record.isProcessed = False
      st = "The record {} haven't the right number of reference measurments to process the reference of transmittance calculation. Number of D measurments = {} (need to be = 2).".format(record.id,len(transRefAll))
      LO.l_war(st)
      record.add_toLog(st)
  else:
    record.isProcessed = False
    st = "The record {} doesn't have all spectrum measurments to process the transmittance calculation.  Number of E measurments = {} (need to be > 0) and  Number of D measurments = {} (need to be >0).".format(record.id,len(transTargets),len(transRefAll))
    LO.l_err(st)
    record.add_toLog(st)
  return record

    ### Small Leaf calculation
    ########################
def small_leaf_calculation(record):
  pm = record.fv_properties_measured
  pmB, pmR, pmT = (False for i in range(3))
  if 'both' in pm:
    pmB = True
  if pmB or 'reflectance' in pm:
    pmR = True
  if pmB or 'transmittance' in pm:
    pmT = True

  wvlMax = record.fv_calibration.cMax
  wvlMin = record.fv_calibration.cMin
  
  RrefA, RrefAP, RtarAPi, RtarAi, RrefP, RtarP, Rstr = ([] for i in range(7))
  TrefA, TtarAi = ([] for i in range(2))
  
  for measurement in record.fv_measurements:
    #Reflectance
    if 'A:' in measurement.sphere_configuration_svc_small_leaves:
      RrefA.append(measurement)
    if 'B:' in measurement.sphere_configuration_svc_small_leaves:
      RrefAP.append(measurement) #B: No leaf
    if 'C:' in measurement.sphere_configuration_svc_small_leaves:
      RrefP.append(measurement)
    if 'D:' in measurement.sphere_configuration_svc_small_leaves:
      Rstr.append(measurement) 
    if 'E:' in measurement.sphere_configuration_svc_small_leaves:
      RtarP.append(measurement)
    if 'F:' in measurement.sphere_configuration_svc_small_leaves:
      leafNumber = measurement.leaf_number
      if leafNumber:
        RtarAPi.append(measurement)
        record.fv_reflecLeaves[leafNumber] = measurement
    if'G:' in measurement.sphere_configuration_svc_small_leaves:
      RtarAi.append(measurement)
    # Transmittance
    if 'H:' in measurement.sphere_configuration_svc_small_leaves:
      TrefA.append(measurement)
    if 'I:' in measurement.sphere_configuration_svc_small_leaves:
      leafNumber = measurement.leaf_number
      if leafNumber:
        TtarAi.append(measurement)
        record.fv_transLeaves[leafNumber] = measurement
  
  # Fix the range, if not use of calibration
  if not pmR:
    wvlMax = TrefA[0].spectre.metadata['wavelength_range'][1]
    wvlMin = TrefA[0].spectre.metadata['wavelength_range'][0]
  
  lwv = 400.0
  # REFLECTANCE CALCULATION
  # https://www.protocols.io/view/measuring-spectral-reflectance-and-transmittance-3-q56dy9e?step=117
  if pmR and len(RtarAPi) == len(RtarAi) and len(RtarAPi)>2:
    # Calibration
    calib = record.fv_calibration.spectre.measurement.sort_index().loc[wvlMin:wvlMax]
    # absolute reflectance of the filter paper (arfp) at 400nm
    # arfp = [(RtarP[0] - Rstr[0]) ÷ (RrefP[0] - Rstr[0])] × calib
    # (C - D) or (RrefP[0] - Rstr[0])
    divisorArfp = RrefP[0].spectre.measurement.at[lwv] - Rstr[0].spectre.measurement.at[lwv]
    # (E - D) or (RtarP[0] - Rstr[0])
    dividendArfp = RtarP[0].spectre.measurement.at[lwv] - Rstr[0].spectre.measurement.at[lwv]
    # (E - D)/(C - D) or [(RtarP[0] - Rstr[0]) ÷ (RrefP[0] - Rstr[0])]
    divisionArfp = dividendArfp / divisorArfp
    # ([ (E - D)/(C - D) ]) × calib.refl
    arfp = divisionArfp * calib.at[lwv]
    #(calib ÷ arfp)
    multip = calib.at[lwv] / arfp

    for i in range(len(RtarAPi)):
      t = 0
      if i > 2:
        t = 1
      # (A-D) or (RrefA - Rstr)
      AD400 = RrefA[t].spectre.measurement.at[lwv] - Rstr[0].spectre.measurement.at[lwv]
      # (B-D) or (RrefAP - Rstr)
      BD400 = RrefAP[t].spectre.measurement.at[lwv] - Rstr[0].spectre.measurement.at[lwv]
      # (G-D)
      # (RtarAi - Rstr)
      GD400 = RtarAi[i].spectre.measurement.at[lwv] - Rstr[0].spectre.measurement.at[lwv]
      # (G-D)/(A-D)
      # (RtarAi - Rstr) ÷ (RrefA - Rstr)
      rightGri400 = GD400 / AD400
      # (F-D)
      # (RtarAPi - Rstr)
      FD400 = RtarAPi[i].spectre.measurement.at[lwv] - Rstr[0].spectre.measurement.at[lwv]
      # (F-D)/(B-D)
      # (RtarAPi - Rstr) ÷ (RrefAP - Rstr)
      leftGri400 = FD400 / BD400
      # [(F-D)/(B-D) - (G-D)/(A-D)]
      # [ ( (RtarAPi - Rstr) ÷ (RrefAP - Rstr) ) - ( (RtarAi - Rstr) ÷ (RrefA - Rstr) ) ]
      gri400 = leftGri400 - rightGri400
      # [(F-D)/(B-D) - (G-D)/(A-D)] * multip
      # [ ( (RtarAPi - Rstr) ÷ (RrefAP - Rstr) ) - ( (RtarAi - Rstr) ÷ (RrefA - Rstr) ) ] × ( calib ÷ arfp)
      Gri400 = gri400 * multip
      # [1 ÷ (1 - Gri)]
      dGri400 = (1/(1-Gri400))
      # (A-D) or (RrefA - Rstr)
      AD = RrefA[t].spectre.measurement.sub(Rstr[0].spectre.measurement)
      # (G-D) or (RtarAi - Rstr)
      GD = RtarAi[i].spectre.measurement.sub(Rstr[0].spectre.measurement)
      # (G-D)/(A-D) or (RtarAi - Rstr) ÷ (RrefA - Rstr)
      rightGri = GD.div(AD)
      # [(G-D)/(A-D)] × calib × dGri400
      # rightGri × calib or [(RtarA[i] - Rstr) ÷ (RrefA - Rstr)] × calib × [1 ÷ (1 - Gri)]
      mseries = TO.get_monotonic_series(rightGri)
      for x in range(len(mseries)):
        mserie = mseries[x].sort_index().loc[wvlMin:wvlMax]
        for ind, row in mserie.iteritems():
          val = row * calib.at[ind] * dGri400
          mserie.set_value(ind,val)
        mseries[x] = mserie
      pAi = pd.concat(mseries)
      RtarAPi[i].reflectance = pAi
      
    # Average and Standard Deviation
    arr     = np.array([x.reflectance for x in RtarAPi])
    arrIndex= np.array(RtarAPi[0].reflectance.index)
    arrMean = np.mean(arr, axis=0)
    arrStd  = np.std(arr, axis=0, ddof=1)
    
    reflecAverage = pd.Series(arrMean, index=arrIndex, name="reflectance_average")
    reflecAverage.index.name = 'wavelength'
    record.fv_reflecAverage = reflecAverage
    reflecStadDev = pd.Series(arrStd, index=arrIndex, name="reflectance_standard_deviation")
    reflecStadDev.index.name = 'wavelength'
    record.fv_reflecStadDev = reflecStadDev

    # Calculation of (A1/A0):
    distA0A1 = pd.Series()
    if len(RrefA) >1:
      distA0A1 = RrefA[1].spectre.measurement.div(RrefA[0].spectre.measurement)
      record.fv_reflecDiffRef = distA0A1
    else:
      record.isProcessed = False
      st = "The record {} have just one reference measurments to process the reference of refletance calculation. Number of A measurments = {} (need to be > 0).".format(record.id,len(RrefA))
      LO.l_war(st)
      record.add_toLog(st)
    # Calculation of (D0 / A0 => put in reference !):
    if len(RrefA)>0 and len(Rstr)>0:
      distD0A0 = Rstr[0].spectre.measurement.div(RrefA[0].spectre.measurement)
      record.fv_reflecRef = distD0A0
    else:
      record.isProcessed = False
      st = "The record {} have just one reference measurments to process the stray light vs reference. Number of A measurments = {} (need to be > 0) and Number of D measurments = {} (need to be > 0).".format(record.id,len(RrefA),len(Rstr))
      LO.l_war(st)
      record.add_toLog(st)
    
  else:
    record.isProcessed = False
    st = "The record {} doesn't have all spectrum measurments to process the refletance calculation. Number of D measurments = {} (need to be > 2 and need to be equal to number of G). Number of G measurments = {} (need to be equal to number of D).".format(record.id,len(RtarAPi),len(RtarAi))
    LO.l_war(st)
    record.add_toLog(st)
        
  # Transmittance
  # https://www.protocols.io/view/measuring-spectral-reflectance-and-transmittance-3-q56dy9e?step=118
  if pmT and len(TtarAi)>0 and len(TrefA)>0:
    for i in range(len(TtarAi)):
      # (I/H) at 400
      # Gti = Ttari ÷ Tref
      Gti = TtarAi[i].spectre.measurement.at[lwv] / TrefA[0].spectre.measurement.at[lwv]
      dGti = (1 / (1 - Gti))
      # (I/H)
      # (Ttar,i  ÷ Tref)
      IH = TtarAi[i].spectre.measurement.div(TrefA[0].spectre.measurement)
      # ((I/H)-Gti)*dGti
      # [ (Ttar,i  ÷ Tref) - Gti ] × [ 1 ÷ (1 - Gti) ]
      mseries = TO.get_monotonic_series(IH)
      for x in range(len(mseries)):
        mserie = mseries[x].sort_index().loc[wvlMin:wvlMax]
        for ind, row in mserie.iteritems():
          val = (row - Gti) * dGti
          mserie.set_value(ind,val)
        mseries[x] = mserie
      tAi = pd.concat(mseries)
      TtarAi[i].transmittance = tAi

    # Average and Standard Deviation
    arr     = np.array([x.transmittance for x in TtarAi])
    arrIndex= np.array(TtarAi[0].transmittance.index)
    arrMean = np.mean(arr, axis=0)
    arrStd  = np.std(arr, axis=0, ddof=1)

    transAverage = pd.Series(arrMean, index=arrIndex, name="transmittance_average")
    transAverage.index.name = 'wavelength'
    record.fv_transAverage = transAverage
    transStadDev = pd.Series(arrStd, index=arrIndex, name="transmittance_standard_deviation")
    transStadDev.index.name = 'wavelength'
    record.fv_transStadDev = transStadDev
      
    # Calculation of (H1/H0):
    distH0H1 = pd.Series()
    if len(TrefA) > 1:
      # refH1 / refH0 
      distH0H1 = TrefA[1].spectre.measurement.div(TrefA[0].spectre.measurement)
      record.fv_transDiffRef = distH0H1
    else:
      record.isProcessed = False
      st = "The record {} have just one reference measurments to process  the reference of transmittance calculation. Number of H measurments = {} (need to be > 1)".format(record.id,len(TrefA))
      LO.l_war(st)
      record.add_toLog(st)
  else:
    record.isProcessed = False
    st = "The record {} have doesn't all spectrum measurments to process the transmittance calculation. Number of I measurments = {} (need to be > 0). Number of H measurments = {} (need to be > 0).".format(record.id,len(TtarAi),len(TrefA))
    LO.l_war(st)
    record.add_toLog(st)
  return record

##############################################
# Record to CSV
##############################################
def leafspectra_record_to_csv(record):
  if TO.create_directory(record.fv_processedPath):
    c,l,r = leafspectra_record_to_csv_values(record)
    TO.write_in_csv(record.fv_processedPath+'/all.csv',c)
    TO.write_in_csv(record.fv_processedPath+'/leaves.csv',l)
    TO.write_in_csv(record.fv_processedPath+'/ref.csv',r)

def leafspectra_record_to_csv_values(record):
  dfrra = TO.from_series_to_dataframe(record.fv_reflecAverage)
  dfrrs = TO.from_series_to_dataframe(record.fv_reflecStadDev)
  dfrta = TO.from_series_to_dataframe(record.fv_transAverage)
  dfrts = TO.from_series_to_dataframe(record.fv_transStadDev)
  
  c = []
  c.append(["record_id","sample_id","scientific_name","date_measured","measured_by","spectroradiometer_start_time","spectroradiometer_id","instrumentation_id","leaf_side_measured","reflectance_transmittance","wavelength","R_T_Average","R_T_STD"])
  if not dfrra.empty:
    for index, row in dfrra.iterrows():
      c.append(record.to_csv_all()+["reflectance",row[0],row[1],dfrrs.iloc[index][1]])
  if not dfrta.empty:
    for index, row in dfrta.iterrows():
      c.append(record.to_csv_all()+["transmittance",row[0],row[1],dfrts.iloc[index][1]])
    
  l = []
  l.append(["record_id","sample_id","file_name","leaf_number","leaf_side_measured","reflectance-transmittance","wavelength","raw_value","calculated_value"])
  for measurement in record.fv_measurements:
    reflectance = measurement.reflectance
    if not reflectance.empty:
      df = TO.from_series_to_dataframe(reflectance)
      for index, row in df.iterrows():
        dft = TO.from_series_to_dataframe(measurement.spectre.measurement)
        l.append([record.id,record.fv_sample_id]+measurement.to_csv_leaf()+["reflectance",row[0],dft.iloc[index][1],row[1]])
    transmittance = measurement.transmittance
    if not transmittance.empty:
      df = TO.from_series_to_dataframe(transmittance)
      for index, row in df.iterrows():
        dft = TO.from_series_to_dataframe(measurement.spectre.measurement)
        l.append([record.id,record.fv_sample_id]+measurement.to_csv_leaf()+["transmittance",row[0],dft.iloc[index][1],row[1]])
  r = []
  r.append(["record_id","sample_id","propertie","wavelength","relative_value"])
  if not record.fv_reflecRef.empty:
    df = TO.from_series_to_dataframe(record.fv_reflecRef)
    for index, row in df.iterrows():
      r.append([record.id,record.fv_sample_id,'stray_light_vs_reference',row[0],row[1]])
  if not record.fv_reflecDiffRef.empty:
    df = TO.from_series_to_dataframe(record.fv_reflecDiffRef)
    for index, row in df.iterrows():
      r.append([record.id,record.fv_sample_id,'reflectance_reference',row[0],row[1]])
  if not record.fv_transDiffRef.empty:
    df = TO.from_series_to_dataframe(record.fv_transDiffRef)
    for index, row in df.iterrows():
      r.append([record.id,record.fv_sample_id,'transmittance_reference',row[0],row[1]])
  return c,l,r


##############################################
# Record to plot
##############################################
def plots_leafspectra_records(rec):
  for record in rec.records[:]:
    if record.isProcessed == True:
      LO.l_info('Start prepare plots data for record {}'.format(record.id))
      TOP.get_leafspectra_record_plot(record)
      if TOP.get_leafspectra_record_leaves_plot(record):
        record.leaves_plot = PA.CaboWebsite+''+record.project_name+'/spectra/processed/'+record.fv_working_folder+'/'+record.fv_sample_id+'/'+record.fv_sample_id+'_leaves.png'
      else:
        record.isProcessed = False
        s = 'The record id {} is incomplete all leaves are not available'.format(record.id)
        LO.l_war(s)
        record.add_toLog(s)
  return rec
  
##############################################
## Update records
##############################################
def update_leafspectra_records(rec):
  """
  This parallelisation of process_record
  """
  """
  wraps = []
  for record in rec.records:
    b = update_leafspectra_record(record)
    if b:
      wraps.append(b)
  return wraps
      
  """
  # parallelisation here
  output = mp.Queue()
  pool = mp.Pool(processes=PA.NumberOfProcesses)
  results = [pool.apply_async(update_leafspectra_record, args=(record,)) for record in rec.records[:]]
  pool.close()
  pool.join()
  spectrum = LeafSpectrum()
  for r in results:
    record = r.get()
    if record:
      spectrum.add_record(record)
  return spectrum
  
def update_leafspectra_record(record):
  """Update a leaf spectra record
  This function take a leafspectra record object and return a processed leafspectra record processed object
  """
  if record.isProcessed:
    LO.l_info('Update record {}'.format(record.id))
    keyValues = FO.get_Keys_from_DataNames(record.form_id,['record_is_calculated', 'calculated_record_link'])
    if record.leaves_plot == '':
      record.leaves_plot = 'http://data.caboscience.org/field-data/projects/2018-Girard-MSc-UdeM/spectra/processed/'
    obj = TOFA.get_record(record.id)
    obj['record']['form_values'][keyValues['record_is_calculated']]= 'yes'
    obj['record']['form_values'][keyValues['calculated_record_link']]= record.leaves_plot
    TOFA.fulcrum_update_record(""+record.id+"",obj)
  return record



##############################################
# Spectrum Data Logs
##############################################
def print_log_records(rec):
  for record in rec.records[:]:
    status_value = TO.get_record_status_value(record.status)
    if status_value>1:
      extract_log_record(record)
    
def extract_log_record(record):
  if record.fv_processedPath != '':
    TO.create_directory(record.fv_processedPath+'')
    TO.string_to_file(record.fv_processedPath+'/'+record.fv_sample_id+'_log.txt','{}'.format(record.logInfo))
  else:
    #PA.ProjectWebsitePath+'Rec_without_processedPath'
    LO.l_war('no fv_processedPath for record {}'.format(record.id))
