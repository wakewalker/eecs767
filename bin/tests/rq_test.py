'''Start an rq worker, before run this script by running the following command:
    rq worker
'''

from  time import sleep
from rq import Queue
from rq.job import Job
from redis import Redis
from tokenizer import count_words_at_url

redis_conn = Redis()
q = Queue(connection=redis_conn)

jobs = []
for i in range(100):
    job = q.enqueue(count_words_at_url, 'http://python-rq.org/docs/')
    jobs.append(job)
#    print job.result

sleep(10)
#print job.result

for job in jobs:
    #    job = Job().fetch(job_id, connection=redis_conn)
    print '%s: %s' % (job.get_id(), job.result)
