#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
import projects as PR
import parameters as PA
import records as RE
import tools as TO
import logs as LO

# Spectroscopy
import specdal
# System
import sys

##############################################
# OBJECTS
##############################################

class Plots(RE.Records):
  """ Plots object
  Plots object is containing a list of Plots Object
  """

class Plot(RE.Record):
  def __init__(self, record):
    super(Plot,self).__init__(record.altitude, record.assigned_to, record.assigned_to_id, record.client_created_at, record.client_updated_at, record.course, record.created_at, record.created_by, record.created_by_id, record.created_duration, record.created_location, record.edited_duration, record.form_id, record.form_name, record.form_values, record.horizontal_accuracy, record.id, record.latitude, record.longitude, record.project_id, record.speed, record.status, record.updated_at, record.updated_by, record.updated_by_id, record.updated_duration, record.updated_location, record.version, record.vertical_accuracy, record.project_name)
    self.fv_altitude = ''
    self.fv_approbation = ''
    self.fv_approved_by = ''
    self.fv_average_latitude = ''
    self.fv_average_longitude = ''
    self.fv_azimuth_width_degrees = ''
    self.fv_corner_altitude_m = ''
    self.fv_corner_field_id = ''
    self.fv_corner_gps_info = ''
    self.fv_corner_horizontal_accuracy_m = ''
    self.fv_corner_id = ''
    self.fv_corner_latitude_degrees = ''
    self.fv_corner_location = ''
    self.fv_corner_longitude_degrees = ''
    self.fv_corner_number = ''
    self.fv_corner_vertical_accuracy_m = ''
    self.fv_corners = ''
    self.fv_current_gps_information = ''
    self.fv_data_quality_control = ''
    self.fv_date_approved = ''
    self.fv_date_deleted = ''
    self.fv_date_first_established = '' #
    self.fv_date_published = ''
    self.fv_date_rejected = ''
    self.fv_date_submitted = ''
    self.fv_date_verified = ''
    self.fv_deleted = ''
    self.fv_deleted_by = ''
    self.fv_first_established_by = '' #
    self.fv_gps_info = ''
    self.fv_gps_informations_updated_from_corners = ''
    self.fv_hidden_variables = ''
    self.fv_horizontal_accuracy = ''
    self.fv_latitude = ''
    self.fv_location = ''
    self.fv_longitude = ''
    self.fv_number_of_corners = ''
    self.fv_number_of_rejections = ''
    self.fv_optional_plot_info = ''
    self.fv_plot = ''
    self.fv_plot_audio_remarks = ''
    self.fv_plot_diameter_m = ''
    self.fv_plot_field_id = ''
    self.fv_plot_geometry = ''
    self.fv_plot_id = ''
    self.fv_plot_length_m = ''
    self.fv_plot_photos = ''
    self.fv_plot_remarks = ''
    self.fv_plot_shape = ''  #*
    self.fv_plot_shape_size = ''
    self.fv_plot_width_m = ''
    self.fv_publication = ''
    self.fv_published_by = ''
    self.fv_rejected_by = ''
    self.fv_rejection = ''
    self.fv_site = '' #
    self.fv_site_id = ''
    self.fv_study_site = ''
    self.fv_submission = ''
    self.fv_submitted_by = ''
    self.fv_update_corner_location_with_gps = ''
    self.fv_update_location_with_gps = ''
    self.fv_verification = ''
    self.fv_verified_by = ''
    self.fv_vertical_accuracy = ''


def extract_plot_record(record):
  """ This will extract a plot panel record data from a record "form values"
  
  :param arg1: a Plot to be tested
  :type arg1: Plot

  :return: an updated record if it is validated or the record
  :rtype: Plot
  """
  LO.l_info('Start extract leaf spectra recordid {}'.format(record.id))
  rv  = record.form_values

  if 'date_first_established' in rv \
    and 'first_established_by' in rv \
    and 'plot_shape' in rv \
    and 'site' in rv :
    if 'altitude' in rv: record.fv_altitude = rv['altitude']
    if 'approbation' in rv: record.fv_approbation = rv['approbation']
    if 'approved_by' in rv: record.fv_approved_by = rv['approved_by']
    if 'average_latitude' in rv: record.fv_average_latitude = rv['average_latitude']
    if 'average_longitude' in rv: record.fv_average_longitude = rv['average_longitude']
    if 'azimuth_width_degrees' in rv: record.fv_azimuth_width_degrees = rv['azimuth_width_degrees']
    if 'corner_altitude_m' in rv: record.fv_corner_altitude_m = rv['corner_altitude_m']
    if 'corner_field_id' in rv: record.fv_corner_field_id = rv['corner_field_id']
    if 'corner_gps_info' in rv: record.fv_corner_gps_info = rv['corner_gps_info']
    if 'corner_horizontal_accuracy_m' in rv: record.fv_corner_horizontal_accuracy_m = rv['corner_horizontal_accuracy_m']
    if 'corner_id' in rv: record.fv_corner_id = rv['corner_id']
    if 'corner_latitude_degrees' in rv: record.fv_corner_latitude_degrees = rv['corner_latitude_degrees']
    if 'corner_location' in rv: record.fv_corner_location = rv['corner_location']
    if 'corner_longitude_degrees' in rv: record.fv_corner_longitude_degrees = rv['corner_longitude_degrees']
    if 'corner_number' in rv: record.fv_corner_number = rv['corner_number']
    if 'corner_vertical_accuracy_m' in rv: record.fv_corner_vertical_accuracy_m = rv['corner_vertical_accuracy_m']
    if 'corners' in rv: record.fv_corners = rv['corners']
    if 'current_gps_information' in rv: record.fv_current_gps_information = rv['current_gps_information']
    if 'data_quality_control' in rv: record.fv_data_quality_control = rv['data_quality_control']
    if 'date_approved' in rv: record.fv_date_approved = rv['date_approved']
    if 'date_deleted' in rv: record.fv_date_deleted = rv['date_deleted']
    if 'date_first_established' in rv: record.fv_date_first_established = rv['date_first_established']
    if 'date_published' in rv: record.fv_date_published = rv['date_published']
    if 'date_rejected' in rv: record.fv_date_rejected = rv['date_rejected']
    if 'date_submitted' in rv: record.fv_date_submitted = rv['date_submitted']
    if 'date_verified' in rv: record.fv_date_verified = rv['date_verified']
    if 'deleted' in rv: record.fv_deleted = rv['deleted']
    if 'deleted_by' in rv: record.fv_deleted_by = rv['deleted_by']
    if 'first_established_by' in rv: record.fv_first_established_by = rv['first_established_by']
    if 'gps_info' in rv: record.fv_gps_info = rv['gps_info']
    if 'gps_informations_updated_from_corners' in rv: record.fv_gps_informations_updated_from_corners = rv['gps_informations_updated_from_corners']
    if 'hidden_variables' in rv: record.fv_hidden_variables = rv['hidden_variables']
    if 'horizontal_accuracy' in rv: record.fv_horizontal_accuracy = rv['horizontal_accuracy']
    if 'latitude' in rv: record.fv_latitude = rv['latitude']
    if 'location' in rv: record.fv_location = rv['location']
    if 'longitude' in rv: record.fv_longitude = rv['longitude']
    if 'number_of_corners' in rv: record.fv_number_of_corners = rv['number_of_corners']
    if 'number_of_rejections' in rv: record.fv_number_of_rejections = rv['number_of_rejections']
    if 'optional_plot_info' in rv: record.fv_optional_plot_info = rv['optional_plot_info']
    if 'plot' in rv: record.fv_plot = rv['plot']
    if 'plot_audio_remarks' in rv: record.fv_plot_audio_remarks = rv['plot_audio_remarks']
    if 'plot_diameter_m' in rv: record.fv_plot_diameter_m = rv['plot_diameter_m']
    if 'plot_field_id' in rv: record.fv_plot_field_id = rv['plot_field_id']
    if 'plot_geometry' in rv: record.fv_plot_geometry = rv['plot_geometry']
    if 'plot_id' in rv: record.fv_plot_id = rv['plot_id']
    if 'plot_length_m' in rv: record.fv_plot_length_m = rv['plot_length_m']
    if 'plot_photos' in rv: record.fv_plot_photos = rv['plot_photos']
    if 'plot_remarks' in rv: record.fv_plot_remarks = rv['plot_remarks']
    if 'plot_shape' in rv: record.fv_plot_shape = rv['plot_shape']
    if 'plot_shape_size' in rv: record.fv_plot_shape_size = rv['plot_shape_size']
    if 'plot_width_m' in rv: record.fv_plot_width_m = rv['plot_width_m']
    if 'publication' in rv: record.fv_publication = rv['publication']
    if 'published_by' in rv: record.fv_published_by = rv['published_by']
    if 'rejected_by' in rv: record.fv_rejected_by = rv['rejected_by']
    if 'rejection' in rv: record.fv_rejection = rv['rejection']
    if 'site' in rv: record.fv_site = rv['site']
    if 'site_id' in rv: record.fv_site_id = rv['site_id']
    if 'study_site' in rv: record.fv_study_site = rv['study_site']
    if 'submission' in rv: record.fv_submission = rv['submission']
    if 'submitted_by' in rv: record.fv_submitted_by = rv['submitted_by']
    if 'update_corner_location_with_gps' in rv: record.fv_update_corner_location_with_gps = rv['update_corner_location_with_gps']
    if 'update_location_with_gps' in rv: record.fv_update_location_with_gps = rv['update_location_with_gps']
    if 'verification' in rv: record.fv_verification = rv['verification']
    if 'verified_by' in rv: record.fv_verified_by = rv['verified_by']
    if 'vertical_accuracy' in rv: record.fv_vertical_accuracy = rv['vertical_accuracy']

  else:
    tab = ['date_first_established', 'first_established_by', 'plot_shape', 'site']
    s = ""
    for t in tab:
      if not t in rv:
        if s:
          s+=', '
        s += t
    LO.l_war('Project {}, the record id {} will not be used because it has no {}.'.format(record.project_name,record.id,s))
    record.isValid = False
    record.add_toLog('Project {}, the record id {} will not be used because it has no {}.'.format(record.project_name,record.id,s))

##############################################
# Get From Plots
##############################################

def get_scientific_name_with_plot_id(plotID):
  pls = load_plots()
  return get_scientific_name_with_plot_id_from_plots(plotID,pls)

def get_plot_shape_with_plot_id_from_plots(plotID,pls):
  if len(pls)>0 and plotID in pls.recordsDict:
    return pls.recordsDict[plotID].fv_plot_shape
  LO.l_war("No Plot shape associated with {}".format(plotID))
  return ''

def get_plot_with_plot_id(plotID):
  pls = load_plots()
  return get_plot_with_plot_id_from_plots(plotID,pls)

def get_plot_with_plot_id_from_plots(plotID,pls):
  if len(pls)>0 and plotID in pls.recordsDict:
    return pls.recordsDict[plotID]
  LO.l_war("No plot associated with {}".format(plotID))
  return ''

##############################################
# Get Plots
##############################################

def get_plots_from_records(recs):
  plots = Plots()
  for plot_raw in recs.records:
    plot = Plot(plot_raw)
    extract_plot_record(plot)
    if plot.isValid:
      plots.add_record(plot)
      st = 'The plot record id {} is complete for processing'.format(plot.id)
      LO.l_debug(st)
      plot.add_toLog(st)
    else:
      st = 'The plot record id {} is incomplete and will not be used'.format(plot.id)
      LO.l_war(st)
      plot.add_toLog(st)
  return plots
  
##############################################
# LOAD SOURCES
##############################################

# Load Plots from Plots Records File
def load_plots_from_json_file():
  if TO.file_is_here(PA.PlotsRecordsFile):
    records = RE.load_records_from_json(PA.PlotsRecordsFile)
    return get_plots_from_records(records)
  else:
    LO.l_err('The file {} is not available. A default empty Plots will be loaded'.format(PA.PlotsRecordsFile))
    return Plots()

# Load Plots from fulcrum
def load_plots_from_fulcrum():
  RE.backup_records_from_forms()
  return load_plots_from_json_file()

# Load from Plots form
def load_plots_from_plots_form():
  if TO.file_is_here(PA.PlotsFormFile):
    plots_form = FO.load_form_from_json_file(PA.PlotsFormFile)
    recs = RE.load_records_from_fulcrum(plots_form)
    return get_plots_from_records(recs)
  else:
    LO.l_err('The file {} is not available. A default empty Plots will be loaded'.format(PA.PlotsRecordsFile))
    return Plots()

# Load Plots
def load_plots():
  pls = load_plots_from_json_file()
  if len(pls) < 1:
    pls = load_plots_from_plots_form()
  if len(pls) < 1:
    pls = load_plots_from_fulcrum()
  return pls
