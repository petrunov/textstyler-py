import os
import sys
import time

from fastapi.testclient import TestClient

from app.main import app
from app.state import cache, jobs

client = TestClient(app)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_improve_text_valid():
    # Clear cache to ensure test isolation
    cache.clear()
    text = "I has a apple"
    # First call should process and cache the result
    response = client.get(f"/improve?text={text.replace(' ', '+')}")
    assert response.status_code == 200
    data = response.json()
    assert "Improved:" in data["improved_text"]
    first_result = data["improved_text"]

    # The cache should now contain the text
    assert text in cache

    # Second call should return the cached result
    response2 = client.get(f"/improve?text={text.replace(' ', '+')}")
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["improved_text"] == first_result


def test_improve_text_missing_param():
    # GET /improve without the required 'text' query parameter
    # Should return 422 (validation error)
    response = client.get("/improve")
    assert response.status_code == 422


def test_improve_async_valid():
    # Clear cache and jobs for test isolation
    cache.clear()
    jobs.clear()
    text = "I has a apple"
    response = client.post("/improve-async", json={"text": text})
    assert response.status_code == 200
    data = response.json()
    job_id = data.get("job_id")
    assert job_id is not None

    # Poll the job status until it is done (or timeout after a few iterations)
    max_attempts = 10
    for _ in range(max_attempts):
        job_response = client.get(f"/job-status/{job_id}")
        if job_response.json().get("status") == "done":
            break
        time.sleep(0.5)
    job_data = job_response.json()
    assert job_data["status"] == "done"
    assert "Improved:" in job_data["result"]


def test_improve_async_missing_text():
    # POST /improve-async without 'text' should trigger a validation error (422)
    response = client.post("/improve-async", json={})
    assert response.status_code == 422


def test_job_status_not_found():
    # Non-existent job ID should return 404
    response = client.get("/job-status/non-existent-job-id")
    assert response.status_code == 404
