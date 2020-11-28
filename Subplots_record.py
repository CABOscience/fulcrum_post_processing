#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
from . import projects as PR
from . import parameters as PA
from . import tools as TO
from . import logs as LO

# Spectroscopy
#import specdal
# System
import sys

##############################################
# OBJECTS
##############################################

class Subplots(RE.Records):
  """ Subplots object
  Plots object is containing a list of Plots Object
  """

class Subplot(RE.Record):
  def __init__(self, record):
    super(Subplot,self).__init__(record.altitude, record.assigned_to, record.assigned_to_id, record.client_created_at, record.client_updated_at, record.course, record.created_at, record.created_by, record.created_by_id, record.created_duration, record.created_location, record.edited_duration, record.form_id, record.form_name, record.form_values, record.horizontal_accuracy, record.id, record.latitude, record.longitude, record.project_id, record.speed, record.status, record.updated_at, record.updated_by, record.updated_by_id, record.updated_duration, record.updated_location, record.version, record.vertical_accuracy, record.project_name)
    self.fv_altitude = ''
    self.fv_approbation = ''
    self.fv_approved_by = ''
    self.fv_azimuth = ''
    self.fv_azimuth_width_degrees = ''
    self.fv_corner_altitude = ''
    self.fv_corner_current_gps_information = ''
    self.fv_corner_gps_info = ''
    self.fv_corner_horizontal_accuracy = ''
    self.fv_corner_latitude = ''
    self.fv_corner_longitude = ''
    self.fv_corner_number = ''
    self.fv_corner_update_gps_position = ''
    self.fv_corner_vertical_accuracy = ''
    self.fv_corners = ''
    self.fv_current_gps_information = ''
    self.fv_data_quality_control = ''
    self.fv_date_approved = ''
    self.fv_date_first_established = '' #
    self.fv_date_published = ''
    self.fv_date_rejected = ''
    self.fv_date_submitted = ''
    self.fv_date_verified = ''
    self.fv_distance_from_plot_center_m = ''
    self.fv_filter_site = ''
    self.fv_filter_site_id = ''
    self.fv_first_established_by = '' #
    self.fv_gps_info = ''
    self.fv_hidden_variables = ''
    self.fv_horizontal_accuracy = ''
    self.fv_latitude = ''
    self.fv_location = ''
    self.fv_longitude = ''
    self.fv_number_of_corners = ''
    self.fv_number_of_rejections = ''
    self.fv_optional_subplot_info = ''
    self.fv_plot = '' #
    self.fv_plot_altitude_m = ''
    self.fv_plot_angle_azimut = ''
    self.fv_plot_diameter = ''
    self.fv_plot_horizontal_accuracy_m = ''
    self.fv_plot_id = ''
    self.fv_plot_infos = ''
    self.fv_plot_latitude = ''
    self.fv_plot_length = ''
    self.fv_plot_location = ''
    self.fv_plot_longitude = ''
    self.fv_plot_section = ''
    self.fv_plot_shape = ''
    self.fv_plot_shape_and_size = ''
    self.fv_plot_vertical_accuracy_m = ''
    self.fv_plot_width = ''
    self.fv_position_along_length_x_axis_m = ''
    self.fv_position_along_width_y_axis_m = ''
    self.fv_publication = ''
    self.fv_published_by = ''
    self.fv_rejected_by = ''
    self.fv_rejection = ''
    self.fv_site_id = ''
    self.fv_submission = ''
    self.fv_submitted_by = ''
    self.fv_subplot = ''
    self.fv_subplot_audio_remarks = ''
    self.fv_subplot_diameter_m = ''
    self.fv_subplot_field_id = ''
    self.fv_subplot_geometry = ''
    self.fv_subplot_id = ''
    self.fv_subplot_length_m = ''
    self.fv_subplot_photos = ''
    self.fv_subplot_positioning_method = '' #
    self.fv_subplot_remarks = ''
    self.fv_subplot_shape = '' #
    self.fv_subplot_shape_size = ''
    self.fv_subplot_width_m = ''
    self.fv_timestamp = ''
    self.fv_update_location_with_gps = ''
    self.fv_verification = ''
    self.fv_verified_by = ''
    self.fv_vertical_accuracy = ''



def extract_plot_record(record):
  """ This will extract a spectroscopy panel record data from a record "form values"
  
  :param arg1: a SpectroscopyPanel to be tested
  :type arg1: SpectroscopyPanel

  :return: an updated record if it is validated or the record
  :rtype: SpectroscopyPanel
  """
  LO.l_info('Start extract leaf spectra recordid {}'.format(record.id))
  rv  = record.form_values

  if 'date_first_established' in rv \
    and 'first_established_by' in rv \
    and 'plot' in rv \
    and 'subplot_positioning_method' in rv \
    and 'subplot_shape' in rv :
    if 'altitude' in rv: record.fv_altitude = rv['altitude']
    if 'approbation' in rv: record.fv_approbation = rv['approbation']
    if 'approved_by' in rv: record.fv_approved_by = rv['approved_by']
    if 'azimuth' in rv: record.fv_azimuth = rv['azimuth']
    if 'azimuth_width_degrees' in rv: record.fv_azimuth_width_degrees = rv['azimuth_width_degrees']
    if 'corner_altitude' in rv: record.fv_corner_altitude = rv['corner_altitude']
    if 'corner_current_gps_information' in rv: record.fv_corner_current_gps_information = rv['corner_current_gps_information']
    if 'corner_gps_info' in rv: record.fv_corner_gps_info = rv['corner_gps_info']
    if 'corner_horizontal_accuracy' in rv: record.fv_corner_horizontal_accuracy = rv['corner_horizontal_accuracy']
    if 'corner_latitude' in rv: record.fv_corner_latitude = rv['corner_latitude']
    if 'corner_longitude' in rv: record.fv_corner_longitude = rv['corner_longitude']
    if 'corner_number' in rv: record.fv_corner_number = rv['corner_number']
    if 'corner_update_gps_position' in rv: record.fv_corner_update_gps_position = rv['corner_update_gps_position']
    if 'corner_vertical_accuracy' in rv: record.fv_corner_vertical_accuracy = rv['corner_vertical_accuracy']
    if 'corners' in rv: record.fv_corners = rv['corners']
    if 'current_gps_information' in rv: record.fv_current_gps_information = rv['current_gps_information']
    if 'data_quality_control' in rv: record.fv_data_quality_control = rv['data_quality_control']
    if 'date_approved' in rv: record.fv_date_approved = rv['date_approved']
    if 'date_first_established' in rv: record.fv_date_first_established = rv['date_first_established']
    if 'date_published' in rv: record.fv_date_published = rv['date_published']
    if 'date_rejected' in rv: record.fv_date_rejected = rv['date_rejected']
    if 'date_submitted' in rv: record.fv_date_submitted = rv['date_submitted']
    if 'date_verified' in rv: record.fv_date_verified = rv['date_verified']
    if 'distance_from_plot_center_m' in rv: record.fv_distance_from_plot_center_m = rv['distance_from_plot_center_m']
    if 'filter_site' in rv: record.fv_filter_site = rv['filter_site']
    if 'filter_site_id' in rv: record.fv_filter_site_id = rv['filter_site_id']
    if 'first_established_by' in rv: record.fv_first_established_by = rv['first_established_by']
    if 'gps_info' in rv: record.fv_gps_info = rv['gps_info']
    if 'hidden_variables' in rv: record.fv_hidden_variables = rv['hidden_variables']
    if 'horizontal_accuracy' in rv: record.fv_horizontal_accuracy = rv['horizontal_accuracy']
    if 'latitude' in rv: record.fv_latitude = rv['latitude']
    if 'location' in rv: record.fv_location = rv['location']
    if 'longitude' in rv: record.fv_longitude = rv['longitude']
    if 'number_of_corners' in rv: record.fv_number_of_corners = rv['number_of_corners']
    if 'number_of_rejections' in rv: record.fv_number_of_rejections = rv['number_of_rejections']
    if 'optional_subplot_info' in rv: record.fv_optional_subplot_info = rv['optional_subplot_info']
    if 'plot' in rv: record.fv_plot = rv['plot']
    if 'plot_altitude_m' in rv: record.fv_plot_altitude_m = rv['plot_altitude_m']
    if 'plot_angle_azimut' in rv: record.fv_plot_angle_azimut = rv['plot_angle_azimut']
    if 'plot_diameter' in rv: record.fv_plot_diameter = rv['plot_diameter']
    if 'plot_horizontal_accuracy_m' in rv: record.fv_plot_horizontal_accuracy_m = rv['plot_horizontal_accuracy_m']
    if 'plot_id' in rv: record.fv_plot_id = rv['plot_id']
    if 'plot_infos' in rv: record.fv_plot_infos = rv['plot_infos']
    if 'plot_latitude' in rv: record.fv_plot_latitude = rv['plot_latitude']
    if 'plot_length' in rv: record.fv_plot_length = rv['plot_length']
    if 'plot_location' in rv: record.fv_plot_location = rv['plot_location']
    if 'plot_longitude' in rv: record.fv_plot_longitude = rv['plot_longitude']
    if 'plot_section' in rv: record.fv_plot_section = rv['plot_section']
    if 'plot_shape' in rv: record.fv_plot_shape = rv['plot_shape']
    if 'plot_shape_and_size' in rv: record.fv_plot_shape_and_size = rv['plot_shape_and_size']
    if 'plot_vertical_accuracy_m' in rv: record.fv_plot_vertical_accuracy_m = rv['plot_vertical_accuracy_m']
    if 'plot_width' in rv: record.fv_plot_width = rv['plot_width']
    if 'position_along_length_x_axis_m' in rv: record.fv_position_along_length_x_axis_m = rv['position_along_length_x_axis_m']
    if 'position_along_width_y_axis_m' in rv: record.fv_position_along_width_y_axis_m = rv['position_along_width_y_axis_m']
    if 'publication' in rv: record.fv_publication = rv['publication']
    if 'published_by' in rv: record.fv_published_by = rv['published_by']
    if 'rejected_by' in rv: record.fv_rejected_by = rv['rejected_by']
    if 'rejection' in rv: record.fv_rejection = rv['rejection']
    if 'site_id' in rv: record.fv_site_id = rv['site_id']
    if 'submission' in rv: record.fv_submission = rv['submission']
    if 'submitted_by' in rv: record.fv_submitted_by = rv['submitted_by']
    if 'subplot' in rv: record.fv_subplot = rv['subplot']
    if 'subplot_audio_remarks' in rv: record.fv_subplot_audio_remarks = rv['subplot_audio_remarks']
    if 'subplot_diameter_m' in rv: record.fv_subplot_diameter_m = rv['subplot_diameter_m']
    if 'subplot_field_id' in rv: record.fv_subplot_field_id = rv['subplot_field_id']
    if 'subplot_geometry' in rv: record.fv_subplot_geometry = rv['subplot_geometry']
    if 'subplot_id' in rv: record.fv_subplot_id = rv['subplot_id']
    if 'subplot_length_m' in rv: record.fv_subplot_length_m = rv['subplot_length_m']
    if 'subplot_photos' in rv: record.fv_subplot_photos = rv['subplot_photos']
    if 'subplot_positioning_method' in rv: record.fv_subplot_positioning_method = rv['subplot_positioning_method']
    if 'subplot_remarks' in rv: record.fv_subplot_remarks = rv['subplot_remarks']
    if 'subplot_shape' in rv: record.fv_subplot_shape = rv['subplot_shape']
    if 'subplot_shape_size' in rv: record.fv_subplot_shape_size = rv['subplot_shape_size']
    if 'subplot_width_m' in rv: record.fv_subplot_width_m = rv['subplot_width_m']
    if 'timestamp' in rv: record.fv_timestamp = rv['timestamp']
    if 'update_location_with_gps' in rv: record.fv_update_location_with_gps = rv['update_location_with_gps']
    if 'verification' in rv: record.fv_verification = rv['verification']
    if 'verified_by' in rv: record.fv_verified_by = rv['verified_by']
    if 'vertical_accuracy' in rv: record.fv_vertical_accuracy = rv['vertical_accuracy']

  else:
    tab = ['date_first_established', 'first_established_by', 'plot', 'subplot_positioning_method', 'subplot_shape']
    s = ""
    for t in tab:
      if not t in rv:
        if s:
          s+=', '
        s += t
    record.isValid = False
    LO.l_war('Project {}, the record id {} will not be used because it has no {}.'.format(record.project_name,record.id,s))
    record.add_toLog('Project {}, the record id {} will not be used because it has no {}.'.format(record.project_name,record.id,s))
