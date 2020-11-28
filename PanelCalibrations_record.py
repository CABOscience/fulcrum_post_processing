#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
from . import parameters as PA
from . import records as RE
from . import tools as TO
from . import tools_plots as TOP
from . import logs as LO
from . import PanelCalibrations_measurements as PCM
from . import SpectroscopyPanels_record as SPR

# System
import os, sys
import multiprocessing as mp
# Spectroscopy
#import specdal
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

class PanelCalibrations(RE.Records):
  '''
  This is just a comment
  '''

class PanelCalibration(RE.Record):
  def __init__(self, record):
    super(PanelCalibration,self).__init__(record.altitude, record.assigned_to, record.assigned_to_id, record.client_created_at, record.client_updated_at, record.course, record.created_at, record.created_by, record.created_by_id, record.created_duration, record.created_location, record.edited_duration, record.form_id, record.form_name, record.form_values, record.horizontal_accuracy, record.id, record.latitude, record.longitude, record.project_id, record.speed, record.status, record.updated_at, record.updated_by, record.updated_by_id, record.updated_duration, record.updated_location, record.version, record.vertical_accuracy, record.project_name)
    self.fv_approved_by = '' 
    self.fv_base_file_name = '' #
    self.fv_calibration = SPR.get_empty_calib()
    self.fv_cleaning = ''
    self.fv_computer = '' #
    self.fv_computer_type = '' 
    self.fv_date_approved = '' 
    self.fv_date_deleted = '' 
    self.fv_date_measured = '' #
    self.fv_date_published = '' 
    self.fv_date_rejected = '' 
    self.fv_date_submitted = '' 
    self.fv_date_verified = '' 
    self.fv_deleted_by = '' 
    self.fv_event_remarks = '' 
    self.fv_hidden_variables = '' 
    self.fv_instrumentation_id = '' 
    self.fv_instrumentation_type = '' 
    self.fv_manufacturer_short_name = '' 
    self.fv_manufacturer_short_name_sphere = '' 
    self.fv_measured_by = '' #
    self.fv_measurements = '' 
    self.fv_measurements_raw = '' 
    self.fv_number_of_measurements = '' 
    self.fv_number_of_rejections = '' 
    self.fv_number_of_replicate = '' 
    self.fv_number_of_scans = '' 
    self.fv_panel_photos = ''
    self.fv_parent_directory = '' #
    self.fv_protocol_url = '' 
    self.fv_published_by = '' 
    self.fv_reference_panel = '' #
    self.fv_reference_panel_id = '' 
    self.fv_rejected_by = '' 
    self.fv_serial_number = '' 
    self.fv_spectral_measurements_visibility = '' 
    self.fv_spectroradiometer_id = '' #
    self.fv_spectroradiometer_start_time = '' #
    self.fv_spectrum_number_current = '' #
    self.fv_submitted_by = '' 
    self.fv_target_panel = '' #
    self.fv_target_panel_id = '' 
    self.fv_time_measured = '' #
    self.fv_verified_by = '' 
    self.fv_working_folder = '' #
    self.fv_reflecAverage = pd.Series()
    self.fv_reflecDiffRef = pd.Series()
    self.fv_reflecReplicates  = {}
    self.fv_reflecRef     = pd.Series()
    self.fv_reflecStadDev = pd.Series()
    self.fv_transAverage  = pd.Series()
    self.fv_transDiffRef  = pd.Series()
    self.fv_transReplicates  = {}
    self.fv_transStadDev  = pd.Series()
    # need to be check
    self.fv_processedPath = "" # it will be: PA.PanelCalibPath+''+pname+'/'+wf+'/'
    self.fv_sourcePath = "" # it will be: PA.PanelCalibPath+''+pname+'/'+wf+'/'
    self.fv_extFile = ''
    self.fv_measureType = ''
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
    self.replicate_plot = ''
    self.wvlMax = ''
    self.wvlMin = ''
    
  def to_csv_all(self):
    return [self.id, self.fv_date_measured, self.fv_measured_by, self.fv_spectroradiometer_start_time, self.fv_spectroradiometer_id, self.fv_instrumentation_id]

  def to_info(self):
    return [self.id, self.fv_date_measured, self.fv_measured_by]

  def whoami(self):
    return type(self).__name__
  
def extract_panel_calibrations_record(record):
  """ This will extract a plant panel record data from a record "form values"
  
  :param arg1: a SpectroscopyPanel to be tested
  :type arg1: SpectroscopyPanel

  :return: an updated record if it is validated or the record
  :rtype: SpectroscopyPanel
  """
  LO.l_info('Start extract panel calibration recordid {}'.format(record.id))
  rv  = record.form_values

  if 'base_file_name' in rv \
    and 'computer' in rv \
    and 'date_measured' in rv \
    and 'measured_by' in rv \
    and 'parent_directory' in rv \
    and 'reference_panel' in rv \
    and 'spectroradiometer_id' in rv \
    and 'spectroradiometer_start_time' in rv \
    and 'target_panel' in rv \
    and 'time_measured' in rv \
    and 'working_folder' in rv :

    if 'approved_by' in rv: record.fv_approved_by = rv['approved_by']
    if 'base_file_name' in rv: record.fv_base_file_name = rv['base_file_name']
    if 'cleaning' in rv: record.fv_cleaning = rv['cleaning']
    if 'computer' in rv: record.fv_computer = rv['computer']
    if 'computer_type' in rv: record.fv_computer_type = rv['computer_type']
    if 'date_approved' in rv: record.fv_date_approved = rv['date_approved']
    if 'date_deleted' in rv: record.fv_date_deleted = rv['date_deleted']
    if 'date_measured' in rv: record.fv_date_measured = rv['date_measured']
    if 'date_published' in rv: record.fv_date_published = rv['date_published']
    if 'date_rejected' in rv: record.fv_date_rejected = rv['date_rejected']
    if 'date_submitted' in rv: record.fv_date_submitted = rv['date_submitted']
    if 'date_verified' in rv: record.fv_date_verified = rv['date_verified']
    if 'deleted_by' in rv: record.fv_deleted_by = rv['deleted_by']
    if 'event_remarks' in rv: record.fv_event_remarks = rv['event_remarks']
    if 'hidden_variables' in rv: record.fv_hidden_variables = rv['hidden_variables']
    if 'instrumentation_id' in rv: record.fv_instrumentation_id = rv['instrumentation_id']
    if 'instrumentation_type' in rv: record.fv_instrumentation_type = rv['instrumentation_type']
    if 'manufacturer_short_name' in rv: record.fv_manufacturer_short_name = rv['manufacturer_short_name']
    if 'manufacturer_short_name_sphere' in rv: record.fv_manufacturer_short_name_sphere = rv['manufacturer_short_name_sphere']
    if 'measured_by' in rv: record.fv_measured_by = rv['measured_by']
    if 'measurements' in rv: record.fv_measurements_raw = rv['measurements']
    if 'number_of_measurements' in rv: record.fv_number_of_measurements = rv['number_of_measurements']
    if 'number_of_rejections' in rv: record.fv_number_of_rejections = rv['number_of_rejections']
    if 'number_of_replicate' in rv: record.fv_number_of_replicate = rv['number_of_replicate']
    if 'number_of_scans' in rv: record.fv_number_of_scans = rv['number_of_scans']
    if 'panel_photos' in rv: record.fv_panel_photos = rv['panel_photos']
    if 'parent_directory' in rv: record.fv_parent_directory = rv['parent_directory']
    if 'protocol_url' in rv: record.fv_protocol_url = rv['protocol_url']
    if 'published_by' in rv: record.fv_published_by = rv['published_by']
    if 'reference_panel' in rv: record.fv_reference_panel = rv['reference_panel']
    if 'reference_panel_id' in rv: record.fv_reference_panel_id = rv['reference_panel_id']
    if 'rejected_by' in rv: record.fv_rejected_by = rv['rejected_by']
    if 'serial_number' in rv: record.fv_serial_number = rv['serial_number']
    if 'spectral_measurements_visibility' in rv: record.fv_spectral_measurements_visibility = rv['spectral_measurements_visibility']
    if 'spectroradiometer_id' in rv: record.fv_spectroradiometer_id = rv['spectroradiometer_id']
    if 'spectroradiometer_start_time' in rv: record.fv_spectroradiometer_start_time = rv['spectroradiometer_start_time']
    if 'spectrum_number_current' in rv: record.fv_spectrum_number_current = rv['spectrum_number_current']
    if 'submitted_by' in rv: record.fv_submitted_by = rv['submitted_by']
    if 'target_panel' in rv: record.fv_target_panel = rv['target_panel']
    if 'target_panel_id' in rv: record.fv_target_panel_id = rv['target_panel_id']
    if 'time_measured' in rv: record.fv_time_measured = rv['time_measured']
    if 'verified_by' in rv: record.fv_verified_by = rv['verified_by']
    if 'working_folder' in rv: record.fv_working_folder = rv['working_folder']
    
    rpd = record.fv_parent_directory
    if rpd.startswith("PANEL-CALIBRATIONS"):
      record.fv_parent_directory = rpd[19:]
    record.fv_processedPath = PA.WebsitePath+'PanelCalibrationsCalculated'+'/'+record.fv_parent_directory+''+record.fv_working_folder+''
    record.fv_sourcePath = PA.PanelCalibPath+''+record.fv_parent_directory+''+record.fv_working_folder+''
    if record.fv_manufacturer_short_name_sphere == 'SVC':
      record.fv_extFile = '.sig'
      record.fv_measureType = 'tgt_counts'
    record.fv_measurements = PCM.extract_panel_calibrations_measurements(record.fv_measurements_raw)
    validate_panel_calibrations_measurements(record)
    update_panel_calibrations_measurements(record)

  else:
    tab = ['base_file_name', 'computer', 'date_measured', 'measured_by', 'parent_directory', 'reference_panel', 'spectroradiometer_id', 'spectroradiometer_start_time', 'target_panel', 'time_measured', 'working_folder']
    s = ""
    for t in tab:
      if not t in rv:
        if s:
          s+=', '
        s += t
    record.isValid = False
    sPnoR = 'Project {}, the record id {} will not be used because it has no {}.'.format(record.project_name,record.id,s)
    LO.l_war(sPnoR)
    record.add_toLog(sPnoR)

def validate_panel_calibrations_measurements(record):
  """ This will validate the panel calibrations record measurments
  
  :param arg1: a LeafSpectra to be tested
  :type arg1: LeafSpectra

  :return: True if is a valid record False if it's not a LeafSpectra record
  :rtype: boolean (True,False)
  """
  ext = record.fv_extFile
  mts = record.fv_measurements.measurements
  rid = record.id
  rsp = record.fv_sourcePath
  
  measurmentsDone = True
  LO.l_debug('Start validate record {} measurements'.format(rid))
  for i, mt in enumerate(mts):
    for file_name in mt.files_name[:]:
      if file_name:
        fName = rsp+file_name+''+ext
        mt.files_path.append(fName)
        if not TO.file_is_here(fName):
          measurmentsDone = False
          nFa = "The record id {} has not {} available.".format(rid,fName)
          LO.l_war(nFa)
          record.add_toLog(nFa)
    if len(mt.files_path) < 3:
      nFp = "The record id {} has not at least 3 records available for measurment {}.".format(rid,fName,i)
      LO.l_war(nFa)
      record.add_toLog(nFa)
      record.isValid = False
  if not measurmentsDone:
    record.isValid = False

def update_panel_calibrations_measurements(record):
  """ This will link metadata and data extracted from files of a panel calibration record
  It will also prepare "interpolated_files" form processing
  
  :param arg1: a panel calibration to be tested
  :type arg1:  PanelCalibration
  
  :return: a tested panel calibration (with measurments if test is good)
  :rtype: PanelCalibration
  """
  if record.isValid:
    # from record object
    pname = record.project_name
    rid   = record.id
    # from leaf spectra object
    ext   = record.fv_extFile
    mts   = record.fv_measurements.measurements

    measureType = record.fv_measureType
    wf          = record.fv_working_folder
    vmax = -1
    vmin = -1
    
    measurmentsDone = True
    for mt in mts[:]:
      for i, fName in enumerate(mt.files_path):
        if fName and TO.file_is_here(fName):
          LO.l_debug("\tStart spectre extraction for {}".format(fName))
          spect = TO.create_spectrum(fName,measureType)
          mt.spectres.append(spect)
          mt.spectres[i].interpolate(method='cubic')
          wvl_max = mt.spectres[i].metadata['wavelength_range'][1]
          wvl_min = mt.spectres[i].metadata['wavelength_range'][0]
          if vmax == -1 or wvl_max < vmax:
            vmax = wvl_max
          if vmin == -1 or wvl_min > vmin:
            vmin = wvl_min
          TO.create_directory(record.fv_processedPath+'/interpolated_files/')
          spectreProcessed = record.fv_processedPath+'/interpolated_files/'+mt.files_name[i]+ext+'.txt'
          s = '{}'.format(mt.spectres[i])
          s += '###############\nALL DATA\n###############\n'
          with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            s += '{}'.format(mt.spectres[i].measurement)
          TO.string_to_file(spectreProcessed,'{}'.format(s))
        else:
          LO.l_war("The record id {} has not {} available.".format(rid,fName))
          record.add_toLog("The record id {} has not {} available.".format(rid,fName))
          measurmentsDone = False
       # Average and Standard Deviation
      arr     = np.array([spectre.measurement for spectre in mt.spectres])
      arrIndex= np.array(mt.spectres[0].measurement.index)
      arrMean = np.mean(arr, axis=0)
      arrStd  = np.std(arr, axis=0, ddof=1)
      
      reflecAverage = pd.Series(arrMean, index=arrIndex, name="reflectance_average")
      reflecAverage.index.name = 'wavelength'
      mt.reflecAverage = reflecAverage
      reflecStadDev = pd.Series(arrStd, index=arrIndex, name="reflectance_standard_deviation")
      reflecStadDev.index.name = 'wavelength'
      mt.reflecStadDev = reflecStadDev

    if not measurmentsDone:
      LO.l_war("The record id {} will not be used because it has not all its spectre available.".format(rid))
      record.add_toLog("The record id {} will not be used because it has not all its spectre available.".format(rid))
      record.isValid = False
    record.wvlMax = vmax
    record.wvlMin = vmin
  return record

def link_panel_calibrations_records_and_calibration(spectroPanels,recs):
  """ This will link calibration and a leaf spectra record
  
  :param arg1: a Calibrations list
  :type arg1: Calibrations

  :param arg2: a fulcrum measurements list
  :type arg2: LeafSpectra

  :return: True if a calibration has been found, false if the calibration has not been found
  :rtype: boolean (True/False)
  """
  panelCalibrations = PanelCalibrations()
  for record in recs.records[:]:
    if record.isValid:
      rID     = record.id
      panel_id= record.fv_reference_panel[0]['record_id']
      
      LO.l_info('panel id is>{}'.format(panel_id))
      
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
    panelCalibrations.add_record(record)
  return panelCalibrations


##############################################
# Get Panel calibrations
##############################################
def get_panel_calibrations_from_records(recs):
  panelCalibrations = PanelCalibrations()
  for panelCalibration_raw in recs.records:
    panelCalibration = PanelCalibration(panelCalibration_raw)
    extract_panel_calibrations_record(panelCalibration)
    if panelCalibration.isValid:
      panelCalibrations.add_record(panelCalibration)
      st = 'The panel calibration record id {} is complete for processing'.format(panelCalibration.id)
      LO.l_debug(st)
      panelCalibration.add_toLog(st)
    else:
      st = 'The panel calibration record id {} is incomplete and will not be used'.format(panelCalibration.id)
      LO.l_war(st)
      panelCalibration.add_toLog(st)
  return panelCalibrations

##############################################
# Load Records
##############################################
# Load Panel calibrations from Panel calibrations Records File
def load_panel_calibrations_from_webhook():
  if TO.file_is_here(PA.PanelCalibrationsFormFile):
    records = RE.load_webhook_records_with_formID_from_formFile(PA.PanelCalibrationsFormFile)
    return get_plants_from_records(records)
  else:
    return RE.error_load(PA.PanelCalibrationsFormFile)

# Load Panel calibrations from Panel calibrations Records File
def load_panel_calibrations_from_records_file():
  if TO.file_is_here(PA.PanelCalibrationsRecordsFile):
    records = RE.load_records_from_json(PA.PanelCalibrationsRecordsFile)
    return get_panel_calibrations_from_records(records)
  else:
    return RE.error_load(PA.PlantsRecordsFile)

# Load Panel calibrations from fulcrum
def load_panelCalibrations_from_fulcrum():
  RE.backup_records_from_forms()
  return load_panel_calibrations_from_records_file()

# Load Panel Calibrations from form
def load_panelCalibrations_from_form():
  if TO.file_is_here(PA.PlantsFormFile):
    panelCalibrations_form = FO.load_form_from_json_file(PA.PlantsFormFile)
    recs = RE.load_records_from_fulcrum(panelCalibrations_form)
    return get_panelCalibrations_from_records(recs)
  else:
    return RE.error_load(PA.PlantsRecordsFile)

# Load Panel calibrations
def load_panelCalibrations():
  pls = load_panel_calibrations_from_records_file()
  if len(pls) < 1:
    pls = load_panelCalibrations_from_form()
  if len(pls) < 1:
    pls = load_panelCalibrations_from_fulcrum()
  return pls

##############################################
## Process record
##############################################

def process_panel_calibrations_records(rec):
  # parallelisation here
  
  output = mp.Queue()
  pool = mp.Pool(processes=3)
  results = [pool.apply_async(process_record, args=(record,)) for record in rec.records[:]]
  pool.close()
  pool.join()
  panelCalibrations = PanelCalibrations()
  for r in results:
    record = r.get()
    if record:
      panelCalibrations.add_record(record)
  return panelCalibrations

  """
  for record in rec.records[:]:
    process_record(record)
  return PanelCalibrations()
  """

def process_record(record):
  LO.l_info('Start prepare panel calibration data for record {}'.format(record.id))
  if record.isValid:
    boo = panel_calibration_calculation(record)
    if boo:
      record.isProcessed = True
  return record

## Panel Calibration Calculations
########################
def panel_calibration_calculation(record):
  boo = True
  
  wvlMax = record.wvlMax
  wvlMin = record.wvlMin
  reflTargets, reflStrays, reflRefs = ([] for i in range(3))
  transRefAll, transTargets = ([] for i in range(2))
  mts   = record.fv_measurements.measurements
  
  numberOfC=1
  for mt in mts[:]:
    # Reflectance
    if 'A:' in mt.sphere_configuration:
      reflRefs.append(mt)
      if len(reflRefs)==0:
        LO.l_war("the record {} doesn't have any reference. The wvlMax and wvlMin used will come from calibration".format(record.id))
    if 'B:' in mt.sphere_configuration:
      reflStrays.append(mt)
    if 'C:' in mt.sphere_configuration:
      reflTargets.append(mt)
      record.fv_reflecReplicates["{}".format(numberOfC)] = mt
      numberOfC+=1


  # REFLECTANCE CALCULATION
  if len(reflStrays)>0 and len(reflRefs)>0 and len(reflTargets)>0:
    # Calibration
    calib = record.fv_calibration.spectre.measurement.sort_index().loc[wvlMin:wvlMax]
    # (A - B):
    divisorsTar = reflRefs[0].reflecAverage.sub(reflStrays[0].reflecAverage)
    # Calculations per leafs:
    for reflTarget in reflTargets:
      # (C - B):
      dividendsTar = reflTarget.reflecAverage.sub(reflStrays[0].reflecAverage)
      # [ (C - B) ÷ (A - B) ]
      divisionTar = dividendsTar.div(divisorsTar)
      # ([ (C - B) ÷ (A - B) ]) × calib.refl
      mseries = TO.get_monotonic_series(divisionTar)
      for i in range(len(mseries)):
        mserie = mseries[i].sort_index().loc[wvlMin:wvlMax]
        for ind, row in mserie.items():
          mserie.set_value(ind,row)
        mseries[i] = mserie
        i+=1
      reflectance = pd.concat(mseries)
      reflTarget.reflectance= reflectance
      #reflTarget.reflectance= divisionTar

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
    if len(reflRefs) > 3:
      distA0A1 = reflRefs[len(reflRefs)-1].reflecAverage.div(reflRefs[0].reflecAverage)
      record.fv_reflecDiffRef = distA0A1
    else:
      LO.l_war("the record {} haven't the right number of reference measurments to process the reference of reflectance calculation.".format(record.id))
    # Calculation of (B0/A0):
    distB0A1 = pd.Series()
    if len(reflStrays) > 0 and len(reflRefs) > 0 :
      distB0A1 = reflStrays[0].reflecAverage.div(reflRefs[0].reflecAverage)
      record.fv_reflecRef = distB0A1
    else:
      LO.l_war("the record {} have just one reference measurments to process the stray light vs reference.".format(record.id))
  else:
    boo = False
    LO.l_err("the record {} doesn't have all spectrum measurments to process the reflectance calculation.".format(record.id))

  return boo

##############################################
# Record to plot
##############################################
def plots_panel_calibrations_records(recs):
  panelCalibrations = PanelCalibrations()  
  for record in recs.records[:]:
    if record.isProcessed == True:
      LO.l_info('Start prepare plots data for record {}'.format(record.id))
      TOP.get_panel_calibrations_record_plot(record)
      TOP.get_panel_calibrations_record_measurments_plot(record)
      LO.l_info("{}".format(record.replicate_plot))
    if not record.isProcessed:
        s = 'The record id {} is incomplete all leaves are not available'.format(record.id)
        LO.l_war(s)
        record.add_toLog(s)
    panelCalibrations.add_record(record) 
  return panelCalibrations


