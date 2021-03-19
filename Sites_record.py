#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
import projects as PR
import parameters as PA
import records as RE
import tools as TO
import logs as LO

# Spectroscopy
#import specdal
# System
import sys

##############################################
# OBJECTS
##############################################

class Sites(RE.Records):
  """ Sites object
  Sites object is containing a list of Sites Object
  """

class Site(RE.Record):
  def __init__(self, record):
    super(Site,self).__init__(record.altitude, record.assigned_to, record.assigned_to_id, record.client_created_at, record.client_updated_at, record.course, record.created_at, record.created_by, record.created_by_id, record.created_duration, record.created_location, record.edited_duration, record.form_id, record.form_name, record.form_values, record.horizontal_accuracy, record.id, record.latitude, record.longitude, record.project_id, record.speed, record.status, record.updated_at, record.updated_by, record.updated_by_id, record.updated_duration, record.updated_location, record.version, record.vertical_accuracy, record.project_name)
    self.fv_approbation = ''
    self.fv_approved_by = ''
    self.fv_continent = ''
    self.fv_corner_latitude = ''
    self.fv_corner_longitude = ''
    self.fv_corner_number = ''
    self.fv_corners = '' # doute
    self.fv_corners_latitude = ''
    self.fv_corners_longitude = ''
    self.fv_country = ''
    self.fv_data_quality_control = ''
    self.fv_date_approved = ''
    self.fv_date_defined = '' #
    self.fv_date_deleted = ''
    self.fv_date_published = ''
    self.fv_date_rejected = ''
    self.fv_date_submitted = ''
    self.fv_date_verified = ''
    self.fv_deleted = ''
    self.fv_deleted_by = ''
    self.fv_first_defined_by = '' #
    self.fv_hidden_variables = ''
    self.fv_municipality = ''
    self.fv_number_of_corners = ''
    self.fv_number_of_rejections = ''
    self.fv_optional_site_info = ''
    self.fv_original_purpose = '' #
    self.fv_publication = ''
    self.fv_published_by = ''
    self.fv_rejected_by = ''
    self.fv_rejection = ''
    self.fv_site = ''
    self.fv_site_audio_remarks = ''
    self.fv_site_geometry = ''
    self.fv_site_id = ''
    self.fv_site_latitude = ''
    self.fv_site_longitude = ''
    self.fv_site_photos = ''
    self.fv_site_remarks = ''
    self.fv_state_province = ''
    self.fv_submission = ''
    self.fv_submitted_by = ''
    self.fv_verbatim_site = ''
    self.fv_verification = ''
    self.fv_verified_by = ''

  def __str__(self):
    return super(Site, self).__str__()+'\n\n>fv_original_purpose {}'.format(self.fv_original_purpose)


def extract_site_record(record):
  """ This will extract a spectroscopy panel record data from a record "form values"
  
  :param arg1: a SpectroscopyPanel to be tested
  :type arg1: SpectroscopyPanel

  :return: an updated record if it is validated or the record
  :rtype: SpectroscopyPanel
  """
  LO.l_info('Start extract leaf spectra recordid {}'.format(record.id))
  rv  = record.form_values

  if 'corners' in rv \
    and 'date_defined' in rv \
    and 'first_defined_by' in rv \
    and 'original_purpose' in rv :
    if 'approbation' in rv: record.fv_approbation = rv['approbation']
    if 'approved_by' in rv: record.fv_approved_by = rv['approved_by']
    if 'continent' in rv: record.fv_continent = rv['continent']
    if 'corner_latitude' in rv: record.fv_corner_latitude = rv['corner_latitude']
    if 'corner_longitude' in rv: record.fv_corner_longitude = rv['corner_longitude']
    if 'corner_number' in rv: record.fv_corner_number = rv['corner_number']
    if 'corners' in rv: record.fv_corners = rv['corners']
    if 'corners_latitude' in rv: record.fv_corners_latitude = rv['corners_latitude']
    if 'corners_longitude' in rv: record.fv_corners_longitude = rv['corners_longitude']
    if 'country' in rv: record.fv_country = rv['country']
    if 'data_quality_control' in rv: record.fv_data_quality_control = rv['data_quality_control']
    if 'date_approved' in rv: record.fv_date_approved = rv['date_approved']
    if 'date_defined' in rv: record.fv_date_defined = rv['date_defined']
    if 'date_deleted' in rv: record.fv_date_deleted = rv['date_deleted']
    if 'date_published' in rv: record.fv_date_published = rv['date_published']
    if 'date_rejected' in rv: record.fv_date_rejected = rv['date_rejected']
    if 'date_submitted' in rv: record.fv_date_submitted = rv['date_submitted']
    if 'date_verified' in rv: record.fv_date_verified = rv['date_verified']
    if 'deleted' in rv: record.fv_deleted = rv['deleted']
    if 'deleted_by' in rv: record.fv_deleted_by = rv['deleted_by']
    if 'first_defined_by' in rv: record.fv_first_defined_by = rv['first_defined_by']
    if 'hidden_variables' in rv: record.fv_hidden_variables = rv['hidden_variables']
    if 'municipality' in rv: record.fv_municipality = rv['municipality']
    if 'number_of_corners' in rv: record.fv_number_of_corners = rv['number_of_corners']
    if 'number_of_rejections' in rv: record.fv_number_of_rejections = rv['number_of_rejections']
    if 'optional_site_info' in rv: record.fv_optional_site_info = rv['optional_site_info']
    if 'original_purpose' in rv: record.fv_original_purpose = rv['original_purpose']
    if 'publication' in rv: record.fv_publication = rv['publication']
    if 'published_by' in rv: record.fv_published_by = rv['published_by']
    if 'rejected_by' in rv: record.fv_rejected_by = rv['rejected_by']
    if 'rejection' in rv: record.fv_rejection = rv['rejection']
    if 'site' in rv: record.fv_site = rv['site']
    if 'site_audio_remarks' in rv: record.fv_site_audio_remarks = rv['site_audio_remarks']
    if 'site_geometry' in rv: record.fv_site_geometry = rv['site_geometry']
    if 'site_id' in rv: record.fv_site_id = rv['site_id']
    if 'site_latitude' in rv: record.fv_site_latitude = rv['site_latitude']
    if 'site_longitude' in rv: record.fv_site_longitude = rv['site_longitude']
    if 'site_photos' in rv: record.fv_site_photos = rv['site_photos']
    if 'site_remarks' in rv: record.fv_site_remarks = rv['site_remarks']
    if 'state_province' in rv: record.fv_state_province = rv['state_province']
    if 'submission' in rv: record.fv_submission = rv['submission']
    if 'submitted_by' in rv: record.fv_submitted_by = rv['submitted_by']
    if 'verbatim_site' in rv: record.fv_verbatim_site = rv['verbatim_site']
    if 'verification' in rv: record.fv_verification = rv['verification']
    if 'verified_by' in rv: record.fv_verified_by = rv['verified_by']


  else:
    tab = ['corners', 'date_defined', 'first_defined_by', 'original_purpose']
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
# Get From Sites
##############################################

def get_site_with_site_id(siteID):
  sts = load_sites()
  return get_site_with_site_id_from_sites(siteID,sts)

def get_site_with_site_id_from_sites(siteID,sts):
  if len(sts)>0 and siteID in sts.recordsDict:
    return sts.recordsDict[siteID]
  LO.l_war("No site associated with {}".format(siteID))
  return ''


##############################################
# Get Sites
##############################################

def get_sites_from_records(recs):
  sites = Sites()
  for site_raw in recs.records:
    site = Site(site_raw)
    extract_site_record(site)
    if site.isValid:
      sites.add_record(site)
      st = 'The site record id {} is complete for processing'.format(site.id)
      LO.l_debug(st)
      site.add_toLog(st)
    else:
      st = 'The site record id {} is incomplete and will not be used'.format(site.id)
      LO.l_war(st)
      site.add_toLog(st)
  return sites
  
##############################################
# LOAD SOURCES
##############################################

# Load Sites from Sites Records File
def load_sites_from_json_file():
  if TO.file_is_here(PA.SitesRecordsFile):
    records = RE.load_records_from_json(PA.SitesRecordsFile)
    return get_sites_from_records(records)
  else:
    LO.l_err('The file {} is not available. A default empty Sites will be loaded'.format(PA.SitesRecordsFile))
    return Sites()

# Load Sites from fulcrum
def load_sites_from_fulcrum():
  #RE.backup_records_from_forms()
  return load_sites_from_json_file()

# Load from Sites form
def load_sites_from_form():
  if TO.file_is_here(PA.SitesFormFile):
    sites_form = FO.load_form_from_json_file(PA.SitesFormFile)
    recs = RE.load_records_from_fulcrum(sites_form)
    return get_sites_from_records(recs)
  else:
    LO.l_err('The file {} is not available. A default empty Sites will be loaded'.format(PA.SitesRecordsFile))
    return Sites()

# Load Sites
def load_sites():
  pls = load_sites_from_json_file()
  if len(pls) < 1:
    pls = load_sites_from_form()
  if len(pls) < 1:
    pls = load_sites_from_fulcrum()
  return pls
