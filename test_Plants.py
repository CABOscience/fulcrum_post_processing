#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
from . import projects as PR
from . import parameters as PA
from . import Plants_record as PLAR
from . import forms as FO
from . import tools as TO
from . import logs as LO

# Spectroscopy
import specdal
# System
import sys

##############################################
#
# MAIN FUNCTION
#
##############################################
def main():
  PA.set_parameters()
  recordType= PA.PlantsLogFile+"_plants_test"
  LO.create_log(recordType)
  plants = PLAR.load_plants()
  print(len(plants))
  
  plant = PLAR.get_plant_with_plant_id_from_plants('hello-world')
  print(plant)

  plant = PLAR.get_plant_with_plant_id_from_plants('e8adadd6-be8c-4ee2-acad-e250ee012851')
  print(plant)

##############################################
# MAIN
##############################################
if __name__ == '__main__': 
  main ()

