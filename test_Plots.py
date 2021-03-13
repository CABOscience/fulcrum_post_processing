#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
from . import projects as PR
from . import parameters as PA
from . import Plots_record as PLOR
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
  recordType= PA.PlotsLogFile+"_plots_test"
  LO.create_log(recordType)
  plots = PLOR.load_plots()
  print(len(plots))
  
  plot = PLOR.get_plot_with_plot_id('hello-world')
  print(plot)

  plot = PLOR.get_plot_with_plot_id('9acf0b72-8b29-4372-97ac-91f950d6c00b')
  print(plot)

##############################################
# MAIN
##############################################
if __name__ == '__main__': 
  main ()

