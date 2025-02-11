import uuid
from app.state import cache, jobs
from app.services.llm import simulate_llm_improvement_sync

def create_job(text: str) -> str:
    """
    Create a new job with a unique ID.
    """
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "queued", "result": None, "text": text}
    return job_id

def process_job(job_id: str):
    """
    Process a job: update its status, perform the LLM improvement (checking the cache first),
    and then update the job store.
    """
    job = jobs.get(job_id)
    if not job:
        return  # log or handle this case

    text = job["text"]
    jobs[job_id]["status"] = "processing"

    if text in cache:
        result = cache[text]
    else:
        result = simulate_llm_improvement_sync(text)
        cache[text] = result

    jobs[job_id]["result"] = result
    jobs[job_id]["status"] = "done"
