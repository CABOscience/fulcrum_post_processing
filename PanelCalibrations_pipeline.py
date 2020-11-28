#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
from . import projects as PR
from . import parameters as PA
from . import tools as TO
from . import logs as LO
import sys, time
from datetime import datetime 
from . import PanelCalibrations_concat_files as LSCF
from . import PanelCalibrations_record as PCR
#import SpectroscopyPanels_calibrations as SPC
from . import SpectroscopyPanels_record as SPR

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
  recordType= PA.PanelCalibrationLogFile+"_from_form_file"
  LO.create_log("main","",recordType)
  
  LO.l_info('\n\n## Start load records from Panel Calibrations')
  records = PCR.load_panelCalibrations()
  time_lpc = TO.print_time(time_pa,datetime.now(),'Panel Calibrations')
  
  LO.l_info('\n\n## Start load records from Spectroscopy panels')
  spectroPanels = SPR.load_spectroscopypanels()
  time_spr = TO.print_time(start_time,time_lpc,'SpectroPanels')

  LO.l_info('\n\n## Process records\nNumber of Records {}\n######\n'.format(len(records)))
  records = PCR.link_panel_calibrations_records_and_calibration(spectroPanels,records)
  records = PCR.process_panel_calibrations_records(records)
  time_plr = TO.print_time(time_spr,datetime.now(),'process_leafspectra_records')
  LO.l_info('\n\nNumber of Valid Records {}\n######\n\n'.format(records.number_of_valid()))

  LO.l_info('\n\n## Plots records\nNumber of Records {}\n######\n'.format(len(records)))
  records = PCR.plots_panel_calibrations_records(records)
  time_plotr = TO.print_time(start_time,time_plr,'plots_panel_calibrations_records')
  LO.l_info('\n\nNumber of Valid Records {}\n######\n\n'.format(records.number_of_valid()))

  # plots
  # update calibrations records
  ''' FOM LEAFSPECTRA
  LO.l_info('\n\n## Plots records\nNumber of Records {}\n######\n'.format(len(records)))
  records = LSR.plots_leafspectra_records(records)
  time_plotr = TO.print_time(start_time,time_plr,'plots_leafspectra_records')
  LO.l_info('\n\nNumber of Valid Records {}\n######\n\n'.format(records.number_of_valid()))
  
  LO.l_info('\n\n## Update records\nNumber of Records {}\n######\n'.format(len(records)))
  records = LSR.update_leafspectra_records(records)
  time_ulr = TO.print_time(start_time,time_plotr,'update_leafspectra_records')1
  LO.l_info('\n\nNumber of Valid Records {}\n######\n\n'.format(records.number_of_valid()))
  
  LO.l_info('\n\n## Print records log\nNumber of Records {}\n######\n'.format(len(records)))
  LSR.print_log_records(records)
  time_plor = TO.print_time(start_time,time_ulr,'print_log_records')
  LO.l_info('\n\nNumber of Valid Records {}\n######\n\n'.format(records.number_of_valid()))
  
  LO.l_info('## Concat Files\nNumber of Records {}\n######\n'.format(len(records)))
  LSCF.concat_files(records, projects)
  time_clr = TO.print_time(start_time,time_plor,'concat_files')
  LO.l_info('\n\nNumber of Valid Records {}\n######\n\n'.format(records.number_of_valid()))
  '''
  
##############################################
# MAIN
##############################################
if __name__ == '__main__': 
  main ()


