#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
import projects as PR
import parameters as PA
import Sites_record as SIR
import forms as FO
import tools as TO
import logs as LO

# Spectroscopy
import specdal
# System
import sys

##############################################
#
# MAIN FUNCTION
#
##############################################
def main():
  PA.set_parameters()
  recordType= PA.SitesLogFile+"_sites_test"
  LO.create_log("main","",recordType)
  sites = SIR.load_sites()
  print len(sites)
  
  site = SIR.get_site_with_site_id('hello-world')
  print site

  site = SIR.get_site_with_site_id('da900226-f394-492f-89a5-a15890315d1b')
  print site

##############################################
# MAIN
##############################################
if __name__ == '__main__': 
  main ()

