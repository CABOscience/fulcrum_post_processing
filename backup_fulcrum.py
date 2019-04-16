#!/usr/bin/env python
import projects as PR
import parameters as PA
import forms as FO
import records as RE
import tools as TO
import tools_fulcrum_api as TOFA
import tools_plots as PL
import logs as LO
import photos as PH
import sys
import multiprocessing as mp


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
# Global variables
Keys_dataname     = {}


##############################################
#
# MAIN FUNCTION
#
##############################################
def main():
  PA.set_parameters()
  LO.create_log("main","",'backup_fulcrum')
  TOFA.check_fulcrum_version()
  # Backup projects
  PR.backup_projects_from_Fulcrum()
  # Backup Forms (Applications)
  formsO = FO.load_fulcrum_formsJson()
  mp_backup_forms(formsO)
  TOFA.print_num_of_request()

def mp_backup_forms(formsO):
  """
  This parallelisation of backup_form
  """
  # parallelisation here
  output = mp.Queue()
  wraps = []
  pool = mp.Pool(processes=int(PA.NumberOfProcesses))
  recordsForm = [pool.apply_async(mp_backup_form, args=(form,)) for form in formsO.forms[:]]
  pool.close()
  pool.join()
  for r in recordsForm:
    b = r.get()
    if b:
      wraps.append(b)
  return warps

def mp_backup_form(form):
  formName = form.name_cleaned
  formID   = form.id
  if formID:
    # Backup records
    records = RE.backup_records_from_form(form)
    
    # Backup records versions
    if form.script and '/* SAVE VERSIONS */' in form.script:
      RE.backup_records_versions(form,records)
    else:
      LO.l_war("No records versions for {st} will not be saved.\n\
                If you need to saved records versions for {st}.\n\
                Please add /* SAVE VERSIONS */ in the top of it's 'data events'\n\
                ".format(st=formName))
    
    # Backup images
    PH.backup_photos_from_records(form,records)
    return records

##############################################
# MAIN
##############################################
if __name__ == '__main__': 
  main ()


