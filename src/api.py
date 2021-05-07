from flask import Flask, request, send_file
import json
from hotqueue import HotQueue
import redis
import os


redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
  raise Exception()


app = Flask(__name__)
rd = redis.StrictRedis(host=redis_ip, port=6413, db=0)  # db=0 for database
q = HotQueue('queue', host=redis_ip, port=6413, db=1)   # db=1 for queue


# v--- routes ---v

@app.route('/', methods=['GET'])
def info():
  return """
  Routes:

  /		info
  /loaddata	load data into Redis DB (not functional)

"""





if __name__=='__main__':
  app.run(debug=True, host='0.0.0.0')
