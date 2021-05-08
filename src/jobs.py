# jobs.py

import uuid
from hotqueue import HotQueue
import redis
from redis import StrictRedis
import os

redis_ip = os.environ.get('REDIS_IP')

q = HotQueue("queue", host=redis_ip, port=6379, db=1)  # this queue sends job keys to the workers
rd = redis.StrictRedis(host=redis_ip, port=6379, db=0, decode_responses=True)  # this db contains info about jobs
data = redis.StrictRedis(host=redis_ip, port=6379, db=2, decode_responses=True)  # this db contains all the records

def _generate_jid():
    return str(uuid.uuid4())

def generate_job_key(jid):
    return 'job.{}'.format(jid)

def _instantiate_job(jid, origdict, status='submitted'):
    if type(jid) == str:
        newdict = origdict
        print(newdict)
        newdict['jid'] = jid
        newdict['status'] = status
        return newdict

    newdict = origdict
    newdict['jid'] = jid
    newdict['status'] = status
#    for entry in newdict:
    #    if not type(entry) == str:
    #        newdict[entry] = newdict[entry].decode('utf-8')
    return newdict

def _save_job(job_key, job_dict):  # a job object goes in the redis database
    """Save a job object in the Redis database."""
    rd.hmset(job_key, job_dict)  # jobkey = job.{jid}, job_dict is the original dict with the jid and status added

def _queue_job(jid):
    """Add a job to the redis queue."""
    q.put(jid)

def add_job(origdict, status="submitted"):  # given the original input to create a job and maybe status
    """Add a job to the redis queue."""
    #print(type(origdict))
    #print(origdict)
    jid = _generate_jid()  # create a uid for the job
    job_dict = _instantiate_job(jid, origdict, status) # add the id and status into the existing dictionary
    # update call to save_job:
    _save_job(generate_job_key(jid), job_dict)  # put the job and data in the redis db
    # update call to queue_job:
    _queue_job(jid)  # put the job on the queue so the worker can take it and look up the id
    return job_dict

def update_job_status(jid, newstatus):  # update the status of the job by altering the dictionary
    """Update the status of job with job id `jid` to status `status`."""
#    jid, status, start, end = rd.hmget(generate_job_key(jid), 'id', 'status', 'start', 'end')
    olddict = rd.hgetall(generate_job_key(jid))
    print(olddict) 
    job = _instantiate_job(jid, olddict)  # returns a job dictionary
    if job:
        job['status'] = newstatus
        _save_job(generate_job_key(jid), job)
    else:
        raise Exception()

def update_job_result(jid, result):  # update the result of the job by altering the dictionary
    recorddict = rd.hgetall(generate_job_key(jid))

    recorddict['result'] = result
    
    _save_job(generate_job_key(jid), recorddict)


