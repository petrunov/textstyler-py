import asyncio
import os
import sys

import httpx
import pytest
from asgi_lifespan import LifespanManager

from app.main import app
from app.state import cache, jobs

# Ensure the project root is on sys.path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Fake implementations for testing
async def fake_llm_improvement_async(text: str) -> str:
    # A corrected version of the text
    return f"Improved: {text.replace('I has', 'I have')}"


def fake_llm_improvement_sync(text: str) -> str:
    return f"Improved: {text.replace('I has', 'I have')}"


@pytest.mark.asyncio
async def test_improve_text_valid(monkeypatch):
    # Clear cache
    cache.clear()
    text = "I has a apple"

    # Patch the async LLM function (lazy import in the endpoint picks this up)
    monkeypatch.setattr("app.services.llm.llm_improvement", fake_llm_improvement_async)

    async with LifespanManager(app):
        async with httpx.AsyncClient(app=app, base_url="http://test") as client:
            # First call: process and cache the result
            response = await client.get(f"/improve?text={text.replace(' ', '+')}")
            assert response.status_code == 200
            data = response.json()
            assert "Improved:" in data["improved_text"]
            first_result = data["improved_text"]

            # Verify the cache has been updated
            assert text in cache

            # Second call should return the cached result
            response2 = await client.get(f"/improve?text={text.replace(' ', '+')}")
            assert response2.status_code == 200
            data2 = response2.json()
            assert data2["improved_text"] == first_result


@pytest.mark.asyncio
async def test_improve_text_missing_param():
    async with LifespanManager(app):
        async with httpx.AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/improve")
            # Expecting a 422 validation error because 'text' query parameter is missing
            assert response.status_code == 422


@pytest.mark.asyncio
async def test_improve_async_valid(monkeypatch):
    # Clear cache and job store for test isolation
    cache.clear()
    jobs.clear()
    text = "I has a apple"

    # Patch the synchronous LLM function used by the async job processor.
    monkeypatch.setattr(
        "app.services.llm.llm_improvement_sync", fake_llm_improvement_sync
    )

    async with LifespanManager(app):
        async with httpx.AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/improve-async", json={"text": text})
            assert response.status_code == 200
            data = response.json()
            job_id = data.get("job_id")
            assert job_id is not None

            # Poll for job completion (up to 10 attempts, 0.5 sec interval)
            for _ in range(10):
                job_response = await client.get(f"/job-status/{job_id}")
                if job_response.json().get("status") == "done":
                    break
                await asyncio.sleep(0.5)
            job_data = job_response.json()
            assert job_data["status"] == "done"
            assert "Improved:" in job_data["result"]


@pytest.mark.asyncio
async def test_improve_async_missing_text():
    async with LifespanManager(app):
        async with httpx.AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/improve-async", json={})
            # Expecting a 422 validation error because 'text' is missing
            assert response.status_code == 422


@pytest.mark.asyncio
async def test_job_status_not_found():
    async with LifespanManager(app):
        async with httpx.AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/job-status/non-existent-job-id")
            assert response.status_code == 404
