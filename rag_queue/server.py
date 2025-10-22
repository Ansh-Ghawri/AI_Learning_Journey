from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Query
from.client.rq_client import queue
from .queues.worker import process_query

app = FastAPI()

@app.get('/')
def root():
    return {"status": "Server is up and running"}



@app.post('/chat')
def chat(
    query: str = Query(..., description="The query string to process")
):
    job = queue.enqueue(process_query, query)
    return {"status": "Job enqueued", "job_id": job.id}


# NOTE:
# To resolve multithreading issues with RQ workers (on MacOS):
# run:  export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
# then can run the worker command: rq worker --with-scheduler


# dc9f93c1-9998-4826-962e-5d00910fdb73  ,  42eb5b64-b950-4fde-82f6-bbfd4d88ccb8
@app.get('/job-status')
def get_result(
        job_id: str = Query(..., description="The ID of the job to check")
    ):
        job = queue.fetch_job(job_id)
        result = job.return_value()

        return {"result": result}
