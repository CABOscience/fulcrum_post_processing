#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
import projects as PR
import parameters as PA
import records as RE
import forms as FO
import tools as TO
import logs as LO

# Spectroscopy
import specdal
# System
import sys

##############################################
# OBJECTS
##############################################

class Plants(RE.Records):
  """ Plants object
  Plants object is containing a list of Plant Object
  def add_record(self,Plant):
    self.records.append(Plant)
    self.recordsDict[Plant.id]=Plant

  def __len__(self):
    return len(self.records)
  """

class Plant(RE.Record):
  def __init__(self, record):
    super(Plant,self).__init__(record.altitude, record.assigned_to, record.assigned_to_id, record.client_created_at, record.client_updated_at, record.course, record.created_at, record.created_by, record.created_by_id, record.created_duration, record.created_location, record.edited_duration, record.form_id, record.form_name, record.form_values, record.horizontal_accuracy, record.id, record.latitude, record.longitude, record.project_id, record.speed, record.status, record.updated_at, record.updated_by, record.updated_by_id, record.updated_duration, record.updated_location, record.version, record.vertical_accuracy, record.project_name)
    self.fv_altitude = ''
    self.fv_approved_by = ''
    self.fv_bryoquel_taxon = ''
    self.fv_close_up_photos = ''
    self.fv_corners_latitude = ''
    self.fv_corners_longitude = ''
    self.fv_crown_diameter_m = ''
    self.fv_current_gps_information = ''
    self.fv_date_approved = ''
    self.fv_date_deleted = ''
    self.fv_date_first_observed = '' #
    self.fv_date_identified = '' #
    self.fv_date_measured = ''
    self.fv_date_published = ''
    self.fv_date_rejected = ''
    self.fv_date_submitted = ''
    self.fv_date_verified = '' 
    self.fv_dbh_cm = ''
    self.fv_deleted_by = ''
    self.fv_first_observed_by = '' #
    self.fv_first_occurrence_remarks = ''
    self.fv_florabase_taxon = ''
    self.fv_generic_taxon = ''
    self.fv_gps_info = ''
    self.fv_height_m = ''
    self.fv_hidden_variables = ''
    self.fv_horizontal_accuracy = ''
    self.fv_identification = ''
    self.fv_identification_audio_remarks = ''
    self.fv_identification_protocol = '' #
    self.fv_identification_qualifier = ''
    self.fv_identification_references = ''
    self.fv_identification_remarks = ''
    self.fv_identified_by = '' #
    self.fv_latitude = ''
    self.fv_leaf_area_index = ''
    self.fv_location = ''
    self.fv_longitude = ''
    self.fv_measured_by = ''
    self.fv_measurement_type = ''
    self.fv_number_of_rejections = ''
    self.fv_number_of_size_measurements = ''
    self.fv_plant_first_occurrence = ''
    self.fv_plant_id = ''
    self.fv_plant_photos = ''
    self.fv_plant_remarks = ''
    self.fv_plant_size = ''
    self.fv_plant_tagged = ''
    self.fv_plot = ''
    self.fv_plot_field_id = ''
    self.fv_plot_id = ''
    self.fv_published_by = ''
    self.fv_rejected_by = ''
    self.fv_scientific_name = ''
    self.fv_site = '' #
    self.fv_site_and_plot = ''
    self.fv_site_id = ''
    self.fv_site_plot_information = ''
    self.fv_size_measurements = ''
    self.fv_size_measurements_id = ''
    self.fv_submission = ''
    self.fv_submitted_by = ''
    self.fv_tag_id = ''
    self.fv_tag_remarks = ''
    self.fv_tag_type = ''
    self.fv_taxon = ''
    self.fv_taxon_checklist = '' #
    self.fv_taxon_id = ''
    self.fv_update_location_with_gps = ''
    self.fv_vascan_filter_geography = ''
    self.fv_vascan_filter_growth_form = ''
    self.fv_vascan_taxon = ''
    self.fv_verification = ''
    self.fv_verified_by = ''
    self.fv_vertical_accuracy = ''
  
  def __str__(self):
    return super(Plant, self).__str__()+'\n\n>fv_scientific_name {}'.format(self.fv_scientific_name)

def extract_plant_record(record):
  """ This will extract a plant panel record data from a record "form values"
  
  :param arg1: a SpectroscopyPanel to be tested
  :type arg1: SpectroscopyPanel

  :return: an updated record if it is validated or the record
  :rtype: SpectroscopyPanel
  """
  LO.l_info('Start extract leaf plant record id {}'.format(record.id))
  rv  = record.form_values
  if 'date_first_observed' in rv \
    and 'date_identified' in rv \
    and 'first_observed_by' in rv \
    and 'identification_protocol' in rv \
    and 'identified_by' in rv \
    and 'site' in rv \
    and 'taxon_checklist' in rv :
    if 'altitude' in rv: record.fv_altitude = rv['altitude']
    if 'approbation' in rv: record.fv_approbation = rv['approbation']
    if 'approved_by' in rv: record.fv_approved_by = rv['approved_by']
    if 'bryoquel_taxon' in rv: record.fv_bryoquel_taxon = rv['bryoquel_taxon']
    if 'close_up_photos' in rv: record.fv_close_up_photos = rv['close_up_photos']
    if 'corners_latitude' in rv: record.fv_corners_latitude = rv['corners_latitude']
    if 'corners_longitude' in rv: record.fv_corners_longitude = rv['corners_longitude']
    if 'crown_diameter_m' in rv: record.fv_crown_diameter_m = rv['crown_diameter_m']
    if 'current_gps_information' in rv: record.fv_current_gps_information = rv['current_gps_information']
    if 'data_quality_control' in rv: record.fv_data_quality_control = rv['data_quality_control']
    if 'date_approved' in rv: record.fv_date_approved = rv['date_approved']
    if 'date_deleted' in rv: record.fv_date_deleted = rv['date_deleted']
    if 'date_first_observed' in rv: record.fv_date_first_observed = rv['date_first_observed']
    if 'date_identified' in rv: record.fv_date_identified = rv['date_identified']
    if 'date_measured' in rv: record.fv_date_measured = rv['date_measured']
    if 'date_published' in rv: record.fv_date_published = rv['date_published']
    if 'date_rejected' in rv: record.fv_date_rejected = rv['date_rejected']
    if 'date_submitted' in rv: record.fv_date_submitted = rv['date_submitted']
    if 'date_verified' in rv: record.fv_date_verified = rv['date_verified']
    if 'dbh_cm' in rv: record.fv_dbh_cm = rv['dbh_cm']
    if 'deleted' in rv: record.fv_deleted = rv['deleted']
    if 'deleted_by' in rv: record.fv_deleted_by = rv['deleted_by']
    if 'first_observed_by' in rv: record.fv_first_observed_by = rv['first_observed_by']
    if 'first_occurrence_remarks' in rv: record.fv_first_occurrence_remarks = rv['first_occurrence_remarks']
    if 'florabase_taxon' in rv: record.fv_florabase_taxon = rv['florabase_taxon']
    if 'generic_taxon' in rv: record.fv_generic_taxon = rv['generic_taxon']
    if 'gps_info' in rv: record.fv_gps_info = rv['gps_info']
    if 'height_m' in rv: record.fv_height_m = rv['height_m']
    if 'hidden_variables' in rv: record.fv_hidden_variables = rv['hidden_variables']
    if 'horizontal_accuracy' in rv: record.fv_horizontal_accuracy = rv['horizontal_accuracy']
    if 'identification' in rv: record.fv_identification = rv['identification']
    if 'identification_audio_remarks' in rv: record.fv_identification_audio_remarks = rv['identification_audio_remarks']
    if 'identification_protocol' in rv: record.fv_identification_protocol = rv['identification_protocol']
    if 'identification_qualifier' in rv: record.fv_identification_qualifier = rv['identification_qualifier']
    if 'identification_references' in rv: record.fv_identification_references = rv['identification_references']
    if 'identification_remarks' in rv: record.fv_identification_remarks = rv['identification_remarks']
    if 'identified_by' in rv: record.fv_identified_by = rv['identified_by']
    if 'latitude' in rv: record.fv_latitude = rv['latitude']
    if 'leaf_area_index' in rv: record.fv_leaf_area_index = rv['leaf_area_index']
    if 'location' in rv: record.fv_location = rv['location']
    if 'longitude' in rv: record.fv_longitude = rv['longitude']
    if 'measured_by' in rv: record.fv_measured_by = rv['measured_by']
    if 'measurement_type' in rv: record.fv_measurement_type = rv['measurement_type']
    if 'number_of_rejections' in rv: record.fv_number_of_rejections = rv['number_of_rejections']
    if 'number_of_size_measurements' in rv: record.fv_number_of_size_measurements = rv['number_of_size_measurements']
    if 'plant' in rv: record.fv_plant = rv['plant']
    if 'plant_first_occurrence' in rv: record.fv_plant_first_occurrence = rv['plant_first_occurrence']
    if 'plant_id' in rv: record.fv_plant_id = rv['plant_id']
    if 'plant_photos' in rv: record.fv_plant_photos = rv['plant_photos']
    if 'plant_remarks' in rv: record.fv_plant_remarks = rv['plant_remarks']
    if 'plant_size' in rv: record.fv_plant_size = rv['plant_size']
    if 'plant_tagged' in rv: record.fv_plant_tagged = rv['plant_tagged']
    if 'plot' in rv: record.fv_plot = rv['plot']
    if 'plot_field_id' in rv: record.fv_plot_field_id = rv['plot_field_id']
    if 'plot_id' in rv: record.fv_plot_id = rv['plot_id']
    if 'publication' in rv: record.fv_publication = rv['publication']
    if 'published_by' in rv: record.fv_published_by = rv['published_by']
    if 'rejected_by' in rv: record.fv_rejected_by = rv['rejected_by']
    if 'rejection' in rv: record.fv_rejection = rv['rejection']
    if 'scientific_name' in rv: record.fv_scientific_name = rv['scientific_name']
    if 'site' in rv: record.fv_site = rv['site']
    if 'site_and_plot' in rv: record.fv_site_and_plot = rv['site_and_plot']
    if 'site_id' in rv: record.fv_site_id = rv['site_id']
    if 'site_plot_information' in rv: record.fv_site_plot_information = rv['site_plot_information']
    if 'size_measurements' in rv: record.fv_size_measurements = rv['size_measurements']
    if 'size_measurements_id' in rv: record.fv_size_measurements_id = rv['size_measurements_id']
    if 'submission' in rv: record.fv_submission = rv['submission']
    if 'submitted_by' in rv: record.fv_submitted_by = rv['submitted_by']
    if 'tag_id' in rv: record.fv_tag_id = rv['tag_id']
    if 'tag_remarks' in rv: record.fv_tag_remarks = rv['tag_remarks']
    if 'tag_type' in rv: record.fv_tag_type = rv['tag_type']
    if 'taxon' in rv: record.fv_taxon = rv['taxon']
    if 'taxon_checklist' in rv: record.fv_taxon_checklist = rv['taxon_checklist']
    if 'taxon_id' in rv: record.fv_taxon_id = rv['taxon_id']
    if 'update_location_with_gps' in rv: record.fv_update_location_with_gps = rv['update_location_with_gps']
    if 'vascan_filter_geography' in rv: record.fv_vascan_filter_geography = rv['vascan_filter_geography']
    if 'vascan_filter_growth_form' in rv: record.fv_vascan_filter_growth_form = rv['vascan_filter_growth_form']
    if 'vascan_taxon' in rv: record.fv_vascan_taxon = rv['vascan_taxon']
    if 'verification' in rv: record.fv_verification = rv['verification']
    if 'verified_by' in rv: record.fv_verified_by = rv['verified_by']
    if 'vertical_accuracy' in rv: record.fv_vertical_accuracy = rv['vertical_accuracy']
    
  else:
    tab = ['date_first_observed', 'date_identified', 'first_observed_by', 'identification_protocol', 'identified_by', 'site', 'taxon_checklist']
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


##############################################
# Get From Plants
##############################################

def get_scientific_name_with_plant_id(plantID):
  pls = load_plants()
  return get_scientific_name_with_plant_id_from_plants(plantID,pls)

def get_scientific_name_with_plant_id_from_plants(plantID,pls):
  if len(pls)>0 and plantID in pls.recordsDict:
    return pls.recordsDict[plantID].fv_scientific_name
  LO.l_war("No Scientific name associated with {}".format(plantID))
  return ''

def get_plant_with_plant_id_from_plants(plantID,pls=[]):
  if isinstance(pls,Plants):
    if len(pls)>0 and plantID in pls.recordsDict:
      return pls.recordsDict[plantID]
  elif len(pls)<1:
    return get_plant_with_plant_id_from_plants(plantID,load_plants())
  LO.l_war("No plant associated with {}".format(plantID))
  return ''

##############################################
# Get Plants
##############################################

def get_plants_from_records(recs):
  plants = Plants()
  for plant_raw in recs.records:
    plant = Plant(plant_raw)
    extract_plant_record(plant)
    if plant.isValid:
      plants.add_record(plant)
      st = 'The plant record id {} is complete for processing'.format(plant.id)
      LO.l_debug(st)
      plant.add_toLog(st)
    else:
      st = 'The plant record id {} is incomplete and will not be used'.format(plant.id)
      LO.l_war(st)
      plant.add_toLog(st)
  return plants
  
##############################################
# LOAD SOURCES
##############################################

# Load Plants from Plants Records File
def load_plants_from_json_file():
  if TO.file_is_here(PA.PlantsRecordsFile):
    records = RE.load_records_from_json(PA.PlantsRecordsFile)
    return get_plants_from_records(records)
  else:
    LO.l_err('The file {} is not available. A default empty Plants will be loaded'.format(PA.PlantsRecordsFile))
    return Plants()

# Load Plants from fulcrum
def load_plants_from_fulcrum():
  RE.backup_records_from_forms()
  return load_plants_from_json_file()

# Load from Plants form
def load_plants_from_plants_form():
  if TO.file_is_here(PA.PlantsFormFile):
    plants_form = FO.load_form_from_json_file(PA.PlantsFormFile)
    recs = RE.load_records_from_fulcrum(plants_form)
    return get_plants_from_records(recs)
  else:
    LO.l_err('The file {} is not available. A default empty Plants will be loaded'.format(PA.PlantsRecordsFile))
    return Plants()

# Load Plants
def load_plants():
  pls = load_plants_from_json_file()
  if len(pls) < 1:
    pls = load_plants_from_plants_form()
  if len(pls) < 1:
    pls = load_plants_from_fulcrum()
  return pls
