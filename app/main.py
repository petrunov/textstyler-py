from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from app.state import cache, jobs
from app.services.llm import simulate_llm_improvement
from app.jobs import create_job, process_job

app = FastAPI()

class ImprovementRequest(BaseModel):
    text: str

@app.get("/improve")
async def improve_text(text: str):
    """
    GET endpoint that receives text as a query parameter and returns JSON
    with the improved text.
    """
    if text in cache:
        return {"improved_text": cache[text]}
    
    improved_text = await simulate_llm_improvement(text)
    cache[text] = improved_text
    return {"improved_text": improved_text}

@app.post("/improve-async")
async def improve_async(request: ImprovementRequest, background_tasks: BackgroundTasks):
    """
    POST endpoint to submit a text improvement job asynchronously.
    Returns a job ID that can be used to check the job status.
    """
    job_id = create_job(request.text)
    background_tasks.add_task(process_job, job_id)
    return {"job_id": job_id}

@app.get("/job-status/{job_id}")
async def job_status(job_id: str):
    """
    GET endpoint to retrieve the status of an asynchronous job.
    """
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
