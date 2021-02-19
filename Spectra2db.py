#!/usr/bin/env python
# -*- coding: utf-8 -*-
import forms as FO
import parameters as PA
import records as R
import json
import csv
import psycopg2
from psycopg2.extensions import AsIs
import os
import LeafSpectra_record as LS

conn = psycopg2.connect("dbname=cabo_test user=postgres host=vm-03")
conn.set_session(autocommit=True)
cur = conn.cursor()
PA.set_parameters()

spectra_processed_fields = ["record_id","sample_id","scientific_name","date_measured","measured_by","spectroradiometer_start_time","spectroradiometer_id","instrumentation_id","leaf_side_measured","reflectance_transmittance","wavelength","r_t_average","r_t_std"]
spectra_leaves_fields = ["record_id","sample_id","file_name","leaf_number","leaf_side_measured","reflectance_transmittance","wavelength","raw_value","calculated_value"]


def SpectraDBInsert(table, fields, values):
	insert_statement = 'INSERT INTO %s (%s) VALUES %s'
	cur.execute(insert_statement, (AsIs(table), AsIs(','.join(fields)), tuple(values)))

def checkRecord(table, record_id, sample_id, leaf=False):
	if(leaf==False):
		cur.execute("SELECT record_id FROM %s WHERE record_id = %s AND sample_id = %s", (AsIs(table),record_id,sample_id))
	else:
		cur.execute("SELECT record_id FROM %s WHERE record_id = %s AND sample_id = %s AND leaf_number=%s", (AsIs(table),record_id,AsIs(sample_id),AsIs(leaf_number)))
	if cur.fetchone() is not None:
		return True
	else:
		return False

def SpectraDBDelete(table, record_id, sample_id, leaf=False):
	if(leaf == False):
		cur.execute("DELETE FROM %s WHERE record_id = %s AND sample_id = %s", (AsIs(table),record_id,sample_id))
	else:
		cur.execute("DELETE FROM %s WHERE record_id = %s AND sample_id = %s AND leaf_number=%s", (AsIs(table),record_id,AsIs(sample_id),AsIs(leaf_number)))

def LeafSpectra2DB(record):
	#c,l,r = LS.leafspectra_record_to_csv_values(record)
	with open('/home/canadensys/data-website/projects/2019-Boucherville/spectra/processed/2019-07-15-GroboisFieldEL-2092/44066732/all.csv') as csvfile:
		next(csvfile)
		read = csv.reader(csvfile, delimiter=',', quotechar='"')
		SpectraDBProcessAll(read)

def SpectraDBProcessAll(spectra_csv)
		i = 0
		for row in spectra_csv:
			if i == 0 and checkRecord('spectra_processed',row[0],row[1]) == True:
				SpectraDBDelete('spectra_processed',row[0],row[1])
			SpectraDBInsert('spectra_processed',spectra_processed_fields,row)
			i += 1
		print('Spectra All - Inserted ' + str(i) + ' rows')


def SpectraDBProcessLeaves(spectra_csv)
		i = 0
		for row in spectra_csv:
			if i == 0 and checkRecord('spectra_processed',row[0],row[1],row[3]) == True:
				SpectraDBDelete('spectra_processed',row[0],row[1],row[3])
			SpectraDBInsert('spectra_leaves',spectra_leaves_fields,row)
			i += 1
		print('Spectra Leaves - Inserted ' + str(i) + ' rows')
