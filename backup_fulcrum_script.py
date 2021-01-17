#!/usr/bin/env python
import urllib2, json, argparse, io, requests, sys, os.path, copy, logging
from fulcrum import Fulcrum
from fulcrum.exceptions import NotFoundException, InvalidAPIVersionException, UnauthorizedException, InternalServerErrorException, RateLimitExceededException
from datetime import date

'''
Command lines to install fulcrum api
$ sudo apt-get update
$ sudo apt-get install git
$ git clone https://github.com/fulcrumapp/fulcrum-python.git
$ cd fulcrum-python/
$ python setup.py build
$ sudo python setup.py install

Object:
fulcrumApp = connection to fulcrum
forms      = [] a json like https://developer.fulcrumapp.com/endpoints/forms/#form-properties
records    = [] a json like https://developer.fulcrumapp.com/endpoints/records/#record-properties
images     = [] a json like https://developer.fulcrumapp.com/endpoints/photos/#photo-properties

It saves logs in a subdirectory ./logs/ 

It creates 4 types of fulcrum backups :
- two types of fulcrum backups (with and without version)
- two types of fulcrum backups (with and without dataname)

Structure of a saved form:
[fulcrumPath]/form-name
[fulcrumPath]/form-name/images
[fulcrumPath]/form-name/versions

Usage:
python backup_fulcrum_script.py [-h] [-a FULCRUMAPIKEY] [-f FORMS [FORMS ...]]
                                [-p PATH]

Options Fulcrum Backup.

required arguments:
  -a FULCRUMAPIKEY, --fulcrumApiKey FULCRUMAPIKEY
                        Need a fulcrum Api key

optional arguments:
  -f FORMS [FORMS ...], --forms FORMS [FORMS ...]
                        Select specific forms by name or id. Example: -f Plots
                        Sites 'Bulk Leaf Samples' 'Vegetation Surveys: Herbs
                        and Shrubs'
  -p PATH, --path PATH  Choose a directory for backup


'''
# Global variables
fulcrumApiKey = ''    # Load with in agrument -a
fulcrumForms  = {}    # Load with in agrument -f
fulcrumPath   = './'  # Load with in agrument -p
fulcrumApiURL = 'https://api.fulcrumapp.com/api/v2/'
keys_dataname = {}
notFoundStr       = 'because it was not found.'
limitExceededStr  = 'because you have exceeded the number of request.'
numberOfRequest   = 0


##############################################
#
# MAIN FUNCTION
#
##############################################
def main():
  today = str(date.today())
  logPath = get_script_directory()+"/logs/"
  if not os.path.exists(logPath):
    os.makedirs(logPath)
  logFilename = logPath+today+"_backup_fulcrum_script.log"
  logging.basicConfig(name="bibou", level=logging.INFO,
                      filename=logFilename, filemode="a+",
                      format="%(asctime)-15s %(levelname)-8s %(message)s")
  # Get Fulcrum access and forms
  fulcrumApp, forms = get_fulcrum_access()
  
  projectsID = {}
  for form in forms:
    formName = clean_name(form['name'])
    formID   = form['id']
    

    #print ('formName {}'.format(formName))
    # Backup form
    backup_form(formName,form)
    
    # Backup records
    records = backup_records(formID,formName,fulcrumApp)
    
    # Backup records versions
    backupVersion = False
    if 'script' in form and form['script']:
      if '/* SAVE VERSIONS */' in form['script']:
        backupVersion = True
    
    if backupVersion:
      recordsVersions = backup_records_versions(formID,formName,fulcrumApp,records)
    else:
      logger = logging.getLogger("bibou")
      logger.warning("No records versions for {st} will not be saved.\n\
                      If you need to saved records versions for {st}.\n\
                      Please add /* SAVE VERSIONS */ in the top of it's 'data events'\n\
                      ".format(st=formName))
    
    # Backup images
    images  = backup_images(formName,fulcrumApp,recordsVersions)
    
    # Extract projects
    projectsID = extract_projects(projectsID,recordsVersions)
    
    print_num_of_request()
  
  # Backup projects
  backup_projects(projectsID,fulcrumApp)
  print_num_of_request()


##############################################
# Get arguments and return fulcrum access and forms
##############################################
def get_fulcrum_access():
  logger = logging.getLogger("bibou")
  parser = argparse.ArgumentParser(description='Options Fulcrum Backup.')
  parser._action_groups.pop()
  required = parser.add_argument_group('required arguments')
  optional = parser.add_argument_group('optional arguments')
  required.add_argument('-a', '--fulcrumApiKey',
    dest="fulcrumApiKey", help="Need a fulcrum Api key")
  optional.add_argument('-f', '--forms', nargs='+', type=str,
    dest="forms", help="Select specific forms by name or id. \
                        Example: -f Plots Sites 'Bulk Leaf Samples' 'Vegetation Surveys: Herbs and Shrubs'")
  optional.add_argument('-p', '--path', type=str,
    dest="path", help="Choose a directory for backup")
  args = parser.parse_args()
  
  global fulcrumApiKey
  fulcrumApiKey = args.fulcrumApiKey
  global fulcrumForms
  fulcrumForms  = args.forms
  global fulcrumPath
  if args.path:
    argPath = args.path
    argPath = os.path.expanduser(argPath)
    argPath = os.path.abspath(argPath)
    if (os.path.isdir(argPath)):
      if not argPath.endswith('/'):
        argPath = argPath+'/'
      fulcrumPath = argPath
    else:
      logger.warning('The current path is not a directory. The program will used the default path: >> {}'.format(fulcrumPath))
  fulcrumApp  = Fulcrum(key=fulcrumApiKey)
  formsTmp = {}
  try:
    formsTmp = fulcrumApp.forms.search()['forms']
    increase_num_of_request_by(1)
  except (UnauthorizedException,
          InvalidAPIVersionException,
          InternalServerErrorException
          ):
    if not fulcrumApiKey:
      print parser.print_help()
    else:
      s = 'Connexion to Fulcrum has failed due to'
      endString = ''
      if UnauthorizedException:
        endString = 'unauthorized API Key.'
      elif InvalidAPIVersionException:
        endString = 'invalid API version.'
      elif InternalServerErrorException:
        endString = 'internal server error.'
      logger.error(s+' '+endString)
    sys.exit(1)
  except (NotFoundException, RateLimitExceededException):
    s = 'Search forms has failed'
    endString = ''
    if NotFoundException:
      endString = notFoundStr
    elif RateLimitExceededException:
      endString = limitExceededStr
    logger.error(s+' '+endString)
    sys.exit(1)
  
  forms = []
  if fulcrumForms:
    for form in formsTmp:
      for fulcrumForm in fulcrumForms:
        if form['id'] == fulcrumForm:
          forms+=[form]
        if form['name'] == fulcrumForm:
          forms+=[form]
  else:
    forms = formsTmp
  logger.info('The number of backuped forms will be {}'.format(len(forms)))
  return fulcrumApp, forms


##############################################
# Forms
##############################################
# Extract Forms
def backup_form(formName,form):
  # Create directories for formName
  create_form_directories(formName)
  fname = fulcrumPath+formName+'/'+formName+'_form.json'
  extract_keys_dataname(form)
  save_file(fname,form)

def create_form_directories(formName):
  directories = ['versions', 'images']
  for directory in directories:
    directory = fulcrumPath+formName+'/'+directory
    if not os.path.exists(directory):
      os.makedirs(directory)

def extract_keys_dataname(form):
  dictKeysDataname = {}
  search_for_keys_form_recu(dictKeysDataname,form)
  form['dictKeysDataname'] =  dictKeysDataname
  global keys_dataname
  keys_dataname[form['id']] = dictKeysDataname
  
# Forms sub functions
# Recursive search for keys to dataname
def search_for_keys_form_recu(keysDataname,info):
  if isinstance(info, list):
    for v in info:
      if v:
        search_for_keys_form_recu(keysDataname,v)
  elif isinstance(info, dict):
    if 'elements' in info:
      search_for_keys_form_recu(keysDataname,info['elements'])
    if 'data_name' in info and 'key' in info:
      keysDataname[info['key']]=info['data_name']
    
    for vs in info.values():
      if isinstance(vs, list):
        for v in vs:
          if v:
            search_for_keys_form_recu(keysDataname,v)


##############################################
# Records
##############################################
# Backup Records
def backup_records(formID,formName,fulcrumApp):
  logger = logging.getLogger("bibou")
  records = {}
  try:
    records = fulcrumApp.records.search(url_params={'form_id': formID})
  except NotFoundException, RateLimitExceededException:
    s = 'Search records has failed for form '+formName
    endString = ''
    if NotFoundException:
      endString = notFoundStr
    elif RateLimitExceededException:
      endString = limitExceededStr
    logger.error('{} {}'.format(s,endString))
    sys.exit(1)
    
  bName = get_file_basename(formName)
  fname       = bName+'/'+formName+'_records.json'
  numRecords  = len(records['records'])
  save_file(fname,records['records'])
  fname       = bName+'/'+formName+'_records_with_dataname.json'
  recordsWithDataname = update_records_with_dataname(formID,records['records'])
  save_file(fname,recordsWithDataname)
  increase_num_of_request_by(1)
  
  logger.info('There are {} records for the form "{}"'.format(numRecords,formName))
  return records['records']

def update_records_with_dataname(formID,records):
  recordTemp = copy.deepcopy(records)
  for record in recordTemp:
    if 'form_values' in record:
      search_for_keys_recu(formID,record['form_values'])
  return recordTemp
    
# Records sub functions
# Recursive search for keys to dataname
def search_for_keys_recu(formID,info):
  if isinstance(info, list):
    for v in info:
      if v:
        search_for_keys_recu(formID,v)
  elif isinstance(info, dict):
    for k in info.keys():
      if k in keys_dataname[formID]:
        info[keys_dataname[formID][k]] = info.pop(k)
    for v in info.values():
      search_for_keys_recu(formID,v)

# Backup records versions
def backup_records_versions(formID,formName,fulcrumApp,records):
  recordsHistoryList = []
  for record in records:
    latestVersion = record['version']
    recordID      = record['id']
    fname         = get_history_record_file_name(formName,recordID)
    recordsHistory= get_history_record(fname)
    boo           = True

    if len(recordsHistory)>0:
      historyVersion = get_history_record_version(recordsHistory)
      if (latestVersion == historyVersion):
        boo = False
    
    if not boo and latestVersion > 1:
      recordsHistory = get_record_history(fulcrumApp,recordID)
      save_file(fname,recordsHistory)

      # add records versions from backup file
      for recordHistory in recordsHistory:
        if recordHistory['version'] != latestVersion:
          recordsHistoryList += [recordHistory]
    
  records += recordsHistoryList
  bName = get_file_basename(formName)
  fname    = bName+'/'+formName+'_records_versions.json'
  save_file(fname,records)
  fname    = bName+'/'+formName+'_records_versions_with_dataname.json'
  recordsWithDataname = update_records_with_dataname(formID,records)
  save_file(fname,recordsWithDataname)
  return records

# Record history
def get_history_record_file_name(formName,recordID):
  bName = get_file_basename(formName)
  return bName+'/versions/'+recordID+'_versions.json'

def get_history_record(fname):
  if os.path.isfile(fulcrumPath+fname):
    with open(fname) as f:
      return json.load(f)
  return []
  
def get_record_history(recordID):
  logger = logging.getLogger("bibou")
  url = fulcrumApiURL+'/records/'+recordID+'/history.json?token='+fulcrumApiKey
  r = requests.get(url)
  increase_num_of_request_by(1)

  if '200' in str(r):
    return r.json()['records']
  else:
    logger.warning('The version request has not working for {}'.format(recordID))
    return []

def get_history_record_version(records):
  latestVersion = 0
  for record in records:
    if record['version'] > latestVersion:
      latestVersion = record['version']
  return latestVersion


##############################################
# Images
##############################################
def backup_images(formName,fulcrumApp,records):
  bName = get_file_basename(formName)
  photosID = []
  for record in records:
    photosID += search_for_photo_id(record)
  
  if photosID and len(photosID)>0:
    photosID = list(set(photosID))
    
  for photoID in photosID:
    fname = get_photo_file_name(bName,photoID)
    photoSaved = file_is_here(fname)
    if not photoSaved:
      download_photo(fname,fulcrumApp,photoID)
    fname = get_photo_meta_file_name(bName,photoID)
    photoMetaSaved = file_is_here(fname)
    if not photoMetaSaved:
      photoMeta = download_photo_meta(fname,fulcrumApp,photoID)
      save_file(fname,photoMeta)
    
# Photos sub functions
# Recursive search for photos id
def search_for_photo_id(record):
  photos = []
  if 'form_values' in record:
    photos += search_for_photo_id_recu(photos,record['form_values'])
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

def download_photo(fname,fulcrumApp,photoID):
  logger = logging.getLogger("bibou")
  try:
    photo = fulcrumApp.photos.media(photoID)
    increase_num_of_request_by(1)
    with open(fname, 'wb') as f:
      f.write(photo)
  
  except NotFoundException, RateLimitExceededException:
    s = 'Search photos has failed for photo '+photoID
    if NotFoundException:
      logger.warning('{} {}'.format(s,notFoundStr))
      pass
    elif RateLimitExceededException:
      logger.error('{} {}'.format(s,limitExceededStr))
      sys.exit(1)

# Photo Metadata
def get_photo_meta_file_name(bName,photoID):
  return bName+'/images/'+photoID+'.json'

def download_photo_meta(fname,fulcrumApp,photoID):
  logger = logging.getLogger("bibou")
  url = fulcrumApiURL+'/photos/'+photoID+'.json?token='+fulcrumApiKey
  r = requests.get(url)
  increase_num_of_request_by(1)

  if '200' in str(r):
    return r.json()
  else:
    logger.warning('The metadata request has not working for photo {}'.format(photoID))
    return []


##############################################
# Projects
##############################################

def extract_projects(projectsID,records):
  for record in records:
    if 'project_id' in record and record['project_id']:
        projectsID[record['project_id']] = ''
  return projectsID

def backup_projects(projectsID,fulcrumApp):
  bName = get_file_basename('Projects')
  if not os.path.exists(bName):
    os.makedirs(bName)

  for projectID in projectsID.keys():
    # download json project
    project = get_project(projectID,fulcrumApp)
    projectName = project['project']['name']
    # create file with project name
    fname = get_project_file_name(bName,projectName)
    save_file(fname,project)
    
def get_project(projectID,fulcrumApp):
  logger = logging.getLogger("bibou")
  try:
    project = fulcrumApp.projects.find(projectID)
    increase_num_of_request_by(1)
    return project
  
  except NotFoundException, RateLimitExceededException:
    s = 'Search projects has failed for project '+projectID
    if NotFoundException:
      logger.warning('{} {}'.format(s,notFoundStr))
      pass
    elif RateLimitExceededException:
      logger.error('{} {}'.format(s,limitExceededStr))
      sys.exit(1)

def get_project_file_name(bName,projectName):
  return bName+'/'+projectName+'.json'
  


##############################################
# Other functions
##############################################
def file_is_here(fname):
  if os.path.isfile(fname):
    return True
  else:
    return False

def get_file_basename(formName):
  return fulcrumPath+formName

# print json object in a file according to a mode
def save_file(fileName,data):
  try:
      to_unicode = unicode
  except NameError:
      to_unicode = str

  #with io.open(fileName, mode, encoding='utf8') as outfile2:
  with io.open(fileName, 'w') as outfile:
    str_ = json.dumps(data,
                      indent=2, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
    outfile.write(to_unicode(str_))

# change space to underscore
def clean_name(s):
  s = space_to_underscore(s)
  s = colon_to_underscore(s)
  return s
def space_to_underscore(s):
  return s.replace(' ','_')
def colon_to_underscore(s):
  return s.replace(':','_')

def get_script_directory():
  p = os.path.abspath(__file__)
  return os.path.dirname(p)


##############################################
# Request
##############################################
def increase_num_of_request_by(n):
  if not n:
    n = 1
  global numberOfRequest
  numberOfRequest += n
  
def print_num_of_request():
  logger = logging.getLogger("bibou")
  logger.info('the number of request is {}'.format(numberOfRequest))


##############################################
# MAIN
##############################################
if __name__ == '__main__': 
  main ()


