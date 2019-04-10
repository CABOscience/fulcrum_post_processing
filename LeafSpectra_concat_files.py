#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
from parameters import ProjectWebsitePath
import tools as TO
import logs

# System
import os
# files
import zipfile
import fnmatch
# Spectroscopy
import specdal
# Data Science
import pandas as pd

##############################################
# CONCAT FILES in directories and projects
##############################################

def concat_files():
  allCSV      = []
  leavesCSV   = []
  refCSV      = []
  sigfiles    = []
  sigTxtFiles = []
  for root, dirnames, filenames in os.walk(ProjectWebsitePath, followlinks=True):
    for filename in fnmatch.filter(filenames, 'all.csv'):
      allCSV.append(os.path.join(root, filename))
    for filename in fnmatch.filter(filenames, 'leaves.csv'):
      leavesCSV.append(os.path.join(root, filename))
    for filename in fnmatch.filter(filenames, 'ref.csv'):
      refCSV.append(os.path.join(root, filename))
    for filename in fnmatch.filter(filenames, '*.sig'):
      sigfiles.append(os.path.join(root, filename))
    for filename in fnmatch.filter(filenames, '*.txt'):
      if 'interpolated_files' in root:
        sigTxtFiles.append(os.path.join(root, filename))
  c_list = ()
  c_list.append([allCSV,3,'project_all_combined'])
  c_list.append([allCSV,2,'all_combined'])
  c_list.append([leavesCSV,3,'project_leaves_combined'])
  c_list.append([leavesCSV,2,'project_leaves_combined'])
  c_list.append([refCSV,3,'project_ref_combined'])
  c_list.append([refCSV,2,'ref_combined'])
  create_files(c_list)
  z_list = ()
  z_list.append([sigfiles,1,'sigfiles'])
  z_list.append([sigfiles,1,'interpolated_files'])
  create_zip(z_list)
  
  
# Concat files functions
##############################################

def create_files(c_list):
  for l in c_list[:]:
    dic = TO.get_directories(l[1],l[0])
    for k in dic.keys():
      combined_csv = pd.concat( [ pd.read_csv(f) for f in l[0][k] ] )
      combined_csv.to_csv( k+"/"+l[2]+".csv", index=False )

# Zip files functions
##############################################

def create_zip(z_list):
  for l in z_list[:]:
    dic = TO.get_directories(l[1],l[0])
    for k in dic.keys():
      zipf = zipfile.ZipFile(k+'/'+l[2]+'.zip', 'w', zipfile.ZIP_DEFLATED)
      for f in dic[k]:
        zipf.write(f)
      zipf.close()

'''
  create_for_all_projects(allCSV)
  create_for_all_working_directories(allCSV)
  create_for_leaves_projects(leavesCSV)
  create_for_leaves_working_directories(leavesCSV)
  create_for_references_projects(refCSV)
  create_for_references_working_directories(refCSV)
  create_sig_raw_zip_working_directories(sigfiles)
  create_sig_raw_zip_working_directories(sigTxtFiles)

# All
## project level
def create_for_all_projects(allCSV):
  allCSVP = TO.get_directories(3,allCSV)
  for k in allCSVP.keys():
    combined_csv = pd.concat( [ pd.read_csv(f) for f in allCSVP[k] ] )
    combined_csv.to_csv( k+"/project_all_combined.csv", index=False )
## working directory level
def create_for_all_working_directories(allCSV):
  allCSVWF = TO.get_directories(2,allCSV)
  for k in allCSVWF.keys():
    combined_csv = pd.concat( [ pd.read_csv(f) for f in allCSVWF[k] ] )
    combined_csv.to_csv( k+"/all_combined.csv", index=False )
# Leaves
## project level
def create_for_leaves_projects(leavesCSV):
  leavesCSVWF = TO.get_directories(3,leavesCSV)
  for k in leavesCSVWF.keys():
    combined_csv = pd.concat( [ pd.read_csv(f) for f in leavesCSVWF[k] ] )
    combined_csv.to_csv( k+"/project_leaves_combined.csv", index=False )
## working directory level
def create_for_leaves_working_directories(leavesCSV):
  leavesCSVWF = TO.get_directories(2,leavesCSV)
  for k in leavesCSVWF.keys():
    combined_csv = pd.concat( [ pd.read_csv(f) for f in leavesCSVWF[k] ] )
    combined_csv.to_csv( k+"/leaves_combined.csv", index=False )
# Ref
## project level
def create_for_references_projects(refCSV):
  refCSVP = TO.get_directories(3,refCSV)
  for k in refCSVP.keys():
    combined_csv = pd.concat( [ pd.read_csv(f) for f in refCSVP[k] ] )
    combined_csv.to_csv( k+"/project_ref_combined.csv", index=False )
## working directory level
def create_for_references_working_directories(refCSV):
  refCSVP = TO.get_directories(2,refCSV)
  for k in refCSVP.keys():
    combined_csv = pd.concat( [ pd.read_csv(f) for f in refCSVP[k] ] )
    combined_csv.to_csv( k+"/ref_combined.csv", index=False )

# raw sig files
## working directory level
def create_sig_raw_zip_working_directories(sigfiles):
  sigFilesWF = TO.get_directories(1,sigfiles)
  for k in sigFilesWF.keys():
    zipf = zipfile.ZipFile(k+'/sigfiles.zip', 'w', zipfile.ZIP_DEFLATED)
    for f in sigFilesWF[k]:
      zipf.write(f)
    zipf.close()
# interpolated sig files
## working directory level
def create_sig_raw_zip_working_directories(sigTxtFiles):
  sigTxtFilesWF = TO.get_directories(2,sigTxtFiles)
  for k in sigTxtFilesWF.keys():
    zipf = zipfile.ZipFile(k+'/interpolated_files.zip', 'w', zipfile.ZIP_DEFLATED)
    for f in sigTxtFilesWF[k]:
      zipf.write(f)
    zipf.close()
'''
