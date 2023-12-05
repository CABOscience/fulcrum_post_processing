#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
import logs as LO
import tools as TO

# Plot
import os, time
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib.image as mpimg

'''
# How ton install matplotlib
$ sudo apt-get install python-matplotlib

from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import gridspec
'''

##############################################
# Plots
    # save as csv
    # draw plots
##############################################

def get_leafspectra_record_leaves_plot(record):
  pm = record.fv_properties_measured
  pmR = False
  if 'both' in pm or 'reflectance' in pm:
    pmR = True

  xmin = record.get_wavelength_min()
  xmax = record.get_wavelength_max()

  reflecLeaves = record.fv_reflecLeaves
  transLeaves = record.fv_transLeaves
  imgdir = record.fv_processedPath+'/leaves'
  TO.create_directory(imgdir)
  leavesVal = list(reflecLeaves.keys())
  if len(leavesVal)<1:
    leavesVal = list(transLeaves.keys())
  if len(leavesVal)>0:
    for leafNum in leavesVal:
      imgPath = imgdir+'/'+record.fv_sample_id+'_leaf_'+leafNum+'.png'
      reflectance = pd.DataFrame()
      transmittance = pd.DataFrame()
      if leafNum in reflecLeaves:
        if reflecLeaves[leafNum].reflectance.values.size>0: 
          reflectance = TO.from_series_to_dataframe(reflecLeaves[leafNum].reflectance)
          reflectance = reflectance.rename(columns={"tgt_counts": "reflectance"})
          reflectance = reflectance.set_index('wavelength')
      if leafNum in transLeaves:
        if transLeaves[leafNum].transmittance.size>0:
          transmittance = TO.from_series_to_dataframe(transLeaves[leafNum].transmittance)
          transmittance = transmittance.rename(columns={"tgt_counts": "transmittance"})
          transmittance = transmittance.set_index('wavelength')
      title = record.fv_sample_id+' leaf num: '+leafNum
      try:
        img_reflect_and_transmi(xmin,xmax,reflectance,transmittance,imgPath,title)
      except Exception as e:
        LO.l_debug('get_leafspectra_record_leaves_plot Failed to generate plot for image {} with exception:\n{}'.format(imgPath,e))
        record.add_toLog('get_leafspectra_record_leaves_plot Failed to generate plot for image {} with exception:\n{}'.format(imgPath,e))
        pass
 
    imgFiles = TO.get_files_from_path(imgdir+'/')
    if len(imgFiles)>0:
      f, axarr = plt.subplots(3, 2, figsize=(10,10))
      f.suptitle(record.fv_sample_id+' leaves')
      y=0
      x=0
      for imgFile in sorted(imgFiles):
        img = mpimg.imread(imgFile)
        axarr[x,y].imshow(img, interpolation='none')
        #head, tail = os.path.split(imgFile)
        #axarr.set_title(fv_sample_id+' leaves')
        axarr[x,y].axis('off')
        if y == 1:
          x += 1
          y = 0
        else:
          y +=1
      plt.savefig(record.fv_processedPath+'/'+record.fv_sample_id+'_leaves.png', dpi=150)
      #time.sleep(5)
      plt.close('all')
      return True
  return False
  
def print_entire_data_frame(df):
  with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df)
  pd.reset_option('display.max_rows')
  pd.reset_option('display.max_columns')

def get_leafspectra_record_plot(record):
  #if '23a4dc4c-d41e-49f9-bdf4-3f1d737f9549' == record.id:
    reflecAverage = record.fv_reflecAverage
    reflecDiffRef = record.fv_reflecDiffRef
    reflecRef     = record.fv_reflecRef
    reflecStadDev = record.fv_reflecStadDev
    transAverage  = record.fv_transAverage
    transDiffRef  = record.fv_transDiffRef
    transStadDev  = record.fv_transStadDev
    imgpath = record.fv_processedPath+'/'+record.fv_sample_id+'.png'
    xmin = record.get_wavelength_min()
    xmax = record.get_wavelength_max()
    title = record.fv_sample_id+' average'
    try:
      img_reflect_and_transmi(xmin,xmax,reflecAverage,transAverage,imgpath,title)
    except Exception as e:
      record.add_toLog('get_panel_calibrations_record_plot Failed to generate plot for image {} with exception:\n{}'.format(imgpath,e))
      LO.l_debug('get_panel_calibrations_record_plot Failed to generate plot for image {} with exception:\n{}'.format(imgpath,e))
      pass

def img_reflect_and_transmi(xmin , xmax, reflec =pd.DataFrame(),transmi =pd.DataFrame(), imgpath ="", title=''):
  indexV = []
  transmiV = []
  reflecV = []
  if not reflec.empty:
    indexV = reflec.index.values.tolist()
    reflecV = reflec.values.tolist()
  if not transmi.empty:
    transmiV = transmi.values.tolist()
    if len(indexV)<1:
      indexV = transmi.index.values.tolist()
  fig = plt.figure()
  if len(reflecV)>0:
    ax1 = fig.add_subplot(111)
    ax1.plot(indexV, reflecV, color='#998ec3')
    ax1.set_ylabel('reflectance', color='#998ec3')
    ax1.set_xlabel('wavelength (nm)')
    ax1.set_title(title)
    for tl in ax1.get_yticklabels():
      tl.set_color('#998ec3')
    ax1.set_ylim(-0.1, 1.1)
    loc = plticker.MultipleLocator(base=250) # this locator puts ticks at regular intervals
    ax1.xaxis.set_major_locator(loc)
    ax1.set_xlim(xmin,xmax)
    
    if len(transmiV)>0:
      ax2 = ax1.twinx()
      ax2.plot(indexV, transmiV, 'r-', color='#f1a340')
      ax2.set_ylim(1.1, -0.1)
      ax2.set_xlim(xmin,xmax)
      ax2.set_ylabel('transmittance', color='#f1a340')
      for tl in ax2.get_yticklabels():
        tl.set_color('#f1a340')
  else:
    if len(transmiV)>0:
      ax1 = fig.add_subplot(111)
      ax1.plot(indexV, reflecV, color='#f1a340')
      ax1.set_ylabel('transmittance', color='#f1a340')
      ax1.set_xlabel('wavelength (nm)')
      ax1.set_title(title)
      for tl in ax1.get_yticklabels():
        tl.set_color('#f1a340')
      ax1.set_ylim(-0.1, 1.1)
      loc = plticker.MultipleLocator(base=250) # this locator puts ticks at regular intervals
      ax1.xaxis.set_major_locator(loc)
      ax1.set_xlim(xmin,xmax)
  if (len(transmiV)>0 or len(reflecV)>0) and imgpath != "":
    plt.savefig(imgpath, dpi=150)
    #time.sleep(5)
  plt.close('all')

################################################
# Panel Calibrations
################################################

def get_panel_calibrations_record_plot(record):
  #if '23a4dc4c-d41e-49f9-ddbdf4-3f1d737f9549' == record.id:
    reflecAverage = record.fv_reflecAverage
    reflecDiffRef = record.fv_reflecDiffRef
    reflecRef     = record.fv_reflecRef
    reflecStadDev = record.fv_reflecStadDev
    transAverage  = record.fv_transAverage
    transDiffRef  = record.fv_transDiffRef
    transStadDev  = record.fv_transStadDev
    imgpath = record.fv_processedPath+''+record.fv_serial_number+'.png'
    LO.l_info(imgpath)
    xmin = record.wvlMin
    xmax = record.wvlMax
    title = record.fv_parent_directory+' '+record.fv_working_folder+' '+record.fv_serial_number+' average'
    try:
      img_reflect_and_transmi_panel_calibrations(xmin,xmax,reflecAverage,transAverage,imgpath,title)
    except Exception as e:
      record.add_toLog('get_panel_calibrations_record_plot Failed to generate plot for image {} with exception:\n{}'.format(imgpath,e))
      LO.l_debug('get_panel_calibrations_record_plot Failed to generate plot for image {} with exception:\n{}'.format(imgpath,e))
      pass

def img_reflect_and_transmi_panel_calibrations(xmin , xmax, reflec =pd.DataFrame(),transmi =pd.DataFrame(), imgpath ="", title=''):
  indexV = []
  reflecV = []
  if not reflec.empty:
    indexV = reflec.index.values.tolist()
    reflecV = reflec.values.tolist()
  fig = plt.figure()
  if len(reflecV)>0:
    ax1 = fig.add_subplot(111)
    ax1.plot(indexV, reflecV, color='#998ec3')
    ax1.set_ylabel('reflectance', color='#998ec3')
    ax1.set_xlabel('wavelength (nm)')
    ax1.set_title(title)
    for tl in ax1.get_yticklabels():
      tl.set_color('#998ec3')
    ax1.set_ylim(0.95, 1.05)
    loc = plticker.MultipleLocator(base=250) # this locator puts ticks at regular intervals
    ax1.xaxis.set_major_locator(loc)
    ax1.set_xlim(xmin,xmax)

  if (len(reflecV)>0) and imgpath != "":
    plt.savefig(imgpath, dpi=150)
    #time.sleep(5)
    plt.close('all')

def get_panel_calibrations_record_measurments_plot(record):
  xmin = record.wvlMin
  xmax = record.wvlMax

  reflecReplicates  = record.fv_reflecReplicates
  
  imgdir = record.fv_processedPath+'/replicates'
  TO.create_directory(imgdir)
  replicatesVal = list(reflecReplicates.keys())
  if len(replicatesVal)>0:
    for replicateNum in replicatesVal:
      imgPath = imgdir+'/'+record.fv_serial_number+'_replicate_'+replicateNum+'.png'
      reflectance = pd.DataFrame()
      reflectance = reflecReplicates[replicateNum].reflectance
      reflectance = TO.from_series_to_dataframe(reflectance)
      reflectance = reflectance.rename(columns={"tgt_counts": "reflectance"})
      reflectance = reflectance.set_index('wavelength')
      title = record.fv_serial_number+' replicate num: '+replicateNum
      try:
        img_reflect_and_transmi_panel_calibrations(xmin,xmax,reflectance,pd.DataFrame(),imgPath,title)
      except Exception as e:
        record.add_toLog('get_panel_calibrations_record_measurments_plot Failed to generate plot for image {} with exception:\n{}'.format(imgpath,e))
        LO.l_debug('get_panel_calibrations_record_measurments_plot Failed to generate plot for image {} with exception:\n{}'.format(imgpath,e))
        pass

    imgFiles = TO.get_files_from_path(imgdir+'/')
    if len(imgFiles)>0:
      f, axarr = plt.subplots(3, 2, figsize=(10,10))
      f.suptitle(record.fv_serial_number+' replicates')
      y=0
      x=0
      for imgFile in sorted(imgFiles):
        img = mpimg.imread(imgFile)
        axarr[x,y].imshow(img, interpolation='none')
        axarr[x,y].axis('off')
        if y == 1:
          x += 1
          y = 0
        else:
          y +=1
      record.replicate_plot = record.fv_processedPath+'/'+record.fv_serial_number+'_replicates.png'
      plt.savefig(record.replicate_plot, dpi=150)
      plt.close('all')
    else:
      record.isValid = False
  return record

