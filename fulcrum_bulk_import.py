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
python3 fulcrum_bulk_import.py [-h] [-a FulcrumApiKey] [--file path/to/bulk/file]

optional arguments:
  -a FulcrumApiKey, --FulcrumApiKey FulcrumApiKey
                        Need a fulcrum Api key
  --file path/to/bulk/file
'''
##############################################
# MAIN FUNCTION
##############################################
def main():
  PA.set_parameters()
  with open(PA.FulcrumBulkFile) as f:
    lines = f.read().splitlines()
  
  for line in lines[:]:
    if len(line)>0:
      data = {}
      data["id"] = "{}".format(line)
      data["form_id"] = "{}".format(PA.FulcrumBulkFormId)
      fname = PA.FulcrumWebhook+"records/"+"{}".format(line)
      TO.save_in_json_file(fname,data)


##############################################
# MAIN
##############################################
if __name__ == '__main__': 
  main ()

