# Text Styler API

This project implements an API that improves text using a simulated LLM integration. It provides both synchronous and asynchronous endpoints with caching and background processing.

## Features

- **/improve**: Synchronous endpoint that receives a `text` query parameter and returns the improved text.
- **/improve-async**: Asynchronous endpoint to process text improvement jobs in the background.
- **/job-status/{job_id}**: Endpoint to check the status of a submitted job.

## Setup

1. **Clone the repository and change into the directory:**

   ```bash
   git clone https://github.com/your-username/llm-text-improvement.git
   cd llm-text-improvement
   ```

## Examples

1. **Run a cURL request that should return a json response with a job id**

   ```bash
   curl -X POST "http://127.0.0.1:8000/improve-async"
   -H "Content-Type: application/json"      -d '{"text": "I has a apple"}'
   ```

2. **Use the returned job id from the response in your browser http://127.0.0.1:8000/job-status/<job_id>**
