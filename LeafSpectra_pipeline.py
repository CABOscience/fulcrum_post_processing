#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
import projects as PR
import parameters as PA
import records as RE
import tools as TO
import tools_plots as PL
import logs as LO
import sys
import LeafSpectra_concat_files as LSCF
import LeafSpectra_record as LSR
import SpectroscopyPanels_calibrations as SPC

'''
# Use config parser to set parameters it will allow to simplify the loading and be able to set default values
$ sudo apt install python-configparser
import configparser
config = configparser.RawConfigParser()
config.read('example.cfg')

$ sudo apt-get install python-matplotlib

# Use SpecDAL
$ sudo apt-get install python-pandas
$ sudo apt-get install python-scipy
$ sudo apt-get install python-setuptools
$ git clone  -b caboscience  https://github.com/CABOscience/SpecDAL.git
$ cd SpecDAL
$ sudo python setup.py install

$ git clone  -b caboscience  https://github.com/CABOscience/SpecDAL.git ; cd ./SpecDAL/ ; sudo python setup.py install

To resume:
$ sudo apt install python-configparser python-pandas python-scipy python-setuptools python-matplotlib && cd ~/ && git clone  -b caboscience  https://github.com/CABOscience/SpecDAL.git && cd ./SpecDAL/ && sudo python setup.py install

'''

##############################################
#
# MAIN FUNCTION
#
##############################################
def main():
  PA.set_parameters()
  recordType= PA.LeafSpectraLogFile+"_from_form_file"
  LO.create_log("main","",recordType)
  projects = PR.load_projects()
  
  PR.create_project_website_view_directories(projects)
  
  LO.l_info('Start load records from leafspectra')
  calibrations  = SPC.extract_SpectroscopyPanels_calibrations()
  
  # Extract records
  records = []
  if PA.FormsProcess:
    LO.l_info('Start load records from leafspectra')
    records = LSR.load_leafspectra_Records(calibrations)
    LO.l_info('End load records from leafspectra')
  else:
    LO.l_info('Start load records from webhook')
    records = LSR.load_leafspectra_webhook_Records(calibrations)
    LO.l_info('End load records from webhook')
  LSR.process_leafspectra_records(records)
  LO.l_info('Concat Files')
  LSCF.concat_files()

##############################################
# MAIN
##############################################
if __name__ == '__main__': 
  main ()


