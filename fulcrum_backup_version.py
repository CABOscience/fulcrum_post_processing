#!/usr/bin/env python
from . import records as RE
import time

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
  RE.backup_records_versions_from_forms()

##############################################
# MAIN
##############################################
if __name__ == '__main__': 
  main ()

