# jobs.py

import uuid
from hotqueue import HotQueue
import redis
from redis import StrictRedis
import os

redis_ip = os.environ.get('REDIS_IP')

q = HotQueue("queue", host=redis_ip, port=6379, db=1)
rd = redis.StrictRedis(host=redis_ip, port=6379, db=0)

def _generate_jid():
    return str(uuid.uuid4())

def _generate_job_key(jid):
    return 'job.{}'.format(jid)

def _instantiate_job(jid, job_dict):
    if type(jid) == str:
        job_dict['jobid'] = jid
        return job_dict

    job_dict['jobid'] = jid.decode('utf-8')
    return job_dict

def _save_job(job_key, job_dict):
    """Save a job object in the Redis database."""
    rd.hmset(job_key, job_dict)

def _queue_job(jid):
    """Add a job to the redis queue."""
    q.put(jid)

def add_job(jobdict, status="submitted"):
    """Add a job to the redis queue."""
    jid = _generate_jid()
    job_dict = _instantiate_job(jid, jobdict)
    # update call to save_job:
    _save_job(_generate_job_key(jid), job_dict)
    # update call to queue_job:
    _queue_job(jid)
    return job_dict

def update_job_status(jid, newstatus, workerIP):
    """Update the status of job with job id `jid` to status `status`."""
    jid, status, start, end = rd.hmget(_generate_job_key(jid), 'id', 'status', 'start', 'end')
    job = _instantiate_job(jid, status, start, end, workerIP)
    if job:
        job['status'] = newstatus
        _save_job(_generate_job_key(jid), job)
    else:
        raise Exception()
