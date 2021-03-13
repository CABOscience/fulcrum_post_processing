#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
from . import projects as PR
from . import parameters as PA
from . import Plants_record as PLR
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

##############################################
# MAIN
##############################################
if __name__ == '__main__': 
  main ()
