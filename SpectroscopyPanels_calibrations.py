#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
import projects as PR
import parameters as PA
import tools as TO
import logs as LO

# Spectroscopy
#import specdal
# System
import sys

##############################################
# OBJECTS
##############################################

class SpectroscopyPanels_calibrations(object):
  calibrations = []
  calibrations_panel = {}
  
  def print_csv(self):
    s = '\n'+''.join(x.print_csv() for x in self.calibrations)
    return s
  
  def toPrint(self):
    s = '\n'+''.join(x.toPrint()+'\n' for x in self.calibrations)
    print(s)

def make_SpectroscopyPanels_calibrations(calibsTab):
  calib = SpectroscopyPanels_calibrations()
  calib.calibrations = calibsTab
  
  for calibT in calibsTab:
    if calibT.cID in calib.calibrations_panel:
      calib.calibrations_panel[calibT.cID].append(calibT)
    else:
      calib.calibrations_panel[calibT.cID] = [calibT]
  
  return calib

def get_calibration_for_record_time(calibrations, t):
  ts = TO.from_date_to_s(t)
  calib = SpectroscopyPanels_calibration()
  tp = 10000000000000000000000
  for calibration in calibrations:
    tc = TO.from_date_to_s(calibration.dDate)
    td = int(ts)-int(tc)
    if td>=0 and td<tp:
      calib = calibration
      tp = td
  if calib.cID != '':
    return calib
  else:
    return None

# Calibration objects
class SpectroscopyPanels_calibration(object):
  
  def __init__(self,  cID   = "", dDate = "", uDate = "", cDate = "", cMax = 0.0, cMin = 0.0, cFilePath = "", spectre = TO.create_empty_spectrum()):
    self.cID   = cID
    self.dDate = dDate # calibration_date
    self.uDate = uDate # updated_at
    self.cDate = cDate # created_at
    self.cMax   = cMax
    self.cMin   = cMin
    self.cFilePath = cFilePath
    self.spectre = spectre
  
  def __str__(self):
    s = 'calibID>'+self.cID+'< calibUDate>'+self.uDate+'< calibCDate>'+self.cDate+' cFilePath >'+self.cFilePath+' dDate >'+self.dDate+''
    return s
  
  def print_csv(self):
    s = ';'+self.calibID
    return s

  def toPrint(self):
    s = 'calibID>'+self.cID+'< calibUDate>'+self.uDate+'< calibCDate>'+self.cDate
    return s
  
def make_SpectroscopyPanels_calibration(calibID, calibDate, calibUDate, calibCDate, calibFilePath):
  spectre = TO.create_spectrum(calibFilePath,'reflectance')
  spectre.interpolate(method='cubic')
  cMin = spectre.measurement.index.min()
  cMax = spectre.measurement.index.max()
  return SpectroscopyPanels_calibration(calibID, calibDate, calibUDate, calibCDate, cMax, cMin, calibFilePath, spectre)

def utf8_encode(s):
  return s.encode('utf-8').decode('utf-8')
  
##############################################
# Functions
##############################################
def extract_SpectroscopyPanels_calibrations():
  fname = PA.SpectroscopyPanelsRecordsFile
  if TO.file_is_here(fname):
    LO.l_info('The panel calibration file is {}'.format(fname))
    return extract_SpectroscopyPanels_calibrations_values(fname)
  else:
    LO.l_war('The panel calibration  ({}) is available. Program will die'.format(fname))
    sys.exit(1)

def extract_SpectroscopyPanels_calibrations_values(fname):
  calibrationsJson = TO.load_json_file(fname)
  calibrations = []
  for calibrationJson in calibrationsJson:
    if 'id' in calibrationJson:
      if 'calibrations' in calibrationJson['form_values']:
        panelID  = calibrationJson['id']
        calibSerialNumber = calibrationJson['form_values']['serial_number']
        calibrationsTable = calibrationJson['form_values']['calibrations'] #contains all calibration we could used them with date update as base date
        for calibrationTable in calibrationsTable:
          calibID = calibrationTable['id']
          calibDate = "0"
          calibUDate    = calibrationTable['updated_at']
          calibCDate    = calibrationTable['created_at']
          
          calibFormValues = calibrationTable['form_values']
          calibDate       = calibFormValues['calibration_date']
          calibFileName   = calibFormValues['calibration_file_name']
          
          if calibFileName.endswith('.calib'):
            calibFilePath = PA.PanelsPath+calibSerialNumber+"/"+calibDate+"/"+calibFileName
            if TO.file_is_here(calibFilePath):
              LO.l_info('\tStart calibration extraction for {} with date {}'.format(calibFilePath,calibDate))
              #calib = make_SpectroscopyPanels_calibration(panelID, calibSerialNumber,calibID, calibDate, calibUDate, calibCDate, calibFilePath)
              calib = make_SpectroscopyPanels_calibration(calibID, calibDate, calibUDate, calibCDate, calibFilePath)
              calibrations.append(calib)
            else:
              LO.l_war("The calibration {} .calib file is not found or change the end of line (if it comes from csv file).".format(calibID))
          else:
            LO.l_war("The calibration {} does not have a .calib file. Please update the calibration measurement".format(calibID))
  return make_SpectroscopyPanels_calibrations(calibrations)

def extract_SpectroscopyPanels_calibration_values(calibSerialNumber,spCalib):
  calibrations=[]
  for calibrationTable in spCalib:
    calibID = calibrationTable['id']
    calibDate = "0"
    calibUDate    = calibrationTable['updated_at']
    calibCDate    = calibrationTable['created_at']
          
    calibFormValues = calibrationTable['form_values']
    calibDate       = calibFormValues['calibration_date']
    calibFileName   = calibFormValues['calibration_file_name']
          
    if calibFileName.endswith('.calib'):
      calibFilePath = PA.PanelsPath+calibSerialNumber+"/"+calibDate+"/"+calibFileName
      if TO.file_is_here(calibFilePath):
        LO.l_info('\tStart calibration extraction for {} with date {}'.format(calibFilePath,calibDate))
        calib = make_SpectroscopyPanels_calibration(calibID, calibDate, calibUDate, calibCDate, calibFilePath)
        calibrations.append(calib)
      else:
        LO.l_war("The calibration {} .calib file is not found or change the end of line (if it comes from csv file).".format(calibID))
    else:
      LO.l_war("The calibration {} does not have a .calib file. Please update the calibration measurement".format(calibID))
  return make_SpectroscopyPanels_calibrations(calibrations)
  
