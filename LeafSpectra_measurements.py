#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tools as TO
# Spectroscopy
#import specdal
# Data Science
import pandas as pd


##############################################
# SPECTRUM
##############################################

# SpectraMeasurements
#########################

class SpectraMeasurements(object):
  def __init__(self, bn='', fn='',  fnv='',  mi='',  mr='',  ln='',  lp='',  lsm='',  plps='',  rn='',  rps='',  sn='',  scsll='',  scssl='',  tt='', tps=''):
    self.branch_number = bn
    self.file_name = fn
    self.file_name_value = fnv
    self.file_path = ""
    self.measurement_id = mi
    self.measurement_remarks = mr
    self.leaf_number = ln
    self.leaf_side_measured = lsm
    self.leaf_photos = lp
    self.primary_light_port_svc = plps
    self.reflectance = pd.DataFrame()
    self.reflectance_port_svc = rps
    self.replicate_number = rn
    self.spectrum_number = sn
    self.sphere_configuration_svc_large_leaves = scsll
    self.sphere_configuration_svc_small_leaves = scssl
    self.target_type = tt
    self.transmission_port_svc = tps
    self.transmittance = pd.DataFrame()
    self.spectre = TO.create_empty_spectrum()
  
  def __str__(self):
    return '>{} - {}'.format(self.file_name, self.file_path)

  def to_csv(self):
    sc = ''
    if len(self.sphere_configuration_svc_large_leaves)>0:
      sc = self.sphere_configuration_svc_large_leaves
    else: 
      sc = self.sphere_configuration_svc_small_leaves
    port = ''
    if len(self.reflectance_port_svc)>0:
      port = self.reflectance_port_svc
    else :
      port = self.transmission_port_svc
    return [self.file_name, self.file_path,self.leaf_number,self.leaf_side_measured,self.spectrum_number,sc,port]

  def to_csv_leaf(self):
    return [self.file_name,self.leaf_number,self.leaf_side_measured]

  def to_csv_reference(self):
    return [self.leaf_number,self.leaf_side_measured]

  def to_csv_all(self):
    return [self.leaf_side_measured]

def extract_leaf_spectra_measurements(measurements):
  """ This will extract measurements of a leaf spectra record
  
  :param arg1: a fulcrum measurements list
  :type arg1: list()

  :return: A list of SpectraMeasurements
  :rtype: list(SpectraMeasurements)
  """
  measurementsInfo = []
  for measurement in measurements:
    cv = 'choice_values'
    bn, fn, fnv, mi, mr, ln, lp, lsm, plps, rn, rps, sn, scsll, scssl, tt, tps= ("",)*16
    vs  = measurement['form_values']
    fn  = vs['file_name']
    if 'branch_number'          in vs: bn = vs['branch_number']
    if 'file_name_value'        in vs: fnv = vs['file_name_value'] 
    if 'measurement_remarks'    in vs: mr = vs['measurement_remarks']
    if 'measurement_id'         in vs: mi = vs['measurement_id']
    if 'leaf_photos'            in vs: lp = vs['leaf_photos']
    if 'leaf_number'            in vs: ln = vs['leaf_number']
    if 'leaf_side_measured'     in vs: lsm = vs['leaf_side_measured']  
    if 'primary_light_port_svc' in vs: plps = vs['primary_light_port_svc']
    if 'replicate_number'       in vs: rn = vs['replicate_number']
    if 'reflectance_port_svc'   in vs: rps = vs['reflectance_port_svc'][cv][0] 
    if 'sphere_configuration_svc_large_leaves' in vs: scsll = vs['sphere_configuration_svc_large_leaves'][cv][0]  # test if 'sphere_configuration_svc_large_leaves' here
    if 'sphere_configuration_svc_small_leaves' in vs: scssl = vs['sphere_configuration_svc_small_leaves'][cv][0]  # test if 'sphere_configuration_svc_small_leaves' here
    if 'spectrum_number'        in vs: sn  = vs['spectrum_number']      
    if 'target_type'            in vs: tt = vs['target_type']
    if 'transmission_port_svc'  in vs: tps = vs['transmission_port_svc'][cv][0]
    measurementsInfo.append(SpectraMeasurements(bn, fn, fnv, mi, mr, ln, lp, lsm, plps, rn, rps, sn, scsll, scssl, tt, tps))
  return measurementsInfo

