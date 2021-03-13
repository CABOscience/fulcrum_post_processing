#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Local Modules
from .parameters import *
from . import parameters as PA
from . import tools as TO
from . import tools_fulcrum_api as TOFA
# System
import os

def get_ProjectsPath():
  projectsPath = PA.FulcrumPath+'Projects'
  TO.create_directory(projectsPath)
  return projectsPath

##############################################
# Projects
##############################################

class Projects():
  def __init__(self):
    self.projects = []
    self.idName = {}
    self.nameId = {}
  
  def add_project(self,project):
    if project_is_available(project):
      self.projects.append(project)
      self.idName[project.id] = project.name
      self.nameId[project.name] = project.id
    
  def get_projects_size(self):
    return len(self.projects)
    
  def __str__(self):
    st = ''
    print(self.get_projects_size())
    for project in self.projects[:]:
      if project.id != "":
        st += '{}'.format(project)
    return st
    
  def __len__(self):
    return len(self.projects)
    
  
class Project():
  def __init__(self,created_at = "", description = "", ID = "", name = "", updated_at = ""):
    self.created_at = created_at
    self.description = description
    self.id = ID
    self.file_name = ""
    self.name = name
    self.name_cleaned = ""
    self.fulcrum_cleaned_name = ""
    self.updated_at = updated_at
  
  def set_NameCleaned(self):
    self.name_cleaned = TO.clean_name(self.name)
    self.fulcrum_name_cleaned = TO.fulcrum_clean_name(self.name)
  
  def set_file_name(self):
    self.file_name = get_ProjectsPath()+'/'+self.name_cleaned+'.json'
  
  def __str__(self):
    return '{} {} {}'.format(self.id,self.file_name,self.name_cleaned)

#
# Project(s) From Json
#
def create_projects_from_json(projectsJson):
  ps = Projects()
  for projectJson in projectsJson:
    project = create_project_from_json(projectJson)
    ps.add_project(project)
  return ps

def create_project_from_json(projectJson):
  project = Project(projectJson['created_at'], projectJson['description'], projectJson['id'], projectJson['name'], projectJson['updated_at'])
  project.set_NameCleaned()
  project.set_file_name()
  return project
    
#
# Backup Projects
#
def backup_projects_from_Fulcrum():
  bName = TO.get_file_basename('Projects')
  if not os.path.exists(bName):
    os.makedirs(bName)
  
  projectsJson = TOFA.get_projects()
  if projectsJson:
    fname = PA.FulcrumPath+'all_projects.json'
    TO.save_in_json_file(fname,projectsJson)

    ps = create_projects_from_json(projectsJson)
    for project in ps.projects[:]:
      fname = project.file_name
      TO.save_in_json_file(fname,project.__dict__)
    return ps
  else:
    return Project()

#
# Load Project(s)
#

def get_project_name_from_id(project_id,pjs=[]):
  if isinstance(pjs, Projects):
    if project_id in pjs.idName:
      return pjs.idName[project_id]
    pass
  elif len(pjs)<1:
    return get_project_name_from_id(project_id,load_projects())
  return ""

def load_backuped_projects():
  ps = Projects()
  projectsFile = TO.get_files_from_path(get_ProjectsPath()+'/')
  for projectFile in projectsFile:
    projectJson = TO.load_json_file(projectFile)
    if 'id' in projectJson:
      project = create_project_from_json(projectJson)
      ps.add_project(project)
  return ps

def load_projects():
  ps = load_backuped_projects()
  if ps.get_projects_size() < 1:
    ps = backup_projects_from_Fulcrum()
  return ps

#
# Website Project(s) directories (with symbolic links)
#
def create_project_website_view_directories(projects):
  for project in list(projects.idName.values()):
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
      src = PA.CampaignsPath+projectName+'/'+directory
      if os.path.exists(src):
        dest = PA.ProjectWebsitePath+projectName+'/'+directory+'/'+subDirectory
        if not os.path.exists(dest):
          os.symlink(src,dest)

#
# Records and Project
#
def extract_projects_ID_from_records(records):
  ps = Projects()
  for record in records:
    if 'project_id' in record and record['project_id']:
      project_id = record['project_id']
      if project_id not in ps.idName:
        projectJson = find_project_from_project_ID(project_id)
        project = create_project_from_json(projectJson)
        ps.add_project(project)
  return projectsID

#
# Project is specific
#
def project_is_available(project):
  b = False
  if len(PA.FulcrumProjects)>0:
    if project.id in PA.FulcrumProjects or project.name in PA.FulcrumProjects:
      b = True
  else:
    b = True
  return b

def test_if_project_id(project_id,pjs=[]):
  return project_id in pjs.idName

