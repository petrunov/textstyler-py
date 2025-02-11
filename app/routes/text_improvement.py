from fastapi import APIRouter, BackgroundTasks, HTTPException, Query
from pydantic import BaseModel, field_validator

from app.state import cache, jobs

router = APIRouter()


class ImprovementRequest(BaseModel):
    text: str

    @field_validator("text")
    def text_must_have_valid_length(cls, v):
        # Check for non-empty/whitespace
        if not v or not v.strip():
            raise ValueError("Text must not be empty or whitespace.")
        # Enforce length constraints
        stripped = v.strip()
        if not (5 <= len(stripped) <= 1000):
            raise ValueError("Text length must be between 5 and 1000 characters.")
        return stripped


@router.get("/improve")
async def improve_text(text: str = Query(..., min_length=5, max_length=1000)):
    if not text.strip():
        raise HTTPException(
            status_code=422, detail="Text must not be empty or whitespace."
        )
    """
    GET endpoint that receives text as a query parameter.
    Returns JSON with the improved text.
    """
    # Lazy import: import the function when the endpoint is called.
    # This allows for monkey patching in the test suite.
    from app.services.llm import llm_improvement

    if text in cache:
        return {"improved_text": cache[text]}

    improved_text = await llm_improvement(text)
    cache[text] = improved_text
    return {"improved_text": improved_text}


@router.post("/improve-async")
async def improve_async(request: ImprovementRequest, background_tasks: BackgroundTasks):
    """
    POST endpoint to submit a text improvement job asynchronously.
    Returns a job ID that can be used to check the job status.
    """
    from app.services.jobs import create_job, process_job

    job_id = create_job(request.text)
    background_tasks.add_task(process_job, job_id)
    return {"job_id": job_id}


@router.get("/job-status/{job_id}")
async def job_status(job_id: str):
    """
    GET endpoint to retrieve the status of an asynchronous job.
    """
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job["status"] == "error":
        return {"status": "error", "result": job["result"]}

    return job
