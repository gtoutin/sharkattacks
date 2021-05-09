from hotqueue import HotQueue
import json
import os
import redis
import jobs
import sys



#rd = redis.StrictRedis(host=redis_ip, port=6413, db=0, decode_responses=True)
#q = HotQueue('queue', host=redis_ip, port=6413, db=1)
rd = jobs.rd
q = jobs.q
data = jobs.data


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
  print(len(output),file=sys.stderr)
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

  rd.hset(f'job.{jid}', 'result', str(output))  # put the result in the job entry in the db
  jobs.update_job_status(jid, 'complete')  # now it's done
  print('updated status to complete',file=sys.stderr)


if __name__ == '__main__':
  print("worker is alive",file=sys.stderr)
  runjobs()

