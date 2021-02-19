#!/usr/bin/env python
# -*- coding: utf-8 -*-
import forms as FO
import parameters as PA
import records as R
import json
import psycopg2
from psycopg2.extensions import AsIs
import os

conn = psycopg2.connect("dbname=cabo_test user=postgres host=vm-03")
conn.set_session(autocommit=True)
cur = conn.cursor()
PA.set_parameters()
common_fields_main = {
	"id":"fulcrum_id",
	"assigned_to":"assigned_to", 
	"created_at":"created_at", 
	"created_by":"created_by", 
	"latitude":"latitude", 
	"longitude":"longitude", 
	"status":"status", 
	"updated_at":"updated_at", 
	"updated_by":"updated_by", 
	"version":"version", 
	"horizontal_accuracy": "gps_horizontal_accuracy",
	"vertical_accuracy": "gps_vertical_accuracy", 
	"speed": "gps_speed", 
	"course": "gps_course", 
	"altitude": "gps_altitude"
}
common_fields_sub = {
	"created_at":"created_at", 
	"created_by":"created_by", 
	"updated_at":"updated_at", 
	"updated_by":"updated_by", 
	"version":"version", 
}

vals={}


def prepareRecordValues(record):
	vals={}
	FF = FO.get_form_from_formid(record.form_id)
	keysTypes = FF.dictKeysTypes
	keysDataNames = FF.dictKeysDataName
	def recuMapValues(tblName, values, record, id):
		kv = {}
		if id == 0: #The main form table
			for f in common_fields_main:
				kv[common_fields_main[f]] = getattr(record, f)
		else: # Sub tables
			kv["fulcrum_parent_id"] = record.id
			kv["fulcrum_record_id"] = record.id
			kv['fulcrum_id'] = id
			for f in common_fields_sub:
				kv[common_fields_sub[f]] = getattr(record, f)
								
		for v in values:
			if v in keysTypes:
				if keysTypes[v] in ['TextField','CalculatedField','BarcodeField','Label','DateTimeField','YesNoField','TimeField','ClassificationField','HyperlinkField']:
					kv[keysDataNames[v]] = values[v]
				elif keysTypes[v] in ['RecordLinkField']:
					rf=[]
					for r in values[v]:
						rf.append(r['record_id'])
					kv[keysDataNames[v]] = ",".join(rf)
				elif keysTypes[v] in ['ChoiceField']:
					kv[keysDataNames[v]] = ",".join(values[v]['choice_values'])
				elif keysTypes[v] in ['Repeatable']:
					for rep in values[v]:
						recuMapValues(tblName + '_' + keysDataNames[v], rep['form_values'], record, rep['id'])
				elif keysTypes[v] in ['PhotoField']:
					photos=[]
					captions=[]
					for p in values[v]:
						if p['photo_id'] is not None:
							photos.append(p['photo_id'])
						if p['caption'] is not None:
							captions.append(p['caption'])
					kv[keysDataNames[v]] = ",".join(photos)
					kv[keysDataNames[v]+"_caption"] = ",".join(captions)
		if tblName not in vals:
			vals[tblName]=[kv]
		else:
			vals[tblName].append(kv)
	recuMapValues(formatFormName(FF.name), record.form_values, record, 0)
	return vals


def formatFormName(fName):
	return fName.lower().replace(' ','_')

def checkRecord(table, id):
	cur.execute("SELECT fulcrum_id FROM %s WHERE fulcrum_id = %s", (AsIs(table),id))
	if cur.fetchone() is not None:
		return True
	else:
		return False

def insertRecord(values):
	for table in values:
		for r in values[table]:
			if checkRecord(table, r['fulcrum_id']) == True:
				cur.execute('DELETE FROM %s WHERE fulcrum_id = %s', (AsIs(table),r['fulcrum_id']))
				print('Updating record')
			else:
				print('Inserting record')
			columns = r.keys()
			val = [r[column] for column in columns]
			insert_statement = 'INSERT INTO %s (%s) VALUES %s'
			cur.execute(insert_statement, (AsIs(table), AsIs(','.join(columns)), tuple(val)))
			#print cur.mogrify(insert_statement, (AsIs(table), AsIs(','.join(columns)), tuple(val)))


def recordWebhook2DB(rec):
	FF = FO.get_form_from_formid(rec.form_id)
	if(FF.name != 'Pigments'):  ## TO UPDATE WHEN NEW SQL IS TRANSFERRED!!!!
		insertRecord(prepareRecordValues(rec))

def scanWebhookFolder():
	for filename in os.listdir('/home/canadensys/fulcrum_webhook_data/records/'):
		rec=R.record_from_fileName('/home/canadensys/fulcrum_webhook_data/records/'+filename)
		recordWebhook2DB(rec)
