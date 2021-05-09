from flask import Flask, request, send_file
import json
from hotqueue import HotQueue
import redis
import os
import jobs
import uuid
import sys


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

  /						info
  /loaddata/					load data into Redis database
  /records/info/				information about the records
  /records/attribval/<attribute>/<value>/	get all records with an attribute with a certain value
  /records/contains/<word>/			get all records that have a certain word
  /records/id/<record id>/			get a specific record
  /records/delete/<record id>/			TODO delete a specific record
  /job/<job id>/				view the information about a submitted job
  /result/<job id>/				see the result of a submitted job
  /viz/<attrib>/<startyear>/<endyear>/		TODO visualize an attribute over a selection of years. Available attributes are Age, Sex, Fatal.

"""

# get information about the records
@app.route('/records/info/', methods=['GET'])
def record_info():
  return """
  ATTRIBUTE		DESCRIPTION
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
  Age			Numerical age or ?
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
  jobdict = jobs.add_job(jobdict)
  print(jobdict, file=sys.stderr)
  return "Submitted job "+jobdict['jid']

# return info about a certain job
@app.route('/job/<wantedid>/', methods=['GET'])
def getjob(wantedid):
  return rd.hgetall('job.'+wantedid)

# return result of a job
@app.route('/result/<wantedid>/', methods=['GET'])
def getresult(wantedid):
  return rd.hget('job.'+wantedid, 'result')


# return a specific record
@app.route('/records/id/<wantedid>/', methods=['GET'])
def getrecord(wantedid):
  jobdict = {
  'type': 'getrecord',
  'wantedid': str(wantedid) } 
  jobdict = jobs.add_job(jobdict)
  return "Submitted job "+jobdict['jid']


# return all records containing a specific string
@app.route('/records/contains/<word>/', methods=['GET'])
def record_contains(word):
  jobdict = {
  'type': 'contains',
  'word': word }
  jobdict = jobs.add_job(jobdict)
  return "Submitted job "+jobdict['jid']


if __name__=='__main__':
  app.run(debug=True, host='0.0.0.0')

