from flask import Flask, request, send_file
import json
from hotqueue import HotQueue
import redis
import os
import jobs
import uuid


redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
  raise Exception()


app = Flask(__name__)

rd = jobs.rd
q = jobs.q
data = jobs.data


# v--- routes ---v

@app.route('/', methods=['GET'])
def info():
  return """
  Routes:

  /					info
  /loaddata/				load data into Redis DB
  /records/info/			information about the records
  /records/<attribute>/<value>/		get all records with an attribute with a certain value
  /records/contains/<word>/		TODO get all records that have a certain word
  /records/<record id>/			TODO get a specific record
  /viz/<attrib>/<startdate>/<enddate>/	TODO vizualize an attribute from start to end date.

"""

# get information about the records
@app.route('/records/info/', methods=['GET'])
def record_info():
  return """
  ATTRIBUTE	DESCRIPTION
  original order	A number that uniquely identifies a record
  Date			Usually year, sometimes descriptive and inexact, sometimes down to the day
  Year			Numerical year or 0000
  Type			Type of incident. Can be Provoked, Unprovoked, Watercraft, Sea Disaster, Under Investigation, Invalid, Unconfirmed, Unverified, Questionable
  Country		All caps country or UNKNOWN
  Area			Smaller region or UNKNOWN
  Location		Local location or UNKNOWN
  Activity		Details about what happened
  Name			Name of the person (or gender or who they were)
  Sex			F, M, or ?
  Age			numerical age or ?
  Injury		Details about the injury
  Fatal			Y, N, or ?
  Time			When attack happened or ?
  Species		Species or UNKNOWN
  href			Link to PDF with more info

"""

# DONE load data from json to db
@app.route('/loaddata/', methods=['GET'])
def load_data():
  with open('sharkattacks.json', 'r', encoding='utf-8-sig') as f:  # encoding='utf-8-sig'
    sharks = json.load(f)  # sharks is a dict
    for record in sharks:
      data.hmset(record['original order'], record) # add the record data to the db
  return "success"


# get all records with an attribute with a certain value. SEND A JOB
@app.route('/records/<attrib>/<value>/', methods=['GET'])
def get_records_cust(attrib, value):
  jobdict = {
  'type': 'attribval',
  'attrib': str(attrib),
  'value': str(value)
}
  print(type(jobdict))
  jobdict = jobs.add_job(jobdict)
  return "Submitted job "+jobdict['jid']

# 


if __name__=='__main__':
  app.run(debug=True, host='0.0.0.0')

