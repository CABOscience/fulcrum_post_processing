#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
import projects as PR
import parameters as PA
import records as RE
import tools as TO
import logs as LO
import SpectroscopyPanels_calibrations as SPC

# Spectroscopy
import specdal
# System
import sys

##############################################
# OBJECTS
##############################################

class SpectroscopyPanels(RE.Records):
  """ SpectroscopyPanels object
  SpectroscopyPanels object is containing a list of SpectroscopyPanel Object
  """
  def add_record(self,SpectroscopyPanel):
    self.records.append(SpectroscopyPanel)
    self.recordsDict[SpectroscopyPanel.ID]=SpectroscopyPanel

class SpectroscopyPanel(RE.Record):
  def __init__(self, record):
    super(SpectroscopyPanel,self).__init__(record.altitude, record.assigned_to, record.assigned_to_id, record.client_created_at, record.client_updated_at, record.course, record.created_at, record.created_by, record.created_by_id, record.created_duration, record.created_location, record.edited_duration, record.form_id, record.form_values, record.horizontal_accuracy, record.ID, record.latitude, record.longitude, record.project_id, record.speed, record.status, record.updated_at, record.updated_by, record.updated_by_id, record.updated_duration, record.updated_location, record.version, record.vertical_accuracy, record.project_name)
    self.fv_calibrated_by = ""
    self.fv_calibrated_reflectance = ""
    self.fv_calibration_date = ""
    self.fv_calibration_document_photos = ""
    self.fv_calibration_file_name = ""
    self.fv_calibration_google_file_directory = ""
    self.fv_calibration_number = ""
    self.fv_calibration_remarks = ""
    self.fv_calibrations = ""
    self.fv_contact_email_address = "" #
    self.fv_link_to_calibration_files = ""
    self.fv_manufacture_name = "" #
    self.fv_manufacturer = ""
    self.fv_manufacturer_short_name = ""
    self.fv_manufacturer_url = ""
    self.fv_material = ""
    self.fv_model_number = ""
    self.fv_model_url = ""
    self.fv_name_of_contact_person = "" #
    self.fv_owner = ""
    self.fv_owner_barcode = ""
    self.fv_owning_institute = ""
    self.fv_owning_institute_address = ""
    self.fv_owning_institute_url = ""
    self.fv_panel = ""
    self.fv_panel_barcode = ""
    self.fv_panel_calibration = ""
    self.fv_panel_description = ""
    self.fv_panel_diameter_mm = ""
    self.fv_panel_height_mm = ""
    self.fv_panel_photos = ""
    self.fv_panel_remarks = ""
    self.fv_panel_shape = ""
    self.fv_panel_type = ""
    self.fv_panel_width_mm = ""
    self.fv_reflectance = ""
    self.fv_serial_number = "" #
    self.fv_wavelength_nm = ""
    self.hasCalibrations = False


  def extract_spectroscopyPanel_record(self,):
    """ This will extract a spectroscopy panel record data from a record "form values"
    
    :param arg1: a SpectroscopyPanel to be tested
    :type arg1: SpectroscopyPanel

    :return: an updated record if it is validated or the record
    :rtype: SpectroscopyPanel
    """
    LO.l_info('Start extract spectroscopy panel recordid {}'.format(self.ID))
    rv  = self.form_values
    if 'serial_number' in rv \
      and 'name_of_contact_person' in rv \
      and 'manufacture_name' in rv \
      and 'contact_email_address' in rv:
      if 'calibrated_by'  in rv: self.fv_calibrated_by = rv['calibrated_by']
      if 'calibrated_reflectance'  in rv: self.fv_calibrated_reflectance = rv['calibrated_reflectance']
      if 'calibration_date'  in rv: self.fv_calibration_date = rv['calibration_date']
      if 'calibration_document_photos'  in rv: self.fv_calibration_document_photos = rv['calibration_document_photos']
      if 'calibration_file_name'  in rv: self.fv_calibration_file_name = rv['calibration_file_name']
      if 'calibration_google_file_directory'  in rv: self.fv_calibration_google_file_directory = rv['calibration_google_file_directory']
      if 'calibration_number'  in rv: self.fv_calibration_number = rv['calibration_number']
      if 'calibration_remarks'  in rv: self.fv_calibration_remarks = rv['calibration_remarks']
      if 'calibrations'  in rv: self.fv_calibrations = rv['calibrations']
      if 'contact_email_address'  in rv: self.fv_contact_email_address = rv['contact_email_address']
      if 'link_to_calibration_files'  in rv: self.fv_link_to_calibration_files = rv['link_to_calibration_files']
      if 'manufacture_name'  in rv: self.fv_manufacture_name = rv['manufacture_name']
      if 'manufacturer'  in rv: self.fv_manufacturer = rv['manufacturer']
      if 'manufacturer_short_name'  in rv: self.fv_manufacturer_short_name = rv['manufacturer_short_name']
      if 'manufacturer_url'  in rv: self.fv_manufacturer_url = rv['manufacturer_url']
      if 'material'  in rv: self.fv_material = rv['material']
      if 'model_number'  in rv: self.fv_model_number = rv['model_number']
      if 'model_url'  in rv: self.fv_model_url = rv['model_url']
      if 'name_of_contact_person'  in rv: self.fv_name_of_contact_person = rv['name_of_contact_person']
      if 'owner'  in rv: self.fv_owner = rv['owner']
      if 'owner_barcode'  in rv: self.fv_owner_barcode = rv['owner_barcode']
      if 'owning_institute'  in rv: self.fv_owning_institute = rv['owning_institute']
      if 'owning_institute_address'  in rv: self.fv_owning_institute_address = rv['owning_institute_address']
      if 'owning_institute_url'  in rv: self.fv_owning_institute_url = rv['owning_institute_url']
      if 'panel'  in rv: self.fv_panel = rv['panel']
      if 'panel_barcode'  in rv: self.fv_panel_barcode = rv['panel_barcode']
      if 'panel_calibration'  in rv: self.fv_panel_calibration = rv['panel_calibration']
      if 'panel_description'  in rv: self.fv_panel_description = rv['panel_description']
      if 'panel_diameter_mm'  in rv: self.fv_panel_diameter_mm = rv['panel_diameter_mm']
      if 'panel_height_mm'  in rv: self.fv_panel_height_mm = rv['panel_height_mm']
      if 'panel_photos'  in rv: self.fv_panel_photos = rv['panel_photos']
      if 'panel_remarks'  in rv: self.fv_panel_remarks = rv['panel_remarks']
      if 'panel_shape'  in rv: self.fv_panel_shape = rv['panel_shape']
      if 'panel_type'  in rv: self.fv_panel_type = rv['panel_type']
      if 'panel_width_mm'  in rv: self.fv_panel_width_mm = rv['panel_width_mm']
      if 'reflectance'  in rv: self.fv_reflectance = rv['reflectance']
      if 'serial_number'  in rv: self.fv_serial_number = rv['serial_number']
      if 'wavelength_nm'  in rv: self.fv_wavelength_nm = rv['wavelength_nm']
    else:
      tab = ['serial_number','name_of_contact_person','manufacture_name','contact_email_address']
      s = ""
      for t in tab:
        if not t in rv:
          if s:
            s+=', '
          s += t
      LO.l_war('Project {}, the record id {} will not be used because it has no {}.'.format(self.project_name,self.ID,s))
      self.isValid = False
      self.add_toLog('Project {}, the record id {} will not be used because it has no {}.'.format(self.project_name,self.ID,s))

  def update_record_with_calibrations(self,):
    if self.fv_calibrations:
      self.fv_calibrations = SPC.extract_SpectroscopyPanels_calibration_values(self.fv_serial_number,self.fv_calibrations)
      self.fv_calibrations.toPrint()
    else:
      print('no calibrations')
    #for calibration in self.fv_calibrations:
    
  def is_record():
    return True

    
##############################################
# Functions
##############################################
def load_spectroscopypanels_webhook_Records():
  """ This will load spectroscopypanels object from webhook
  
  :return: SpectroscopyPanels object full of SpectroscopyPanels processible
  :rtype: SpectroscopyPanels
  """
  spectroPanels = SpectroscopyPanels()
  spectroPanelsForm = TO.load_json_file(PA.SpectroscopyPanelsFormFile)
  spectroPanelsFormID = spectroPanelsForm['id']
  
  webhookRecords = RE.load_webhook_records(projects)
  for record_raw in webhookRecords.records[:]:
    if spectroPanelsFormID not in record.form_id:
      LO.l_info('The record {} will not be used because it is not a Spectroscopy Panels record'.format(record_raw.ID))
    else:
      record = SpectroscopyPanel(record_raw)
      record.extract_spectroscopyPanel_record()
      if record.isValid:
        record.update_record_with_calibrations()
        spectroPanels.add_record(record)
        
  return spectroPanels


def load_spectroscopypanels_Records():
  fname = PA.SpectroscopyPanelsRecordsFile
  if TO.file_is_here(fname):
    LO.l_info('The panel calibration file is {}'.format(fname))
    return get_SpectroscopyPanels_Records(fname)
  else:
    LO.l_war('The panel calibration  ({}) is available. Program will die'.format(fname))
    sys.exit(1)

def get_SpectroscopyPanels_Records(fname):
  fileRecords = RE.load_records_from_json(fname)
  for record_raw in fileRecords.records[:]:
    record = SpectroscopyPanel(record_raw)
    record.extract_spectroscopyPanel_record()
    record.update_record_with_calibrations()
