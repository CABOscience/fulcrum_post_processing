#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
from . import logs as LO
from . import parameters as PA
from . import projects as PR
# System
import os

##############################################
#
# MAIN FUNCTION
#
##############################################
def main():
  PA.set_parameters()
  recordType= PA.PlantsLogFile+"_projects_test"
  LO.create_log(recordType)
  projects = PR.load_projects()
  print(projects)
  print(PR.get_project_name_from_id('5139c2a4-0ccf-43b2-8067-aedee40d478a'))
  

##############################################
# MAIN
##############################################
if __name__ == '__main__': 
  main ()


