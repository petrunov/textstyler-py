# In‑memory cache for improved texts: { original_text: improved_text }
cache = {}

# In‑memory job store for asynchronous processing:
# { job_id: { "status": "queued|processing|done", "result": Optional[str], "text": original_text } }
jobs = {}
