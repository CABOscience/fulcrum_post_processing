#!/usr/bin/env python
import records as RE
import time
import projects as PR
import parameters as PA
import tools as TO
import logs as LO
import sys, time
from datetime import datetime

'''
Usage:
python backup_fulcrum.py [-h] [-a FulcrumApiKey] [-f FORMS [FORMS ...]]
                                [-p PATH]

Options Fulcrum Backup.
optional arguments:
  -a FulcrumApiKey, --FulcrumApiKey FulcrumApiKey
                        Need a fulcrum Api key
  -f FORMS [FORMS ...], --forms FORMS [FORMS ...]
                        Select specific forms by name or id. Example: -f Plots
                        Sites 'Bulk Leaf Samples' 'Vegetation Surveys: Herbs
                        and Shrubs'
  -p PATH, --path PATH  Choose a directory for backup
'''
##############################################
# MAIN FUNCTION
##############################################
def main():
  PA.set_parameters()
  start_time = datetime.now()
  if PA.FormsProcess:
    LO.create_log("backup_fulcrum")
    RE.backup_records_from_fulcrumforms()
  else:
    LO.create_log("backup_fulcrum_webhook")
    RE.record_webhook_to_db()

##############################################
# MAIN
##############################################
if __name__ == '__main__': 
  main ()

