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
import SpectroscopyPanels_record as SPR

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
  recordType= PA.SpectroscopyPanelsLogFile+"_from_form_file"
  LO.create_log("main","",recordType)
  
  SPR.load_spectroscopypanels_Records()

##############################################
# MAIN
##############################################
if __name__ == '__main__': 
  main ()


