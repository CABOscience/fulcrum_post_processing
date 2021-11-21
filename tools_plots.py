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

    # a problem here
    #print 'transAverage before {}'.format(transAverage)
    #transAverage = TO.transmittance_minus_1(transAverage)
    #print 'transAverage after {}'.format(transAverage)
    df = pd.concat([reflecAverage, transAverage], axis=1)
    #print df.to_json(orient='split')
    #print_entire_data_frame(df)
    
    #ax = reflecAverage.plot()
    #df2.plot(ax=ax)
    
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.set_ylim(-0.1, 1)
    ax1.set_xlabel('wavelength')
    ax1.set_ylabel('%')
    ax1.set_title('Spectrum for record {}'.format(record.fv_sample_id))
    
    ax2.invert_yaxis()
    ax2.set_ylim(1, -0.1)
    ax2.set_ylabel('%', color='r')
    for tl in ax2.get_yticklabels():
      tl.set_color('r')
    
    ax1 = reflecAverage.plot()
    ax2 = transAverage.plot(y=['transmittance_average'], color='r')
    #df.plot(y=['reflectance_average'], ax= ax1)
    #df.plot(y=['transmittance_average'], ax= ax2)

      fig, ax = plt.subplots(figsize=(10, 10))
      ax.set_ylim(-0.1, 1)
      ax.set_xlabel('wavelength')
      ax.set_ylabel('%')
      ax.set_title('Spectrum for leaf number {}'.format(leafNum))
      df = pd.DataFrame()
      reflectance = reflecLeaves[leafNum].reflectance
      reflectance = TO.from_series_to_dataframe(reflectance)
      reflectance = reflectance.rename(columns={"tgt_counts": "reflectance"})
      reflectance = reflectance.set_index('wavelength')
      transmittance = transLeaves[leafNum].transmittance
      transmittance = TO.from_series_to_dataframe(transmittance)
      transmittance = transmittance.rename(index=str, columns={"tgt_counts": "transmittance"})
      transmittance = transmittance.set_index('wavelength')
      transmittance = TO.transmittance_minus_1(transmittance)
      df = pd.concat([reflectance, transmittance], axis=1)
      img = df.plot(y=['reflectance', 'transmittance'], ax= ax)
      a = figs.add_subplot(2, np.ceil(float(6)/float(2)), i)
      a.set_title('Spectrum for leaf number {}'.format(leafNum))
      plt.imshow(img)
      i += 1
      plt.savefig()

  pdfFile = record.fv_processedPath+'/'+record.fv_sample_id+'_leaves.pdf'
  pdf = PdfPages(pdfFile)
  cnt = 0
  figs = plt.figure()
  #record.fv_reflecLeaves[leafNumber] = measurement
  reflecLeaves = record.fv_reflecLeaves
  transLeaves = record.fv_transLeaves
  for leafNum in reflecLeaves.keys():
    df = pd.concat([reflecLeaves[leafNum], transLeaves[leafNum]], axis=1)
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_ylim(-0.1, 1)
    ax.set_xlabel('wavelength')
    ax.set_ylabel('%')
    ax.set_title('Spectrum for leaf number {}'.format(leafNum))
    df.plot(y=['transmittance', 'reflectance'], ax= ax)

    # change font size
    #plt.rcParams.update({'font.size': 8})
    #plot_num += 1

    pdf.savefig(fig)
  pdf.close()
  
  # Plotting code
  f, ax1 = plt.subplots(1, figsize=(7,7))
  gs  = gridspec.GridSpec(1, 1, height_ratios=[3,1]) 
  ax1 = plt.subplot(gs[0])
  
  ax1.plot(regrid, resampled, color="red", lw=1.5, label="Spectrum for leaf number {}".format(leaf_number))
  ax1.set_ylabel("{}".format(refl_trance), size=10)
  ax1.set_xlabel("Wavelength (nm)", size=10)
  ax1.set_xlim(wvl_min, wvl_max)
  ax1.set_ylim(-0.1, 1)
  ax1.legend()
  
  return plt.figure()
  with PdfPages('foo.pdf') as pdf:
    for i, group in df.groupby('station_id'):
      plt.figure()
      fig=group.plot(x='year', y='Value',title=str(i)).get_figure()
      pdf.savefig(fig)
     
  plot1 = plotGraph(tempDLstats, tempDLlabels)
  plot2 = plotGraph(tempDLstats_1, tempDLlabels_1)
  plot3 = plotGraph(tempDLstats_2, tempDLlabels_2)

  pp = PdfPages('foo.pdf')
  pp.savefig(plot1)
  pp.savefig(plot2)
  pp.savefig(plot3)
  pp.close()


  for imgFile in imgFiles:
  #for i in range(1, columns*rows +1):
      img = mpimg.imread(imgFile)
      fig.add_subplot(rows, columns, i)
      i += 1 
      plt.imshow(img)
      plt.axis('off')
      head, tail = os.path.split(imgFile)
      plt.title(tail)
  imgFiles = TO.get_files_from_path(imgdir)
  imgs = np.empty
  for imgFile in imgFiles:
    imgP = mpimg.imread(imgFile)
    imgs.append(imgP)
  save_images(imgs,3,leavesVal)

def save_images(images =[], cols = 1, titles = []):
    """Display a list of images in a single figure with matplotlib.
    
    Parameters
    ---------
    images: List of np.arrays compatible with plt.imshow.
    
    cols (Default = 1): Number of columns in figure (number of rows is 
                        set to np.ceil(n_images/float(cols))).
    
    titles: List of titles corresponding to each image. Must have
            the same length as titles.
    """
    assert((titles is None)or (len(images) == len(titles)))
    n_images = len(images)
    if titles is None: titles = ['Image (%d)' % i for i in range(1,n_images + 1)]
    fig = plt.figure()
    for n, (image, title) in enumerate(zip(images, titles)):
        a = fig.add_subplot(cols, np.ceil(n_images/float(cols)), n + 1)
        if image.ndim == 2:
            plt.gray()
        plt.imshow(image)
        a.set_title(title)
    fig.set_size_inches(np.array(fig.get_size_inches()) * n_images)
    plt.savefig(record.fv_processedPath+'/'+record.fv_sample_id+'_leaves.png')

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
        reflectance = reflecLeaves[leafNum].reflectance
        reflectance = TO.from_series_to_dataframe(reflectance)
        reflectance = reflectance.rename(columns={"tgt_counts": "reflectance"})
        reflectance = reflectance.set_index('wavelength')
      if leafNum in transLeaves:
        transmittance = transLeaves[leafNum].transmittance
        transmittance = TO.from_series_to_dataframe(transmittance)
        transmittance = transmittance.rename(columns={"tgt_counts": "transmittance"})
        transmittance = transmittance.set_index('wavelength')
      title = record.fv_sample_id+' leaf num: '+leafNum
      img_reflect_and_transmi(xmin,xmax,reflectance,transmittance,imgPath,title)

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
    img_reflect_and_transmi(xmin,xmax,reflecAverage,transAverage,imgpath,title)

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
    #xmin = record.get_wavelength_min()
    #xmax = record.get_wavelength_max()
    xmin = record.wvlMin
    xmax = record.wvlMax
    title = record.fv_parent_directory+' '+record.fv_working_folder+' '+record.fv_serial_number+' average'
    img_reflect_and_transmi_panel_calibrations(xmin,xmax,reflecAverage,transAverage,imgpath,title)

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
      img_reflect_and_transmi_panel_calibrations(xmin,xmax,reflectance,pd.DataFrame(),imgPath,title)

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

