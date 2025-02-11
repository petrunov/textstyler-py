from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, field_validator
from app.state import cache, jobs
from app.services.llm import simulate_llm_improvement
from app.services.jobs import create_job, process_job  

router = APIRouter()

class ImprovementRequest(BaseModel):
    text: str

@field_validator("text")
def text_must_not_be_empty(cls, v):
    if not v or not v.strip():
        raise ValueError("Text must not be empty or whitespace.")
    return v

@router.get("/improve")
async def improve_text(text: str):
    """
    GET endpoint that receives text as a query parameter and returns JSON with the improved text.
    """
    if text in cache:
        return {"improved_text": cache[text]}

    improved_text = await simulate_llm_improvement(text)
    cache[text] = improved_text
    return {"improved_text": improved_text}

@router.post("/improve-async")
async def improve_async(request: ImprovementRequest, background_tasks: BackgroundTasks):
    """
    POST endpoint to submit a text improvement job asynchronously.
    Returns a job ID that can be used to check the job status.
    """
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
