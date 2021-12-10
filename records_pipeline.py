#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
import projects as PR
import parameters as PA
import tools as TO
import logs as LO
import sys, time
from datetime import datetime
import records as RE
import forms as FO

##############################################
#
# MAIN FUNCTION
#
##############################################
def main():
  start_time = datetime.now()
  PA.set_parameters()
  time_pa = TO.print_time(start_time,start_time,'Parameters')
  leafSpectraForm = FO.load_form_from_json_file(PA.LeafSpectraFormFile)
  leafSpectraFormID = leafSpectraForm.id
  if not PA.FormsProcess:
    wrecords = RE.record_webhook_to_db()
    for rec in wrecords.records[:]:
      if leafSpectraFormID not in rec.form_id:
        fname = TO.get_WebhookRecordsPath()+'/'+rec.id+''
        TO.delete_a_file(fname)


##############################################
# MAIN
##############################################
if __name__ == '__main__':
  main ()

