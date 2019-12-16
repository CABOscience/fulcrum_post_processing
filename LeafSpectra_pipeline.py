#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
import projects as PR
import parameters as PA
import tools as TO
import logs as LO
import sys, time
from datetime import datetime 
import LeafSpectra_concat_files as LSCF
import LeafSpectra_record as LSR
#import SpectroscopyPanels_calibrations as SPC
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
  start_time = datetime.now() 
  PA.set_parameters()
  time_pa = TO.print_time(start_time,start_time,'Parameters')
  recordType= PA.LeafSpectraLogFile+"_from_form_file"
  LO.create_log("main","",recordType)
  projects = PR.load_projects()
  PR.create_project_website_view_directories(projects)
  time_pr = TO.print_time(start_time,time_pa,'Project')
  
  LO.l_info('\n\n## Start load records from Spectroscopy panels')
  #calibrations  = SPC.extract_SpectroscopyPanels_calibrations()
  spectroPanels = SPR.load_spectroscopypanels()
  time_spr = TO.print_time(start_time,time_pr,'SpectroPanels')
  
  # Extract records
  records = []
  if PA.FormsProcess:
    LO.l_info('\n\n## Start load records from leafspectra')
    records = LSR.load_leafspectra_Records(spectroPanels)
    LO.l_info('\n\n## End load records from leafspectra')
    time_llr = TO.print_time(start_time,time_spr,'load_leafspectra_Records')
    LO.l_info('\n\nNumber of Valid Records {}\n######\n\n'.format(records.number_of_valid()))
  else:
    LO.l_info('\n\n## Start load records from webhook')
    records = LSR.load_leafspectra_webhook_Records(calibrations)
    LO.l_info('\n\n## End load records from webhook')
    time_llr = TO.print_time(start_time,time_spr,'load_leafspectra_webhook_Records')
    LO.l_info('\n\nNumber of Valid Records {}\n######\n\n'.format(records.number_of_valid()))
  
  LO.l_info('\n\n## Process records\nNumber of Records {}\n######\n'.format(len(records)))
  records = LSR.process_leafspectra_records(records)
  time_plr = TO.print_time(start_time,time_llr,'process_leafspectra_records')
  LO.l_info('\n\nNumber of Valid Records {}\n######\n\n'.format(records.number_of_valid()))
  
  LO.l_info('\n\n## Plots records\nNumber of Records {}\n######\n'.format(len(records)))
  records = LSR.plots_leafspectra_records(records)
  time_plotr = TO.print_time(start_time,time_plr,'plots_leafspectra_records')
  LO.l_info('\n\nNumber of Valid Records {}\n######\n\n'.format(records.number_of_valid()))
  
  LO.l_info('\n\n## Update records\nNumber of Records {}\n######\n'.format(len(records)))
  records = LSR.update_leafspectra_records(records)
  time_ulr = TO.print_time(start_time,time_plotr,'update_leafspectra_records')
  LO.l_info('\n\nNumber of Valid Records {}\n######\n\n'.format(records.number_of_valid()))
  
  LO.l_info('\n\n## Print records log\nNumber of Records {}\n######\n'.format(len(records)))
  LSR.print_log_records(records)
  time_plor = TO.print_time(start_time,time_ulr,'print_log_records')
  LO.l_info('\n\nNumber of Valid Records {}\n######\n\n'.format(records.number_of_valid()))
  
  LO.l_info('## Concat Files\nNumber of Records {}\n######\n'.format(len(records)))
  LSCF.concat_files(records, projects)
  time_clr = TO.print_time(start_time,time_plor,'concat_files')
  LO.l_info('\n\nNumber of Valid Records {}\n######\n\n'.format(records.number_of_valid()))

##############################################
# MAIN
##############################################
if __name__ == '__main__': 
  main ()


