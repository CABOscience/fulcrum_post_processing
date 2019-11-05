#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
import parameters as PA
import tools as TO
import tools_fulcrum_api as TOFA
import logs as LO

# System
import sys

##############################################
# Record
##############################################

# OBJECTS
#########################
class Photos(object):
  def __init__(self):
    self.photos=[]
    self.photosDict={}
    
  def __len__(self):
    return len(self.photos)
    
  def get_photos(self):
    return self.photos
  
  def __str__(self):
    tp = ""
    for record in self.photos:
      if tp:
        tp += '\n'+photo
      else:
        tp = photo
    return tp

  def to_csv(self):
    tp = []
    for record in self.photos:
      tp.append(record.to_csv())
    return tp
  
  def add_record(self,photo_raw):
    self.photos.append(photo_raw)
    self.photosDict[photo_raw.id]=photo_raw


class Exif(object):
  def __init__(self, artist = "", color_space = "", date_time = "", date_time_digitized = "", date_time_original = "", digital_zoom_ratio = "", document_name = "", exposure_bias_value = "", exposure_mode = "", exposure_program = "", exposure_time = "", f_number = "", flash = "", focal_length = "", gps_altitude = "", gps_altitude_ref = "", gps_dop = "", gps_latitude = "", gps_latitude_ref = "", gps_longitude = "", gps_longitude_ref = "", image_description = "", image_length = "", image_width = "", iso_speed_ratings = "", light_source = "", make = "", metering_mode = "", model = "", pixel_x_dimension = "", pixel_y_dimension = "", resolution_unit = "", scene_capture_type = "", software = "", subsec_time = "", subsec_time_digitized = "", subsec_time_orginal = "", white_balance = "", x_resolution = "", y_resolution = "", ycb_cr_positioning = ""):
    self.artist = artist
    self.color_space = color_space
    self.date_time = date_time
    self.date_time_digitized = date_time_digitized
    self.date_time_original = date_time_original
    self.digital_zoom_ratio = digital_zoom_ratio
    self.document_name = document_name
    self.exposure_bias_value = exposure_bias_value
    self.exposure_mode = exposure_mode
    self.exposure_program = exposure_program
    self.exposure_time = exposure_time
    self.f_number = f_number
    self.flash = flash
    self.focal_length = focal_length
    self.gps_altitude = gps_altitude
    self.gps_altitude_ref = gps_altitude_ref
    self.gps_dop = gps_dop
    self.gps_latitude = gps_latitude
    self.gps_latitude_ref = gps_latitude_ref
    self.gps_longitude = gps_longitude
    self.gps_longitude_ref = gps_longitude_ref
    self.image_description = image_description
    self.image_length = image_length
    self.image_width = image_width
    self.iso_speed_ratings = iso_speed_ratings
    self.light_source = light_source
    self.make = make
    self.metering_mode = metering_mode
    self.model = model
    self.pixel_x_dimension = pixel_x_dimension
    self.pixel_y_dimension = pixel_y_dimension
    self.resolution_unit = resolution_unit
    self.scene_capture_type = scene_capture_type
    self.software = software
    self.subsec_time = subsec_time
    self.subsec_time_digitized = subsec_time_digitized
    self.subsec_time_orginal = subsec_time_orginal
    self.white_balance = white_balance
    self.x_resolution = x_resolution
    self.y_resolution = y_resolution
    self.ycb_cr_positioning = ycb_cr_positioning

def extract_exif_from_raw(exif_raw):
  artist, color_space, date_time, date_time_digitized, date_time_original, digital_zoom_ratio, document_name, exposure_bias_value, exposure_mode, exposure_program, exposure_time, f_number, flash, focal_length, gps_altitude, gps_altitude_ref, gps_dop, gps_latitude, gps_latitude_ref, gps_longitude, gps_longitude_ref, image_description, image_length, image_width, iso_speed_ratings, light_source, make, metering_mode, model, pixel_x_dimension, pixel_y_dimension, resolution_unit, scene_capture_type, software, subsec_time, subsec_time_digitized, subsec_time_orginal, white_balance, x_resolution, y_resolution, ycb_cr_positioning = ("",)*41
  if 'artist'               in exif_raw : artist = exif_raw ['artist']
  if 'color_space'          in exif_raw : color_space = exif_raw ['color_space']
  if 'date_time'            in exif_raw : date_time = exif_raw ['date_time']
  if 'date_time_digitized'  in exif_raw : date_time_digitized = exif_raw ['date_time_digitized']
  if 'date_time_original'   in exif_raw : date_time_original = exif_raw ['date_time_original']
  if 'digital_zoom_ratio'   in exif_raw : digital_zoom_ratio = exif_raw ['digital_zoom_ratio']
  if 'document_name'        in exif_raw : document_name = exif_raw ['document_name']
  if 'exposure_bias_value'  in exif_raw : exposure_bias_value = exif_raw ['exposure_bias_value']
  if 'exposure_mode'        in exif_raw : exposure_mode = exif_raw ['exposure_mode']
  if 'exposure_program'     in exif_raw : exposure_program = exif_raw ['exposure_program']
  if 'exposure_time'        in exif_raw : exposure_time = exif_raw ['exposure_time']
  if 'f_number'             in exif_raw : f_number = exif_raw ['f_number']
  if 'flash'                in exif_raw : flash = exif_raw ['flash']
  if 'focal_length'         in exif_raw : focal_length = exif_raw ['focal_length']
  if 'gps_altitude'         in exif_raw : gps_altitude = exif_raw ['gps_altitude']
  if 'gps_altitude_ref'     in exif_raw : gps_altitude_ref = exif_raw ['gps_altitude_ref']
  if 'gps_dop'              in exif_raw : gps_dop = exif_raw ['gps_dop']
  if 'gps_latitude'         in exif_raw : gps_latitude = exif_raw ['gps_latitude']
  if 'gps_latitude_ref'     in exif_raw : gps_latitude_ref = exif_raw ['gps_latitude_ref']
  if 'gps_longitude'        in exif_raw : gps_longitude = exif_raw ['gps_longitude']
  if 'gps_longitude_ref'    in exif_raw : gps_longitude_ref = exif_raw ['gps_longitude_ref']
  if 'image_description'    in exif_raw : image_description = exif_raw ['image_description']
  if 'image_length'         in exif_raw : image_length = exif_raw ['image_length']
  if 'image_width'          in exif_raw : image_width = exif_raw ['image_width']
  if 'iso_speed_ratings'    in exif_raw : iso_speed_ratings = exif_raw ['iso_speed_ratings']
  if 'light_source'         in exif_raw : light_source = exif_raw ['light_source']
  if 'make'                 in exif_raw : make = exif_raw ['make']
  if 'metering_mode'        in exif_raw : metering_mode = exif_raw ['metering_mode']
  if 'model'                in exif_raw : model = exif_raw ['model']
  if 'pixel_x_dimension'    in exif_raw : pixel_x_dimension = exif_raw ['pixel_x_dimension']
  if 'pixel_y_dimension'    in exif_raw : pixel_y_dimension = exif_raw ['pixel_y_dimension']
  if 'resolution_unit'      in exif_raw : resolution_unit = exif_raw ['resolution_unit']
  if 'scene_capture_type'   in exif_raw : scene_capture_type = exif_raw ['scene_capture_type']
  if 'software'             in exif_raw : software = exif_raw ['software']
  if 'subsec_time'          in exif_raw : subsec_time = exif_raw ['subsec_time']
  if 'subsec_time_digitized' in exif_raw : subsec_time_digitized = exif_raw ['subsec_time_digitized']
  if 'subsec_time_orginal'  in exif_raw : subsec_time_orginal = exif_raw ['subsec_time_orginal']
  if 'white_balance'        in exif_raw : white_balance = exif_raw ['white_balance']
  if 'x_resolution'         in exif_raw : x_resolution = exif_raw ['x_resolution']
  if 'y_resolution'         in exif_raw : y_resolution = exif_raw ['y_resolution']
  if 'ycb_cr_positioning'   in exif_raw : ycb_cr_positioning = exif_raw ['ycb_cr_positioning']
  
  return Exif(artist, color_space, date_time, date_time_digitized, date_time_original, digital_zoom_ratio, document_name, exposure_bias_value, exposure_mode, exposure_program, exposure_time, f_number, flash, focal_length, gps_altitude, gps_altitude_ref, gps_dop, gps_latitude, gps_latitude_ref, gps_longitude, gps_longitude_ref, image_description, image_length, image_width, iso_speed_ratings, light_source, make, metering_mode, model, pixel_x_dimension, pixel_y_dimension, resolution_unit, scene_capture_type, software, subsec_time, subsec_time_digitized, subsec_time_orginal, white_balance, x_resolution, y_resolution, ycb_cr_positioning)

class Photo(object):
  def __init__(self, access_key = "", content_type = "", created_at = "", created_by = "", created_by_id = "", deleted_at = "", exif = "", file_size = "", form_id = "", large = "", latitude = "", longitude = "", original = "", processed = "", record_id = "", stored = "", thumbnail = "", updated_at = "", updated_by = "", updated_by_id = "", uploaded = "", url = ""):
    self.access_key = access_key
    self.content_type = content_type
    self.created_at = created_at
    self.created_by = created_by
    self.created_by_id = created_by_id
    self.deleted_at = deleted_at
    self.exif = ""
    if exif:
      self.exif = extract_exif_from_raw(exif_raw)
    self.file_size = file_size
    self.form_id = form_id
    self.large = large
    self.latitude = latitude
    self.longitude = longitude
    self.original = original
    self.processed = processed
    self.record_id = record_id
    self.stored = stored
    self.thumbnail = thumbnail
    self.updated_at = updated_at
    self.updated_by = updated_by
    self.updated_by_id = updated_by_id
    self.uploaded = uploaded
    self.url = url
    self.isValid = True
    self.logInfo = ""
     

  def __str__(self):
    return '>access key {} - form {} - record {}'.format(self.access_key, self.form_id, self.record_id)

  def to_csv(self):
    return []

  def to_info(self):
    return []

  #def whoami(self):
  #  print type(self).__name__
    
  def is_image(self):
    if self.access_key and self.form_id and sefl.record_id:
      return True
    else:
      LO.l_war('The image has (no) ID ({}) and/or "form_id" ({}) and/or "record_id" ({}). We will not be able to process it.'.format(self.access_key, self.form_id, self.record_id))
      self.add_toLog('The image has (no) ID ({}) and/or "form_id" ({}) and/or "record_id" ({}). We will not be able to process it.'.format(self.access_key, self.form_id, self.record_id))
      return False
      
  def add_toLog(self, st):
    if not isinstance(st, basestring):
      print 'st'
      print st
    else:
     self.logInfo += "\n"+st

##############################################
# photos Functions
##############################################

def get_photos_from_directory(fileDirectory):
  # load all json photos from a directory
  return TO.load_json_file(fileName)

def get_photos_from_files_list(listFilePhotos):
  photos = Photos()
  for filePhoto in listfilePhotos:
    photo_raw = get_photo_from_fileName(filePhoto)
    if record_raw:
      project_name = projects[photo_raw.project_id]
      photos.add_record(photo_raw)
  return photos

def get_photo_from_fileName(fileName):
  photo_raw = TO.load_json_file(fileName)
  return extract_photo_from_raw(photo_raw)

def get_photos_from_records_file(fileRecords):
  # load records of a form and extract all photos
  return TO.load_json_file(fileName)

def get_photos_from_form_file(fileRecords):
  # load records of a form and extract all photos
  return TO.load_json_file(fileName)

def get_photos_from_records_list(listRecords,projects=[]):
  records = Records()
  for record_raw in listRecords:
    record = extract_record_from_raw(record_raw,projects)
    records.add_record(record)
  return records

def extract_photo_from_raw(photo_raw):
  access_key, content_type, created_at, created_by, created_by_id, deleted_at, exif, file_size, form_id, large, latitude, longitude, original, processed, record_id, stored, thumbnail, updated_at, updated_by, updated_by_id, uploaded, url = ("",)*22
  if 'access_key'   in photo_raw : access_key = photo_raw['access_key']
  if 'content_type' in photo_raw : content_type = photo_raw['content_type']
  if 'created_at'   in photo_raw : created_at = photo_raw['created_at']
  if 'created_by'   in photo_raw : created_by = photo_raw['created_by']
  if 'created_by_id' in photo_raw : created_by_id = photo_raw['created_by_id']
  if 'deleted_at'   in photo_raw : deleted_at = photo_raw['deleted_at']
  if 'exif'         in photo_raw : exif = photo_raw['exif']
  if 'file_size'    in photo_raw : file_size = photo_raw['file_size']
  if 'form_id'      in photo_raw : form_id = photo_raw['form_id']
  if 'large'        in photo_raw : large = photo_raw['large']
  if 'latitude'     in photo_raw : latitude = photo_raw['latitude']
  if 'longitude'    in photo_raw : longitude = photo_raw['longitude']
  if 'original'     in photo_raw : original = photo_raw['original']
  if 'processed'    in photo_raw : processed = photo_raw['processed']
  if 'record_id'    in photo_raw : record_id = photo_raw['record_id']
  if 'stored'       in photo_raw : stored = photo_raw['stored']
  if 'thumbnail'    in photo_raw : thumbnail = photo_raw['thumbnail']
  if 'updated_at'   in photo_raw : updated_at = photo_raw['updated_at']
  if 'updated_by'   in photo_raw : updated_by = photo_raw['updated_by']
  if 'updated_by_id' in photo_raw : updated_by_id = photo_raw['updated_by_id']
  if 'uploaded'     in photo_raw : uploaded = photo_raw['uploaded']
  if 'url'          in photo_raw : url = photo_raw['url']
  return Photo(access_key, content_type, created_at, created_by, created_by_id, deleted_at, exif, file_size, form_id, large, latitude, longitude, original, processed, record_id, stored, thumbnail, updated_at, updated_by, updated_by_id, uploaded, url)


# Photos sub functions
# Recursive search for photos id
def search_for_photo_id(record):
  photos = []
  if record.form_values:
    photos += search_for_photo_id_recu(photos,record.form_values)
  return photos
  
def search_for_photo_id_recu(photos,info):
  if isinstance(info, list):
    for v in info:
      if v:
        photos = search_for_photo_id_recu(photos,v)
  elif isinstance(info, dict):
    for k in info.keys():
      v = info[k]
      if 'photo_id' in k:
        #print 'photo_id value >'+v+'<<'
        photos+=[v]
      elif v:
        photos = search_for_photo_id_recu(photos,v)
  return photos

# Photo image
def get_photo_file_name(bName,photoID):
  return bName+'/images/'+photoID+'.jpg'

# Photo Metadata
def get_photo_meta_file_name(bName,photoID):
  return bName+'/images/'+photoID+'.json'

def backup_photos_from_records(form,recs):
  formName = form.name_cleaned
  bName = TO.get_FormsPath()+""+formName
  photosID = []
  LO.l_info('Start searching photos for the form "{}" with {} records'.format(formName,len(recs)))
  for record in recs.records:
    photosID += search_for_photo_id(record)
  
  if photosID and len(photosID)>0:
    photosID = list(set(photosID))
    
  LO.l_info('Start backup photos for the form "{}" with {} records'.format(formName,len(recs)))
  for photoID in photosID:
    fname = get_photo_file_name(bName,photoID)
    if not TO.file_is_here(fname):
      photoOb = TOFA.get_photo_file(photoID)
      if photoOb:
        LO.l_debug('Start save photo in "{}" with photo ID {}'.format(fname,photoID))
        TO.photo_to_file(fname,photoOb)
    fname = get_photo_meta_file_name(bName,photoID)
    if not TO.file_is_here(fname):
      photoMeta = TOFA.get_photo_meta(photoID)
      if photoMeta:
        LO.l_debug('Start save photo meta in "{}" with photo ID {}'.format(fname,photoID))
        TO.save_in_json_file(fname,photoMeta)
    


##############################################
# LOAD SOURCES
##############################################

# Load from Webhooks
##############################################
def load_webhook_photos(projects=[]):
  webhookRecords = TO.get_files_from_path(PA.FulcrumWebhook+"records/")
  return get_photos_from_files_list(webhookRecords,projects)

# Load from File Name
##############################################
def load_photos_from_json(fileName,projects=[]):
  listRecords = get_list_records_from_file(fileName)
  return get_records_from_list(listRecords,projects)


##############################################
# Update Record with dataname
##############################################
def record_add_dataname_from_formFile(record,formFile):
  form_raw = TO.load_json_file(formFile)
  dictKeysDataname = form_raw['dictKeysDataname']
  if 'form_values' in record:
    search_datanames_keys_recu(dictKeysDataname,record['form_values'])

# Records sub functions
# Recursive search for keys to dataname
def search_datanames_keys_recu(dictKeysDataname,info):
  if isinstance(info, list):
    for v in info:
      if v:
        search_for_keys_recu(dictKeysDataname,v)
  elif isinstance(info, dict):
    for k in info.keys():
      if k in dictKeysDataname:
        info[dictKeysDataname[k]] = info.pop(k)
    for v in info.values():
      search_for_keys_recu(dictKeysDataname,v)

