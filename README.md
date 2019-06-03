# fulcrum_post_processing
The fulcrum post processing 

## Fulcrum Python
```
$ sudo apt-get update
$ sudo apt-get install git
$ git clone https://github.com/fulcrumapp/fulcrum-python.git
$ cd fulcrum-python/
$ python setup.py build
$ sudo python setup.py install
```

Object:
fulcrumApp = connection to fulcrum
forms      = [] a json like https://developer.fulcrumapp.com/endpoints/forms/#form-properties
records    = [] a json like https://developer.fulcrumapp.com/endpoints/records/#record-properties
images     = [] a json like https://developer.fulcrumapp.com/endpoints/photos/#photo-properties

It saves logs in a subdirectory ./logs/ 

It creates 4 types of fulcrum backups :
- two types of fulcrum backups (with and without version)
- two types of fulcrum backups (with and without dataname)

Structure of a saved form:
[fulcrumPath]/form-name
[fulcrumPath]/form-name/images
[fulcrumPath]/form-name/versions

## Config parser
Use config parser to set parameters it will allow to simplify the loading and be able to set default values
```
$ sudo apt install python-configparser
```
In python script
```
import configparser
config = configparser.RawConfigParser()
config.read('example.cfg')
```
## Plots
`$ sudo apt-get install python-matplotlib`

## SpecDAL
```
$ sudo apt-get install python-pandas python-scipy python-setuptools
$ git clone  -b caboscience  https://github.com/CABOscience/SpecDAL.git
$ cd SpecDAL
$ sudo python setup.py install
```

## For packaging and version
`$ sudo apt install python-setuptools`

## For Parallelisation
`$ pip install multiprocess`

## All in one
```
$ sudo apt-get update
$ sudo apt-get install git python-configparser python-matplotlib python-pandas python-scipy python-setuptools python-pip
$ pip install multiprocess
$ mkdir ~/python-modules
$ cd ~/python-modules
$ git clone  -b caboscience  https://github.com/CABOscience/SpecDAL.git
$ cd SpecDAL
$ sudo python setup.py install
$ cd ~/python-modules
$ git clone https://github.com/fulcrumapp/fulcrum-python.git
$ cd fulcrum-python/
$ python setup.py build
$ sudo python setup.py install
```
