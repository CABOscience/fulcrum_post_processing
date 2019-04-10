#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
from parameters import *
import parameters as PA
import tools as TO
# System
import os

##############################################
# Projects
##############################################
def load_projects():
  projectsPath = FulcrumPath+'Projects/'
  # list files in directory
  projects = {}
  projectsFile = TO.get_files_from_path(projectsPath)
  for projectFile in projectsFile:
    projectJson = TO.load_json_file(projectFile)['project']
    projectName = projectJson['name']
    projectID   = projectJson['id']
    projects[projectID] = projectName
  return projects


def create_project_website_view_directories(projects):
  for project in projects.values():
    create_project_directories(project)
    create_symbolic_links(project)

def create_project_directories(projectName):
  directories = ['leafscans', 'spectra']
  subDirectories = ['processed']
  for directory in directories:
    for subDirectory in subDirectories:
      p = PA.ProjectWebsitePath+projectName+'/'+directory+'/'+subDirectory
      if not os.path.exists(p):
        os.makedirs(p)

def create_symbolic_links(projectName):
  directories = ['leafscans', 'spectra']
  subDirectories = ['raw']
  for directory in directories:
    for subDirectory in subDirectories:
      src = CampaignsPath+projectName+'/'+directory
      if os.path.exists(src):
        dest = PA.ProjectWebsitePath+projectName+'/'+directory+'/'+subDirectory
        if not os.path.exists(dest):
          os.symlink(src,dest)

