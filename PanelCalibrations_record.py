#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
import parameters as PA
import records as RE
import tools as TO
import logs as LO
import SpectroscopyPanels_calibrations as SPC
import LeafSpectra_measurements as LSP

# System
import os, sys
import multiprocessing as mp
# Spectroscopy
import specdal
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

class PanelCalibrations(object):
  def __init__(self):
    self.records=[]
    
  def add_record(self,PanelCalibration):
    self.records.append(PanelCalibration)


class PanelCalibration(object):
  def __init__(self, record, bfn='',dm='',ii='',lltp='',lsm='',manu='',mb='',measurements='',paID='',pdir='',pm='',sai='',sn='',spi='',stt='',wf=''):
    super(PanelCalibration,self).__init__(record.altitude, record.assigned_to, record.assigned_to_id, record.client_created_at, record.client_updated_at, record.course, record.created_at, record.created_by, record.created_by_id, record.created_duration, record.created_location, record.edited_duration, record.form_id, record.form_values, record.horizontal_accuracy, record.id, record.latitude, record.longitude, record.project_id, record.speed, record.status, record.updated_at, record.updated_by, record.updated_by_id, record.updated_duration, record.updated_location, record.version, record.vertical_accuracy, record.project_name)
    self.fv_approved_by = appby
    self.fv_base_file_name = bfn #
    self.fv_branch_number = bran
    self.fv_computer = com #
    self.fv_computer_type = comt
    self.fv_date_approved = dapp
    self.fv_date_deleted = ddel
    self.fv_date_measured = dmea #
    self.fv_date_published = dpub
    self.fv_date_rejected = drej
    self.fv_date_submitted = dsub
    self.fv_date_verified = dver
    self.fv_deleted_by = delb
    self.fv_event_remarks = ever
    self.fv_file_name = fna
    self.fv_file_name_value = fnav
    self.fv_hidden_variables = hvar
    self.fv_instrumentation_id = insi
    self.fv_instrumentation_type = inst
    self.fv_manufacturer_short_name = msn
    self.fv_manufacturer_short_name_sphere = msns
    self.fv_measured_by = meab #
    self.fv_measurement_id = meai #
    self.fv_measurement_remarks = mear
    self.fv_measurements = mea
    self.fv_number_of_measurements = nummea
    self.fv_number_of_rejections = numrej
    self.fv_panel_number = pnumber
    self.fv_panel_photos = pphoto
    self.fv_parent_directory = pardirec #
    self.fv_primary_light_port = plp
    self.fv_protocol_url = prou
    self.fv_published_by = pubb
    self.fv_reference_panel = refp #
    self.fv_reference_panel_id = refpi
    self.fv_reflectance_port = reflp
    self.fv_rejected_by = rejb
    self.fv_replicate_number = repn
    self.fv_serial_number = serinum
    self.fv_spectral_measurements_visibility = smv
    self.fv_spectroradiometer_id = spei #
    self.fv_spectroradiometer_start_time = spest #
    self.fv_spectrum_number = spen
    self.fv_sphere_configuration = sphc
    self.fv_submitted_by = subb
    self.fv_target_panel = tarp #
    self.fv_target_panel_id = tarpi
    self.fv_target_type = tart
    self.fv_time_measured = timm #
    self.fv_transmission_port = transp
    self.fv_verified_by = verb
    self.fv_working_folder = worf #
    self.fv_reflecAverage = pd.Series()
    self.fv_reflecDiffRef = pd.Series()
    self.fv_reflecLeaves  = {}
    self.fv_reflecRef     = pd.Series()
    self.fv_reflecStadDev = pd.Series()
    self.fv_transAverage  = pd.Series()
    self.fv_transDiffRef  = pd.Series()
    self.fv_transLeafs    = {}
    self.fv_transStadDev  = pd.Series()
    # need to be check
    self.fv_processedPath = PA.ProjectWebsitePath+self.fv_serial_number+'/spectra/processed/'+self.working_folder+'/'+self.sample_id
  
  def __str__(self):
    return '>{} - {}'.format(self.id, self.form_id)

  def to_csv(self):
    return [self.id, self.sample_id, self.scientific_name, self.date_measured, self.measured_by, self.spectroradiometer_start_time, self.spectroradiometer_id, self.instrumentation_id, self.leaf_side_measured]

  def to_info(self):
    return [self.id,self.sample_id,self.scientific_name,self.date_measured,self.measured_by]

  def whoami(self):
    return type(self).__name__
    


##############################################
# Extract Record
##############################################
def load_panelcalibrations_webhook_Records(calibrations,projects):
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
        LO.l_info('Start update record {} with calibration and date {}'.format(record.id,record.date_measured))
        if link_leafspectra_record_and_calibration(calibrations,record):
          LO.l_war('The record {} is complete for processing'.format(record.id))
          spectrum.add_record(record)
        else:
          LO.l_war('The record {} will not be used'.format(record_raw.id))
      else:
        LO.l_war('The record {} will not be used'.format(record_raw.id))
  return spectrum


def load_panelcalibrations_Records(calibrations,projects):
  spectrum = LeafSpectrum()
  fileName = PA.LeafSpectraRecordsFile
  rec = RE.load_records_from_json(fileName,projects)
  # parallelisation here
  output = mp.Queue()
  wraps = []
  pool = mp.Pool(processes=3)
  results = [pool.apply_async(add_Record_in_spectrum, args=(calibrations,record_raw)) for record_raw in rec.records[:]]
  pool.close()
  pool.join()
  for r in results:
    b = r.get()
    if b:
      wraps.append(b)
  
  # parallelisation here
  output2 = mp.Queue()
  wraps2 = []
  if len(wraps)>0:
    pool2 = mp.Pool(processes=3)
    results2 = [pool2.apply_async(update_leafspectra_record_measurements, args=(record_raw,)) for record_raw in wraps[:]]
    pool2.close()
    pool2.join()
    for r2 in results2:
      b2 = r2.get()
      if b2:
        wraps2.append(b2)
    if len(wraps2)>0:
      for wrap in wraps2[:]:
        spectrum.add_record(wrap)
  return spectrum

def add_Record_in_spectrum_wrapper(tab):
  return add_Record_in_spectrum(tab[0],tab[1],tab[2])
    
def add_Record_in_PanelCalibrations(calibrations,record_raw):
  record = LeafSpectra(record_raw)
  if validate_leafspectra_record(calibrations,record):
    #LO.l_info('The record.id {} is complete for processing'.format(record.id))
    return record
  #else:
  #  LO.l_war('The record.id {} is incomplete and will not be used'.format(record.id))

def validate_panel_calibrations_record(calibrations,record):
  boo = True
  if not extract_leafspectra_record(record):
    boo = False
  if boo and not link_leafspectra_record_and_calibration(calibrations,record):
    boo = False
  if boo and not validate_leafspectra_record_measurements(record):
    boo = False
  return boo

def extract_panel_calibrations_record(record):
  LO.l_info('Start extract panel calibration recordid {}'.format(record.id))
  rv  = record.form_values

  if 'base_file_name' in rv \
    and 'computer' in rv \
    and 'date_measured' in rv \
    and 'measured_by' in rv \
    and 'measurement_id' in rv \
    and 'parent_directory' in rv \
    and 'reference_panel' in rv \
    and 'spectroradiometer_id' in rv \
    and 'spectroradiometer_start_time' in rv \
    and 'target_panel' in rv \
    and 'time_measured' in rv \
    and 'working_folder' in rv :

    if 'approved_by' in rv: record.fv_approved_by = rv['approved_by']
    if 'base_file_name' in rv: record.fv_base_file_name = rv['base_file_name']
    if 'branch_number' in rv: record.fv_branch_number = rv['branch_number']
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
    if 'file_name' in rv: record.fv_file_name = rv['file_name']
    if 'file_name_value' in rv: record.fv_file_name_value = rv['file_name_value']
    if 'hidden_variables' in rv: record.fv_hidden_variables = rv['hidden_variables']
    if 'instrumentation_id' in rv: record.fv_instrumentation_id = rv['instrumentation_id']
    if 'instrumentation_type' in rv: record.fv_instrumentation_type = rv['instrumentation_type']
    if 'manufacturer_short_name' in rv: record.fv_manufacturer_short_name = rv['manufacturer_short_name']
    if 'manufacturer_short_name_sphere' in rv: record.fv_manufacturer_short_name_sphere = rv['manufacturer_short_name_sphere']
    if 'measured_by' in rv: record.fv_measured_by = rv['measured_by']
    if 'measurement_id' in rv: record.fv_measurement_id = rv['measurement_id']
    if 'measurement_remarks' in rv: record.fv_measurement_remarks = rv['measurement_remarks']
    if 'measurements' in rv: record.fv_measurements = rv['measurements']
    if 'number_of_measurements' in rv: record.fv_number_of_measurements = rv['number_of_measurements']
    if 'number_of_rejections' in rv: record.fv_number_of_rejections = rv['number_of_rejections']
    if 'panel_number' in rv: record.fv_panel_number = rv['panel_number']
    if 'panel_photos' in rv: record.fv_panel_photos = rv['panel_photos']
    if 'parent_directory' in rv: record.fv_parent_directory = rv['parent_directory']
    if 'primary_light_port' in rv: record.fv_primary_light_port = rv['primary_light_port']
    if 'protocol_url' in rv: record.fv_protocol_url = rv['protocol_url']
    if 'published_by' in rv: record.fv_published_by = rv['published_by']
    if 'reference_panel' in rv: record.fv_reference_panel = rv['reference_panel']
    if 'reference_panel_id' in rv: record.fv_reference_panel_id = rv['reference_panel_id']
    if 'reflectance_port' in rv: record.fv_reflectance_port = rv['reflectance_port']
    if 'rejected_by' in rv: record.fv_rejected_by = rv['rejected_by']
    if 'replicate_number' in rv: record.fv_replicate_number = rv['replicate_number']
    if 'serial_number' in rv: record.fv_serial_number = rv['serial_number']
    if 'spectral_measurements_visibility' in rv: record.fv_spectral_measurements_visibility = rv['spectral_measurements_visibility']
    if 'spectroradiometer_id' in rv: record.fv_spectroradiometer_id = rv['spectroradiometer_id']
    if 'spectroradiometer_start_time' in rv: record.fv_spectroradiometer_start_time = rv['spectroradiometer_start_time']
    if 'spectrum_number' in rv: record.fv_spectrum_number = rv['spectrum_number']
    if 'sphere_configuration' in rv: record.fv_sphere_configuration = rv['sphere_configuration']
    if 'submitted_by' in rv: record.fv_submitted_by = rv['submitted_by']
    if 'target_panel' in rv: record.fv_target_panel = rv['target_panel']
    if 'target_panel_id' in rv: record.fv_target_panel_id = rv['target_panel_id']
    if 'target_type' in rv: record.fv_target_type = rv['target_type']
    if 'time_measured' in rv: record.fv_time_measured = rv['time_measured']
    if 'transmission_port' in rv: record.fv_transmission_port = rv['transmission_port']
    if 'verified_by' in rv: record.fv_verified_by = rv['verified_by']
    if 'working_folder' in rv: record.fv_working_folder = rv['working_folder']
  else:
    tab = ['base_file_name', 'computer', 'date_measured', 'measured_by', 'measurement_id', 'parent_directory', 'reference_panel', 'spectroradiometer_id', 'spectroradiometer_start_time', 'target_panel', 'time_measured', 'working_folder']
    s = ""
    for t in tab:
      if not t in rv:
        if s:
          s+=', '
        s += t
    LO.l_war('Project {}, the record.id {} will not be used because it has no {}.'.format(record.project_name,record.id,s))
    return False

# validate the record link measurments
def validate_panel_calibrations_record_measurements(record_raw):
  manu= record_raw.manufacturer_short_name_sphere
  measurements=record_raw.measurements
  pname = record_raw.project_name
  rid = record_raw.id
  wf = record_raw.working_folder
  
  measurmentsDone = True
  #LO.l_info('Start validate record {} measurments'.format(record.id))
  for measurement in measurements:
    measureType = ""
    fName = PA.ProjectWebsitePath+''+pname+'/spectra/raw/'+wf+'/'+measurement.file_name+''
    ext = ''
    if manu == 'SVC':
      ext = '.sig'
      measureType ='tgt_counts'
    fName += ext
    measurement.file_path = fName
    if not TO.file_is_here(fName):
      measurmentsDone = False
  if not measurmentsDone:
    LO.l_war("The record.id {} will not be used because it has not all its spectre available.".format(rid))
  return measurmentsDone

# link metadata and data extracted from files
def update_leafspectra_record_measurements(record_raw):
  manu= record_raw.manufacturer_short_name_sphere
  measurements=record_raw.measurements
  pname = record_raw.project_name
  rid = record_raw.id
  wf = record_raw.working_folder
  measurmentsDone = True
  for measurement in measurements:
    measureType = ""
    fName = PA.ProjectWebsitePath+''+pname+'/spectra/raw/'+wf+'/'+measurement.file_name+''
    ext = ''
    if manu == 'SVC':
      ext = '.sig'
      measureType ='tgt_counts'
    fName += ext
    measurement.file_path = fName
    if TO.file_is_here(fName):
      #LO.l_info("\tStart spectre extraction for {}".format(fName))
      spect = specdal.Spectrum(filepath=fName, measure_type= measureType)
      measurement.spectre = spect
      measurement.spectre.interpolate(method='cubic')
      TO.create_directory(record_raw.processedPath+'/interpolated_files/')
      spectreProcessed = record_raw.processedPath+'/interpolated_files/'+measurement.file_name+ext+'.txt'
      s = '{}'.format(measurement.spectre)
      s += '###############\nALL DATA\n###############\n'
      with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        s += '{}'.format(measurement.spectre.measurement)
      TO.string_to_file(spectreProcessed,'{}'.format(s))
    else:
      LO.l_war("The record.id {} will not be used because it has not all its spectre available.".format(rid))
      measurmentsDone = False
  if measurmentsDone:
    return record_raw

def clean_measured_by(mb):
  st = ""
  if len(mb["choice_values"])>0:
    st += ', '.join(x for x in mb["choice_values"])
  elif len(mb["other_values"])>0:
    st += ', '.join(x for x in mb["other_values"])
  return st

def extract_measurements(measurements):
  measurementsInfo = []
  for measurement in measurements:
    cv = 'choice_values'
    fn, ln, lsm, sn, scsll, scssl, rps, tps = ("",)*8
    vs  = measurement['form_values']
    fn  = vs['file_name']
    if 'leaf_number'            in vs: ln = vs['leaf_number']
    if 'leaf_side_measured'     in vs: lsm = vs['leaf_side_measured']  
    if 'spectrum_number'        in vs: sn  = vs['spectrum_number']      
    if 'reflectance_port_svc'   in vs: rps = vs['reflectance_port_svc'][cv][0] 
    if 'transmission_port_svc'  in vs: tps = vs['transmission_port_svc'][cv][0]
    if 'sphere_configuration_svc_large_leaves' in vs: scsll = vs['sphere_configuration_svc_large_leaves'][cv][0]  # test if 'sphere_configuration_svc_large_leaves' here
    if 'sphere_configuration_svc_small_leaves.l_leaves' in vs: scssl = vs['sphere_configuration_svc_small_leaves.l_leaves'][cv][0]  # test if 'sphere_configuration_svc_large_leaves' here
    measurementsInfo.append(SP.make_SpectraMeasurements(fn, ln, lsm, sn, rps, tps, scsll, scssl))
  return measurementsInfo

##############################################
## Process record
##############################################

def process_panel_calibrations_records(rec):
  # parallelisation here
  output = mp.Queue()
  wraps = []
  pool = mp.Pool(processes=3)
  results = [pool.apply_async(process_record, args=(record,)) for record in rec.records[:]]
  pool.close()
  pool.join()
  for r in results:
    b = r.get()
    if b:
      wraps.append(b)
  
def process_record(record):
  LO.l_info('Start prepare spectrum data for record {}'.format(record.id))
  boo = calculate_leafspectra_record(record)
  if boo:
    LO.l_info('Start prepare csv files for record {}'.format(record.id))
    leafspectra_record_to_csv(record)
  '''
  # parallelisation here
  
  for record in rec.records[:]:
    #print '{}'.format(record.project_name)
    #if 'SWA-Warren' in record.project_name:
    #if 'a44016be-14a1-4b1a-8c56-c92086273442' in record.id:
    if '1ae1a8af-5abf-414d-bd48-8f97f09709f4' in record.id:
      LO.l_info('Start prepare spectrum data for record {}'.format(record.id))
      boo = calculate_leafspectra_record(record)
      print boo
      sys.exit(1)
      if boo:
        LO.l_info('Start prepare csv files for record {}'.format(record.id))
        leafspectra_record_to_csv(record)
  '''

## Panel Calibration Calculations
########################
def panel_calibration_calculation(record):
  boo = True
  
  pm = record.properties_measured
  pmB, pmR, pmT = (False for i in range(3))
  if 'both' in pm:
    pmB = True
  if 'both' in pm or 'reflectance' in pm:
    pmR = True
  if 'both' in pm or 'transmittance' in pm:
    pmT = True

  wvlMax = record.calibration.cMax
  wvlMin = record.calibration.cMin
  reflTargets, reflStrays, reflRefs = ([] for i in range(3))
  transRefAll, transTargets = ([] for i in range(2))
  
  for measurement in record.measurements:
    # Reflectance
    if 'A:' in measurement.sphere_configuration_svc_large_leaves:
      reflRefs.append(measurement)
      if len(reflRefs)>0:
        # set values max and min from the min of max wvl or max calibration data
        wvLO.l_max = reflRefs[0].spectre.metadata['wavelength_range'][1]
        wvLO.l_min = reflRefs[0].spectre.metadata['wavelength_range'][0]
        if wvLO.l_max < wvlMax:
          wvlMax = wvLO.l_max
        if wvLO.l_min > wvlMin:
          wvlMin = wvLO.l_min
      else:
        LO.l_war("the record {} doesn't have any reference. The wvlMax and wvlMin used will come from calibration".format(record.id))
    if 'B:' in measurement.sphere_configuration_svc_large_leaves:
      reflStrays.append(measurement) #B: No leaf
    if 'C:' in measurement.sphere_configuration_svc_large_leaves:
      leafNumber = measurement.leaf_number
      if leafNumber:
        reflTargets.append(measurement)
        record.reflecLeaves[leafNumber] = measurement
    #Transmission
    if 'D:' in measurement.sphere_configuration_svc_large_leaves:
      transRefAll.append(measurement) 
    if 'E:' in measurement.sphere_configuration_svc_large_leaves:
      leafNumber = measurement.leaf_number
      if leafNumber:
        transTargets.append(measurement)
        record.transLeafs[leafNumber] = measurement
  
  # Fix the range, if not use of calibration
  if not pmR:
    wvlMax = transRefAll[0].spectre.metadata['wavelength_range'][1]
    wvlMin = transRefAll[0].spectre.metadata['wavelength_range'][0]

  # REFLECTANCE CALCULATION
  # https://www.protocols.io/view/measuring-spectral-reflectance-and-transmittance-3-p8pdrvn?step=67
  if pmR and len(reflStrays)>0 and len(reflRefs)>0 and len(reflTargets)>0:
    # Calibration
    calib = record.calibration.spectre.measurement.sort_index().loc[wvlMin:wvlMax]
    # (A - B):
    divisorsTar = reflRefs[0].spectre.measurement.sub(reflStrays[0].spectre.measurement)
    # Calculations per leafs:
    for reflTarget in reflTargets:
      # (C - B):
      dividendsTar = reflTarget.spectre.measurement.sub(reflStrays[0].spectre.measurement)
      # [ (C - B) ÷ (A - B) ]
      divisionTar = dividendsTar.div(divisorsTar)
      # ([ (C - B) ÷ (A - B) ]) × calib.refl
      mseries = get_monotonic_series(divisionTar)
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
    record.reflecAverage = reflecAverage
    reflecStadDev = pd.Series(arrStd, index=arrIndex, name="reflectance_standard_deviation")
    reflecStadDev.index.name = 'wavelength'
    record.reflecStadDev = reflecStadDev

    # Calculation of (A1/A0):
    distA0A1 = pd.Series()
    if len(reflRefs) == 2:
      distA0A1 = reflRefs[1].spectre.measurement.div(reflRefs[0].spectre.measurement)
      record.reflecDiffRef = distA0A1
    else:
      LO.l_war("the record {} haven't the right number of reference measurments to process the reference of reflectance calculation.".format(record.id))
    # Calculation of (B0/A0):
    distB0A1 = pd.Series()
    if len(reflStrays) > 0 and len(reflRefs) > 0 :
      distB0A1 = reflStrays[0].spectre.measurement.div(reflRefs[0].spectre.measurement)
      record.reflecRef = distB0A1
    else:
      LO.l_war("the record {} have just one reference measurments to process the stray light vs reference.".format(record.id))
  else:
    boo = False
    LO.l_err("the record {} doesn't all spectrum measurments to process the reflectance calculation.".format(record.id))
  
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
    record.transAverage = transAverage
    transStadDev = pd.Series(arrStd, index=arrIndex, name="transmittance_standard_deviation")
    transStadDev.index.name = 'wavelength'
    record.transStadDev = transStadDev

    # Calculation of (D1/D0):
    distD0D1 = pd.Series()
    if len(transRefAll) == 2:
      distD0D1 = transRefAll[1].spectre.measurement.div(transRefAll[0].spectre.measurement)
      record.transDiffRef    = distD0D1
    else:
      LO.l_war("the record {} haven't the right number of reference measurments to process the reference of transmittance calculation.".format(record.id))
  else:
    boo = False
    LO.l_err("the record {} doesn't all spectrum measurments to process the transmittance calculation.".format(record.id))
  return boo

