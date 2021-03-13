#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
from . import projects as PR
from . import parameters as PA
from . import Sites_record as SIR
from . import forms as FO
from . import tools as TO
from . import logs as LO

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
  LO.create_log(recordType)
  sites = SIR.load_sites()
  print(len(sites))
  
  site = SIR.get_site_with_site_id('hello-world')
  print(site)

  site = SIR.get_site_with_site_id('da900226-f394-492f-89a5-a15890315d1b')
  print(site)

##############################################
# MAIN
##############################################
if __name__ == '__main__': 
  main ()

