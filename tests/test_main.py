from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_improve_text():
    response = client.get("/improve?text=I+has+a+apple")
    assert response.status_code == 200
    data = response.json()
    assert "Improved:" in data["improved_text"]

def test_improve_async_and_job_status():
    # Submit an asynchronous job
    response = client.post("/improve-async", json={"text": "I has a apple"})
    assert response.status_code == 200
    data = response.json()
    job_id = data["job_id"]
    assert job_id is not None

    # Wait a bit for the background task to complete (simulate the processing delay)
    import time
    time.sleep(3)

    # Now check the job status
    response = client.get(f"/job-status/{job_id}")
    assert response.status_code == 200
    job_data = response.json()
    assert job_data["status"] == "done"
    assert "Improved:" in job_data["result"]

def test_job_status_not_found():
    response = client.get("/job-status/non-existent-job-id")
    assert response.status_code == 404
