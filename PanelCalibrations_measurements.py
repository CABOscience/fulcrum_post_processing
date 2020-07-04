#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tools as TO
# Spectroscopy
#import specdal
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
    self.files_name = []
    self.files_path = []
    self.reflectances = [] # pd.DataFrame()
    self.spectres = [] # TO.create_empty_spectrum()
    self.file_numbers = ''
    self.measurement_id = '' #
    self.measurement_remarks = ''
    self.primary_light_port = ''
    self.reflectance_port = ''
    self.spectrum_number = ''
    self.target_type = ''
    self.transmission_port = ''
    self.spectrum_number = ''
    self.spectrum_number_end = ''
    self.sphere_configuration = '' #
    self.isValid = True
    self.logInfo = ""

  def add_toLog(self, st):
    self.logInfo += "\n"+st

  def __str__(self):
    return '>{} - {}'.format(self.file_name, self.file_path)

  def to_csv(self):
    sc = ''
    if len(self.sphere_configuration_svc_large_leaves)>0:
      sc = self.sphere_configuration_svc_large_leaves
    else: 
      sc = self.sphere_configuration_svc_small_leaves
    port = ''
    if len(self.reflectance_port_svc)>0:
      port = self.reflectance_port_svc
    else :
      port = self.transmission_port_svc
    return [self.file_name, self.file_path,self.leaf_number,self.leaf_side_measured,self.spectrum_number,sc,port]

  def to_csv_leaf(self):
    return [self.file_name,self.leaf_number,self.leaf_side_measured]

  def to_csv_reference(self):
    return [self.leaf_number,self.leaf_side_measured]

  def to_csv_all(self):
    return [self.leaf_side_measured]
  
  def m_get_wavelength_range(self):
    return self.spectre.metadata['wavelength_range']
    
  def m_get_wavelength_max(self):
    return self.m_get_wavelength_range()[1]

  def m_get_wavelength_min(self):
    return self.m_get_wavelength_range()[0]
    
  def get_filenames(self):
    return [self.file_name_1, self.file_name_2, self.file_name_3, self.file_name_4, self.file_name_5]


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
      rmt = extract_replicate_spectra_measurement(rmt_raw['form_values'])
      if rmt.isValid:
        cms.add_record(rmt)
  return cms

def extract_replicate_spectra_measurement(rmt_raw):
  """ This will extract measurement of a Panel Calibration spectra record
  
  :param arg1: a fulcrum measurement
  :type arg1: json

  :return: a calibration measurement
  :rtype: CalibrationMeasurement
  """
  cv = 'choice_values'
  rmt = CalibrationMeasurement()
  if 'file_name_1' not in rmt_raw \
    and 'file_name_2' not in rmt_raw \
    and 'file_name_3' not in rmt_raw \
    and 'sphere_configuration' not in rmt_raw \
    and 'measurement_id' not in rmt_raw :
    tab = ['file_name_1', 'file_name_2', 'file_name_3', 'sphere_configuration', 'measurement_id']
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
    rmt.files_name.append(rmt_raw['file_name_1'])
    rmt.files_name.append(rmt_raw['file_name_2'])
    rmt.files_name.append(rmt_raw['file_name_3'])
    rmt.sphere_configuration = rmt_raw['sphere_configuration']
    rmt.measurement_id  = rmt_raw['measurement_id']
    
    if 'file_name_4'    in rmt_raw:     rmt.files_name.append(rmt_raw['file_name_4'])
    if 'file_name_4'    in rmt_raw:     rmt.files_name.append(rmt_raw['file_name_5'])
    if 'measurement_remarks'in rmt_raw: rmt.measurement_remarks = rmt_raw['measurement_remarks']
    if 'primary_light_port' in rmt_raw: rmt.primary_light_port = rmt_raw['primary_light_port']
    if 'reflectance_port'   in rmt_raw: rmt.reflectance_port = rmt_raw['reflectance_port'][cv][0]
    if 'spectrum_number'    in rmt_raw: rmt.spectrum_number = rmt_raw['spectrum_number']
    if 'target_type'        in rmt_raw: rmt.target_type = rmt_raw['target_type']
    if 'transmission_port'  in rmt_raw: rmt.transmission_port = rmt_raw['transmission_port'][cv][0]

  return rmt
