import logging
import uuid

from app.services.llm import simulate_llm_improvement_sync
from app.state import cache, jobs

logger = logging.getLogger(__name__)


def create_job(text: str) -> str:
    """
    Create a new job with a unique ID.
    """
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "queued", "result": None, "text": text}
    return job_id


def process_job(job_id: str):
    """
    Process a job: update its status, perform the LLM improvement (checking the
    cache first), and update the job store. If an error occurs, update status to
    "error" and log the exception.
    """
    job = jobs.get(job_id)
    if not job:
        logger.error(f"Job {job_id} not found during processing.")
        return

    text = job["text"]
    jobs[job_id]["status"] = "processing"

    try:
        if text in cache:
            result = cache[text]
        else:
            result = simulate_llm_improvement_sync(text)
            cache[text] = result

        jobs[job_id]["result"] = result
        jobs[job_id]["status"] = "done"
    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["result"] = f"Processing error: {e}"
        logger.exception(f"Error processing job {job_id}: {e}")
