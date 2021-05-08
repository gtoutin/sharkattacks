from hotqueue import HotQueue
import json
import os
import redis
import jobs



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

# DONE convert dict full of binary strings to one with regular strings
def bintoregular(anims):
  output = []
  for anim in anims:  # destring the animals
      animdict = eval(anim)  # turn into a dictionary per animal
      animdictdecode = {}
      for thing in animdict:  # convert binary to regular string
          animdictdecode[thing.decode('ascii')] = animdict[thing].decode('ascii') # convert each key:value to regular strings
      output.append(animdictdecode)
  return output



def attribval(indict):  # get all records with attribute of value
  jobs.update_job_status(indict['jid'], 'in progress')
  records = get_data()  # get the db data
  attrib = indict['attrib']
  value = indict['value']

  output = []
  output = [ x for x in records if x[attrib] == value ]

  rd.hset(jid, 'result', str(output))  # dump the output list to a string and put it in  !!!! FIX THIS ITS ALMOST RIGHT

  jobs.update_job_status(jid, 'complete')


@q.worker
def runjobs(jid):  # passes in a job key so worker can get the job off the queue
  indict = rd.hgetall(jobs.generate_job_key(jid))
  print(type(indict)) 
  if indict['type'] == 'attribval':
    attribval(indict)  # do the appropriate job function



if __name__ == '__main__':
  runjobs()

