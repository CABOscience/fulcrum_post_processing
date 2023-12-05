#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
import parameters as PA
import records as RE
import projects as PR
import tools as TO
import logs as LO

# System
import os, sys
import multiprocessing as mp
# files
import zipfile
import fnmatch
# Spectroscopy
#import specdal
# Data Science
import pandas as pd

##############################################
# CONCAT FILES in directories and projects
##############################################

def concat_files(recs= RE.Records() , projects=PR.Projects()):
  allCSV      = []
  leavesCSV   = []
  refCSV      = []
  sigfiles    = []
  sigTxtFiles = []
  for root, dirnames, filenames in os.walk(PA.ProjectWebsitePath, followlinks=True):
    for filename in fnmatch.filter(filenames, 'all.csv'):
      if projectinroot(root,projects):
        allCSV.append(os.path.join(root, filename))
    for filename in fnmatch.filter(filenames, 'leaves.csv'):
      if projectinroot(root,projects):
        leavesCSV.append(os.path.join(root, filename))
    for filename in fnmatch.filter(filenames, 'ref.csv'):
      if projectinroot(root,projects):
        refCSV.append(os.path.join(root, filename))
    for filename in fnmatch.filter(filenames, '*.sig'):
      if projectinroot(root,projects):
        sigfiles.append(os.path.join(root, filename))
    for filename in fnmatch.filter(filenames, '*.txt'):
      if 'interpolated_files' in root and projectinroot(root,projects):
        sigTxtFiles.append(os.path.join(root, filename))
  
  LO.l_info('\nNumber of allCSV before {}\n\n'.format(len(allCSV)))
  # Add filter by records:
  # Concat only if the record has a status > than verified
  for recID in list(recs.recordsDict.keys()):
    recStatus = recs.recordsDict[recID].status
    recWf = recs.recordsDict[recID].fv_working_folder
    v = TO.get_record_status_value(recStatus)
    if v < 4:
      recs.recordsDict[recID].add_toLog('The current record status is no submitted or higher. It will not be used in files concatenation. For more information contact Etienne.')
      for acsv in allCSV[:]:
        if recWf in acsv:
          allCSV.remove(acsv)
      for lcsv in leavesCSV[:]:
        if recWf in lcsv:
          leavesCSV.remove(lcsv)
      for rcsv in refCSV[:]:
        if recWf in rcsv:
          refCSV.remove(rcsv)

  LO.l_info('\nNumber of allCSV after {}\n\n'.format(len(allCSV)))
  for al in allCSV[:]:
    LO.l_info('{}'.format(al))
  LO.l_info('\n\n')
  c_list = []
  c_list.append([allCSV,3,'project_all_combined'])
  c_list.append([allCSV,2,'all_combined'])
  c_list.append([leavesCSV,3,'project_leaves_combined'])
  c_list.append([leavesCSV,2,'leaves_combined'])
  c_list.append([refCSV,3,'project_ref_combined'])
  c_list.append([refCSV,2,'ref_combined'])
  b = create_files(c_list)
  z_list = []
  z_list.append([sigfiles,1,'sigfiles'])
  z_list.append([sigTxtFiles,1,'interpolated_files'])
  b = create_zip(z_list)
  
# Test if the root contains a projects name
def projectinroot(root,projects=[]):
  b = False
  for projectName in list(projects.nameId.keys()):
    if projectName in root and PA.ProjectWebsitePath in root:
      b = True
      pass
  return b

# Concat files functions
##############################################

def create_files(c_list):
  wraps = []
  if PA.IsParallel == 'True':
    LO.l_debug("create_files parallelisation")
    output = mp.Queue()
    pool = mp.Pool(processes=PA.NumberOfProcesses)
    results = [pool.apply_async(create_files_from_l, args=(l,)) for l in c_list[:]]
    pool.close()
    pool.join()
    for r in results:
      record = r.get()
      if record:
        wraps.append(record)
  else:
    LO.l_debug("create_files linear")
    for l in c_list[:]:
      record = create_files_from_l(l)
      if record:
        wraps.append(record)
  return wraps

def create_files_from_l(l):
  dic = TO.get_directories(l[1],l[0])
  for k in list(dic.keys()):
    combined_csv = pd.concat( [ pd.read_csv(f) for f in dic[k] ] )
    combined_csv.to_csv( k+"/"+l[2]+".csv", index=False )
  return True

# Zip files functions
##############################################

def create_zip(z_list):
  wraps = []
  if PA.IsParallel == 'True':
    LO.l_debug("create_zip parallelisation")
    output = mp.Queue()
    pool = mp.Pool(processes=PA.NumberOfProcesses)
    results = [pool.apply_async(create_zip_from_l, args=(l,)) for l in z_list[:]]
    pool.close()
    pool.join()
    for r in results:
      record = r.get()
      if record:
        wraps.append(record)
  else:
    LO.l_debug("create_zip linear")
    for l in z_list[:]:
      record = create_zip_from_l(l)
      if record:
        wraps.append(record)
  return wraps

def create_zip_from_l(l):
  dic = TO.get_directories(l[1],l[0])
  for k in list(dic.keys()): 
    zipf = zipfile.ZipFile(k+'/'+l[2]+'.zip', 'w', zipfile.ZIP_DEFLATED)
    for f in dic[k]:
      zipf.write(f)
    zipf.close()
  return True
