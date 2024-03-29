#!/usr/bin/env python
# -*- coding: utf-8 -*-
import parameters as PA
import logs as LO
# System
import io, os, sys
from datetime import datetime 
import time
# files
import csv, codecs, io, json
# Spectroscopy
import specdal
# Math
import re
# Data Science
import pandas as pd
import numpy as np
np.set_printoptions(threshold=sys.maxsize)

'''
# Use SpecDAL
$ sudo apt-get install python-pandas
$ sudo apt-get install python-scipy
$ sudo apt-get install python-setuptools
$ git clone  -b caboscience  https://github.com/CABOscience/SpecDAL.git
$ cd SpecDAL
$ sudo python setup.py install

$ git clone  -b caboscience  https://github.com/CABOscience/SpecDAL.git ; cd ./SpecDAL/ ; sudo python setup.py install
'''

##############################################
# Tools functions
##############################################

# get the FulcrumPath+formName of a FulcrumPath parameter
def get_fulcrum_path_and_basename(st):
  return PA.FulcrumPath+st
def get_FormsFile():
  create_directory(PA.FulcrumPath)
  return get_fulcrum_path_and_basename("all_forms.json")
def get_FormsPath():
  fpath = get_fulcrum_path_and_basename("forms/")
  create_directory(fpath)
  return fpath
def get_WebhookFormsPath():
  #create_directory(PA.FulcrumWebhook+"forms/")
  return PA.FulcrumWebhook+"forms/"
def get_WebhookRecordsPath():
  return PA.FulcrumWebhook+"records/"


# try to delete a file
def delete_a_file(fname,logName="main"):
  if os.path.isfile(fname):
    try:
      os.remove(fname)
      return True
    except Exception as e:
      LO.l_err(e,logName)
  return False

# Test if a file is available and not empty
def file_is_here(fname,logName="main"):
  ''' Test if a file is available and not empty
  
  :param arg1: a string for the filename (with its path)
  :type arg1: string

  :param arg2: a string for the log the default is the main
  :type arg2: string

  :return: True if the file is present and not empty, False else
  :rtype: boolean
  '''
  if os.path.isfile(fname):
    with open(fname, 'r', errors='ignore') as myfile:
      lines = myfile.readlines()
    num_lines = len(lines)
    if num_lines > 1:
      #LO.l_info("\tThe file {} is here".format(fname))
      return True
    else:
      #LO.l_war("\tThe file {} does not have lines available".format(fname))
      return False
  else:
    #LO.l_err("\tThe file {} is not here".format(fname))
    return False

# create a directory if it does not exist
def create_directory(d,logName="main"):
  ''' This function is trying to create a directory if iot does not exist
  
  :param arg1: a string for the directory
  :type arg1: string

  :param arg2: a string for the log the default is the main
  :type arg2: string

  :return: True if it's create or if it already exist, False else
  :rtype: boolean
  '''
  if not os.path.exists(d):
    try:
      os.makedirs(d)
      return True
    except Exception as e:
      LO.l_err(e,logName)
      return False
  else:
    return True

# print json object
def print_as_json(var):
  ''' This function print something in json format
  see: https://docs.python.org/2/library/json.html
  
  :param arg1: something (string, list, dictionnary)
  :type arg1: something
  '''
  print(json.dumps(var, indent=4, sort_keys=True))

# save json object in a file according to a mode
def save_in_json_file(fileName,data,logName="main",arg = "w"):
  ''' This function is trying to write a list in a json file with a default argument "write"
  The options : "w" or "a"
  see: https://docs.python.org/2/library/json.html
  
  :param arg1: a string for the file name
  :type arg1: string

  :param arg2: a list that will be written in the file
  :type arg2: list()

  :param arg3: a string for the log the default is the main
  :type arg3: string

  :param arg4: a argument w or a the default is w
  :type arg4: argument

  :return: True if it's written, False else
  :rtype: boolean
  '''
  try:
      to_unicode = str
  except NameError:
      to_unicode = str

  try:
    #with io.open(fileName, mode, encoding='utf8') as outfile:
    with io.open(fileName, arg) as outfile:
      str_ = json.dumps(data,
                        indent=2, sort_keys=True,
                        separators=(',', ': '), ensure_ascii=False)
      outfile.write(to_unicode(str_))
    return True
  except ValueError:
    LO.l_err(ValueError,logName)
    return False

# Print a string in a file
def string_to_file(fname,s,logName="main",arg = "w"):
  ''' This function is trying to write a string in a file with a default argument "write"
  The options : "w" or "a"
  
  :param arg1: a string for the file name
  :type arg1: string

  :param arg2: a string that will be written in the file
  :type arg2: string

  :param arg3: a string for the log the default is the main
  :type arg3: string

  :param arg4: a argument w or a the default is w
  :type arg4: argument

  :return: True if it's written, False else
  :rtype: boolean
  '''
  try:
    text_file = open(fname, arg)
    text_file.write("{}".format(s))
    text_file.close()
    return True
  except ValueError:
    LO.l_err(ValueError,logName)
    return False

def photo_to_file(fname, photo, logName="main"):
  ''' This function is trying to write a photo in a file
  
  :param arg1: a string for the file name
  :type arg1: string

  :param arg2: the image or photo
  :type arg2: photo

  :param arg3: a string for the log the default is the main
  :type arg3: string

  :return: True if it's written, False else
  :rtype: boolean
  '''
  try:
    with open(fname, 'wb') as f:
      f.write(photo)
    return True
  except ValueError:
    LO.l_err(ValueError,logName)
    return False

def fulcrum_clean_name(s):
  s = s.lower()
  s = space_to_underscore(s)
  pat = re.compile('[^a-z0-9_]+')
  s = pat.sub('_', s)
  pat = re.compile('_{2,}')
  s = pat.sub('_', s)
  return s

# Change string colon or space by underscore
def clean_name(s):
  ''' This function changes space and colon for underscore in a string
  
  :param arg1: a string
  :type arg1: string

  :return: a string with space or colon changed by underscore
  :rtype: string
  '''
  s = space_to_underscore(s)
  s = colon_to_underscore(s)
  s = slash_to_underscore(s)
  return s

# Change \s (' ') to _
def space_to_underscore(s):
  ''' This function changes space for underscore in a string
  
  :param arg1: a string
  :type arg1: string

  :return: a string with space changed by underscore
  :rtype: string
  '''
  return s.replace(' ','_')

# Change : to _
def colon_to_underscore(s):
  ''' This function changes colon for underscore in a string
  
  :param arg1: a string
  :type arg1: string

  :return: a string with colon changed by underscore
  :rtype: string
  '''
  return s.replace(':','_')

# Change / to _
def slash_to_underscore(s):
  ''' This function changes colon for underscore in a string
  
  :param arg1: a string
  :type arg1: string

  :return: a string with slash changed by underscore
  :rtype: string
  '''
  return s.replace('/','_')


# Get the script directory
def get_script_directory():
  ''' This function return a string of the current script directory
  
  :return: a string of the current directory
  :rtype: string
  '''
  p = os.path.abspath(__file__)
  return os.path.dirname(p)

# Load a json file
def load_json_file(fname,logName="main"):
  ''' This function is trying to load a json file
  Deserialize a str or unicode instance containing a JSON document
  see: https://docs.python.org/2/library/json.html
  
  :param arg1: a file path
  :type arg1: string

  :param arg2: a string for the log the default is the main
  :type arg2: string

  :return: a json oject
  :rtype: deserialize json
  '''
  if file_is_here(fname,logName):
    try:
      with open(fname) as f:
        return json.load(f)
    except ValueError:
      LO.l_err(ValueError,logName)
      pass
  return []

# Change timestamp date to string
def from_date_to_s(timestamp):
  ''' This function get a timestamp and return a string
  if the timestamp is bigger than 18: it return "%Y-%m-%dT%H:%M:%S"
  if the timestamp is equal to 10: it return "%Y-%m-%d"
  else it returns a string representing the date and time
  see: https://docs.python.org/2/library/datetime.html#datetime.datetime.strftime
  
  :param arg1: a Timestamp
  :type arg1: timestamp

  :return: a string in three formats
  :rtype: String
  '''
  if '-' in timestamp:
    if len(timestamp)>10:
      return time.strftime("%s", time.strptime(timestamp[:19], "%Y-%m-%dT%H:%M:%S"))
    else:
      return time.strftime("%s", time.strptime(timestamp, "%Y-%m-%d"))
  return timestamp

# Get all files from a path
def get_files_from_path(fpath):
  ''' This function returning a list of path+files from a path
  
  :param arg1: a path
  :type arg1: String

  :return: a list of path+file 
  :rtype: list(String)
  '''
  return [fpath+f for f in os.listdir(fpath) if os.path.isfile(os.path.join(fpath, f))]


# Get all files from a path
def get_files_from_path_recu_with_eof(fpath,eof):
  ''' This function returning a list of path+files from a path with a end of file name pattern
  
  :param arg1: a path
  :type arg1: String

  :param arg2: a pattern for the end of file
  :type arg2: String

  :return: a list of path+file 
  :rtype: list(String)
  '''
  return [os.path.join(dp, f) for dp, dn, filenames in os.walk(fpath) for f in filenames if f.endswith(eof)]
  

# Get all files from a path
def get_files_from_path_recu_with_ext(fpath,ext):
  ''' This function returning a list of path+files from a path with extension file type
  Source: https://stackoverflow.com/a/18394205
  
  :param arg1: a path
  :type arg1: String

  :param arg2: a pattern for the extension
  :type arg2: String

  :return: a list of path+file 
  :rtype: list(String)
  '''
  return [os.path.join(dp, f) for dp, dn, filenames in os.walk(fpath) for f in filenames if os.path.splitext(f)[1] == ext]
  


# Change the status of a record to a value
def get_record_status_value(recordStatus):
  ''' This function is changing the record value to a number
  
  :param arg1: a record
  :type arg1: Record

  :return: A value from -1 status no found then to 0 deleted to 6 for published
  :rtype: int
  '''
  records_status_list = ['deleted', 'pending', 'rejected', 'verified', 'submitted', 'approved', 'published']
  for record_status in records_status_list[:]:
    if recordStatus == record_status:
      return records_status_list.index(record_status)
  return -1

# Bottom-Up recursion for a list files to extract directories
def get_directories(n,files):
  ''' This function is to get directories dictionnary fo files from a list of that files at X level
  
  :param arg1: a level of recursivity
  :type arg1: int

  :param arg2: a list of files
  :type arg2: list()

  :return: a list for directories at a level of arg1
  :rtype: dictionnary(directory) = list(files)
  '''
  d = {}
  for f in files:
    if file_is_here(f):
      directory = get_parent_n_times(n,f)
      if directory in d:
        d[directory].append(f)
      else:
        d[directory] = [f]
  return d

# Get the parent directory of a path or a file n times
def get_parent_n_times(n,f):
  ''' This function is part of the recusivity function
  It repeats the get_parent n times:
  Exemple:
  /hello/world/this/is/my/file.txt at level 3 returns /hello/world
  
  :param arg1: a first level of recursivity
  :type arg1: int

  :param arg2: a file
  :type arg2: a file path

  :return: a list for directories at a level of arg1
  :rtype: list()
  '''
  p = f
  for x in range(0, n):
    p = get_parent(p)
  return p
  
# Get the upper directory of a path or a file
def get_parent(f):
  ''' This function return the parent directory of a file or a path
  Exemple:
  /hello/world/this/is/my/file.txt returns /hello/world/this/is/my/
  
  :param arg1: a path or a file
  :type arg1: string

  :return: a string of the parent directory
  :rtype: string
  '''
  return os.path.abspath(os.path.join(f, os.pardir))


# String to float (decimal)
def s2d(v,logName="main"):
  ''' This function returns a float from a string
  Exemple: 3,2 return 3.2
  
  :param arg1: a string value with a comma
  :type arg1: string

  :param arg2: a string for the log the default is the main
  :type arg2: string

  :return: a string value with a dot
  :rtype: float
  '''
  try:
    return float(v.replace(',','.'))
  except ValueError:
    LO.l_err(ValueError,logName)
    return v

# Extract a multiple choice fulcrum in a simple string
def get_fulcrum_multiple_choice_in_string(my_list):
  """ This will extract all user from a list with 
  
  :param arg1: A fulcrum mutiple choice
  :type arg1: list[]

  :return: A string with all user measured by
  :rtype: string
  """
  st = ""
  if len(my_list["choice_values"])==1:
    st += my_list["choice_values"][0]
  elif len(my_list["choice_values"])>1:
    st += ', '.join(x for x in my_list["choice_values"])
  if len(my_list["other_values"])==1:
    st += my_list["other_values"][0]
  elif len(my_list["other_values"])>1:
    st += ', '.join(x for x in my_list["other_values"])
  return st

# Write a list in a csv file
def write_in_csv(fname,my_list,logName="main",arg = "w"):
  ''' This function is trying to write a list in a json file with a default argument "write"
  The options : "w" or "a"
  see: https://docs.python.org/2/library/json.html
  
  :param arg1: a string for the file name
  :type arg1: string

  :param arg2: a list that will be written in the file
  :type arg2: list()

  :param arg3: a string for the log the default is the main
  :type arg3: string

  :param arg4: a argument w or a the default is w
  :type arg4: argument

  :return: True if it's written, False else
  :rtype: boolean
  '''
  try:
    with open(fname, mode=arg, encoding="utf-8") as csv_file:
      p = csv.writer(csv_file)
      p.writerows(my_list)
    return True
  except ValueError:
    LO.l_err(ValueError,logName)
    return False

# From a panda serie to a panda dataframe
def from_series_to_dataframe(se):
  ''' This function transforms a panda serie in a panda dataframe
  see: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame
  
  :param arg1: a panda series
  :type arg1: series

  :return: panda dataframe
  :rtype: dataframe
  '''
  df = pd.DataFrame()
  if se.values.size>0:
    iname = ""
    sname = ""
    if hasattr(se,'name'):
      sname = se.name
    else:
      sname = "value"

    if hasattr(se, 'index') and hasattr(se.index, 'name'):
      iname = se.index.name
    else:
      iname = "index"
    LO.l_debug("index\n\n{}".format(se.index))
    LO.l_debug("values\n\n{}".format(se.values))
    df = pd.DataFrame(data={iname:se.index,sname:se.values})
    df = df [[iname,sname]]
  return df

# From a panda dataframe to a panda serie
def from_dataframe_to_series(df):
  ''' This function transforms a panda dataframe in a panda serie or nothing if the dataframe does not have exactly two columns
  see: https://pandas.pydata.org/pandas-docs/stable/reference/series.html
  
  :param arg1: a panda dataframe with only two columns
  :type arg1: dataframe

  :return: panda series or nothing
  :rtype: series or nothing
  '''
  l = list(df)
  if len(l)==2:
    index = df[df.columns[0]]
    values = df[df.columns[1]]
    se = pd.Series(values, index=index, name=l[1])
    se.index.name = l[0]
    return se
  else:
    return None
  
# Return monotonic series from specdal

def get_monotonic_series(series):
  '''
  # Operator.py defines operations on pd.Series that consists of
  # wavelength as index and measurement as values
  see: https://github.com/CABOscience/SpecDAL/blob/caboscience/specdal/operators/interpolate.py
  
  return specdal.get_monotonic_series(series)
  return a list of series with monotonic index
  
  TODO: test what happens if not strictly monotonic
  i.e. index: 1, 2, 3, 3
  '''
  if series.index.is_monotonic:
      return [series]
  else:
      index = pd.Series(series.index)
      head_positions = index[index.diff() < 0].index

      N = head_positions.size

      result = [series.iloc[:head_positions[0]]]
      result += [series.iloc[head_positions[i]:head_positions[i+1]] for i in range(0, N-1)]
      result += [series.iloc[head_positions[N-1]:]]
      return result

def create_spectrum(fName,measureType):
  return specdal.Spectrum(filepath=fName, measure_type= measureType)

def create_empty_spectrum():
  return specdal.Spectrum(name='empty')

# time 
def print_time(start_time,time_previous_task,task_type,logName="main"):
  time_now = datetime.now()
  time_elapsed = time_now - start_time
  st = '{} Time elapsed since started (hh:mm:ss.ms) {}'.format(task_type,time_elapsed)
  LO.l_debug(st,logName)
  if time_previous_task != start_time:
    time_temp = time_now - time_previous_task
    stt = '{} Time elapsed since previous task (hh:mm:ss.ms) {}'.format(task_type,time_temp)
    LO.l_debug(stt,logName)
  return time_now
