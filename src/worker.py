from hotqueue import HotQueue
import json
import os
import redis
import jobs
import sys
import matplotlib.pyplot as plt
import numpy as np



rd = jobs.rd
q = jobs.q
data = jobs.data
images = jobs.images


def get_data():  # gets all data in the redis db
  userdata = []
  for key in data.keys():
    userdata.append(data.hgetall(key))
  return userdata


def attribval(indict):  # get all records with attribute of value
  records = get_data()  # get the db data
  attrib = indict['attrib']
  value = indict['value']

  output = []
  output = [ x for x in records if x[attrib] == value ]
  return output


def getrecord(indict):  # get the record corresponding to the original order given (original order is the db key)
  wantedkey = indict['wantedid']
  try:
    output = data.hgetall(wantedkey)
  except:
    output = []
    print('no data with that key found', file=sys.stderr)
  return output


def record_contains(indict):  # get the records containing the word specified
  word = indict['word']  # the word requested
  records = get_data()
  
  output = [ x for x in records if ( word in x['Date'] or word in x['Type'] or word in x['Country'] or word in x['Area'] or word in x['Location'] or word in x['Activity'] 
    or word in x['Name'] or word in x['Injury'] or word in x['Time'] or word in x['Species'] ) ]
  return output


def record_delete(indict):  # delete the specified record
  recordid = indict['recordid']
  data.delete(recordid)
  output = [recordid]
  return output


def addrecord(indict):  # add the new record
  newdata = eval(indict['newdata'])  # this is a dict
  try:
#    data.hmset(newdata['original order'], newdata)
    for attrib in newdata:
      data.hset(newdata['original order'], attrib, newdata[attrib])
  except:
    return False
  return True


def editrecord(indict):  # edit an existing record's attribute
  records = get_data()
  recordid = indict['recordid']
  attrib = indict['attrib']
  value = indict['value']

  data.hset(recordid, attrib, value)

  return True
  

def vizrecords(indict):
  records = get_data()
  attrib = indict['attrib']
  startyear = int(indict['startyear'])
  endyear = int(indict['endyear'])
  jid = indict['jid']
  
  x = range(startyear, endyear+1)  # create list of every year between and including the years

  if attrib=='Age':
    avgages = []  # want to plot avg age vs year
    for year in x:  # loop thru all relevant years
      year = str(year)
      yearrecords = attribval({'attrib':'Year', 'value':year})  # get all records for a year

      agelist = []
      for y in yearrecords:
        try:
          agelist.append(int(y['Age']))
        except:
          continue
      if len(agelist) != 0: avgages.append(sum(agelist)/len(agelist))  # don't divide by 0
      else: avgages.append(0)

    plt.plot(x, avgages)  # make the plot
    plt.xlabel('Year')
    plt.ylabel('Average age')
    plt.title(f'Average age vs. Year for {startyear}-{endyear}')
    plt.savefig('/outimg.png')

  with open('/outimg.png', 'rb') as f:	# opens /jidplot.png as f
    image = f.read()	# reads saved plot into binary
  images.set(jid, image)

  return jid
  


@q.worker
def runjobs(jid):  # passes in a job key so worker can get the job off the queue
  print('worker activated', file=sys.stderr)

  indict = rd.hgetall(jobs.generate_job_key(jid))  # get all relevant job information

  print('job',indict['jid'],'has been received',file=sys.stderr)
  jobs.update_job_status(indict['jid'], 'in progress')

  # send the job info to the appropriate function
  if indict['type'] == 'attribval':
    output = attribval(indict)  # want all with key:value pair
  if indict['type'] == 'getrecord':
    output = getrecord(indict)  # want a job with a specific id (original order, which is the key in the data db)
  if indict['type'] == 'contains':
    output = record_contains(indict)
  if indict['type'] == 'recorddelete':
    output = record_delete(indict)
  if indict['type'] == 'addrecord':
    output = addrecord(indict)
  if indict['type'] == 'editrecord':
    output = editrecord(indict)
  if indict['type'] == 'viz':
    output = vizrecords(indict)  # returns image as a bytes object
  else: output = []

  rd.hset(f'job.{jid}', 'result', str(output))  # put the result in the job entry in the db
  jobs.update_job_status(jid, 'complete')  # now it's done
  print('updated status to complete',file=sys.stderr)


if __name__ == '__main__':
  print("worker is alive",file=sys.stderr)
  runjobs()

