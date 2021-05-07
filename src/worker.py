from hotqueue import HotQueue
import json
import os
import redis
import jobs


redis_ip = os.environ.get('REDIS_IP')
print(redis_ip)
if not redis_ip:
  raise Exception()


#rd = redis.StrictRedis(host=redis_ip, port=6413, db=0, decode_responses=True)
#q = HotQueue('queue', host=redis_ip, port=6413, db=1)
rd = jobs.rd
q = jobs.q


def get_data():  # gets all data in the redis db
  userdata = []
  for key in rd.keys():
    userdata.append(str(rd.hgetall(key)))
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



def attribval(data):  # get all records with attribute of value
  jobs.update_job_status(jid, 'in progress')
  records = get_data()  # get the db data

  attrib = data['attrib']
  value = data['value']

  output = []
  output = [ x for x in bintoregular(anims) if str(x[str(attrib)]) == str(value) ]

  rd.hset(jid, json.dumps(output))

  jobs.update_job_status(jid, 'complete')


@q.worker
def runjobs(job):  # passes in a job id so worker can get the job off the queue
  data = rd.hgetall(job) 
  print(data)
  if data['type'] == 'attribval':
    attribval(data)  # do the appropriate job function



if __name__ == '__main__':
  runjobs()
