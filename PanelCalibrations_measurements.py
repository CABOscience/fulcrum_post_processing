#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Spectroscopy
import specdal
# Data Science
import pandas as pd


##############################################
# SPECTRUM
##############################################

# SpectraMeasurements
#########################

class CalibrationMeasurements(object):
  def __init__(self):
    self.measurements=[]
    self.measurementsDict={}
    
  def __len__(self):
    return len(self.records)
    
  def add_record(self,CalibrationMeasurement):
    self.measurements.append(CalibrationMeasurement)
    self.measurementsDict[CalibrationMeasurement.measurement_id]=CalibrationMeasurement
  
class CalibrationMeasurement(object):
  def __init__(self):
    self.branch_number = ''
    self.file_name = '' #
    self.file_name_value = ''
    self.file_path = ''
    self.measurement_id = '' #
    self.measurement_remarks = ''
    self.panel_number = '' #
    self.primary_light_port = ''
    self.reflectance = pd.DataFrame()
    self.reflectance_port = ''
    self.replicate_number = ''
    self.spectrum_number = ''
    self.target_type = ''
    self.transmission_port = ''
    self.transmittance = pd.DataFrame()
    self.spectre = specdal.Spectrum(name='empty')
    self.sphere_configuration = '' #
    self.isValid = True
    self.logInfo = ""

  def add_toLog(self, st):
    self.logInfo += "\n"+st

def extract_panel_calibrations_measurements(record_measurements):
  """ This will extract measurements of a Panel Calibration record
  
  :param arg1: a fulcrum measurements list
  :type arg1: list()

  :return: a CalibrationMeasurements
  :rtype: CalibrationMeasurements
  """
  cms = CalibrationMeasurements()
  for rmt_raw in record_measurements[:]:
    if 'form_values' in rmt_raw:
      rmt = extract_leaf_spectra_measurement(rmt_raw['form_values'])
      if rmt.isValid:
        cms.add_record(rmt)
  return cms

def extract_leaf_spectra_measurement(rmt_raw):
  """ This will extract measurement of a Panel Calibration spectra record
  
  :param arg1: a fulcrum measurement
  :type arg1: json

  :return: a calibration measurement
  :rtype: CalibrationMeasurement
  """
  cv = 'choice_values'
  rmt = CalibrationMeasurement()
  if 'file_name' not in rmt_raw \
    and 'sphere_configuration' not in rmt_raw \
    and 'panel_number' not in rmt_raw \
    and 'measurement_id' not in rmt_raw :
    tab = ['file_name', 'sphere_configuration', 'panel_number', 'measurement_id']
    s = ""
    for t in tab:
      if not t in rv:
        if s:
          s+=', '
        s += t
    rmt.isValid = False
    sPnoR = 'The measurement (with measurement_id {}) will not be used because it has no {}.'.format(rmt.measurement_id,s)
    LO.l_war(sPnoR)
    rmt.add_toLog(sPnoR)
  else:
    rmt.file_name       = rmt_raw['file_name']
    rmt.sphere_configuration = rmt_raw['sphere_configuration']
    rmt.panel_number    = rmt_raw['panel_number']
    rmt.measurement_id  = rmt_raw['measurement_id']
    
    if 'branch_number'      in rmt_raw: rmt.branch_number = rmt_raw['branch_number']
    if 'file_name_value'    in rmt_raw: rmt.file_name_value = rmt_raw['file_name_value']
    if 'file_path'          in rmt_raw: rmt.file_path = rmt_raw['file_path']
    if 'measurement_remarks'in rmt_raw: rmt.measurement_remarks = rmt_raw['measurement_remarks']
    if 'primary_light_port' in rmt_raw: rmt.primary_light_port = rmt_raw['primary_light_port']
    if 'reflectance_port'   in rmt_raw: rmt.reflectance_port = rmt_raw['reflectance_port'][cv][0]
    if 'replicate_number'   in rmt_raw: rmt.replicate_number = rmt_raw['replicate_number']
    if 'spectrum_number'    in rmt_raw: rmt.spectrum_number = rmt_raw['spectrum_number']
    if 'target_type'        in rmt_raw: rmt.target_type = rmt_raw['target_type']
    if 'transmission_port'  in rmt_raw: rmt.transmission_port = rmt_raw['transmission_port'][cv][0]

