# Text Styler API

The **Text Styler API** is a service that enhances text using simulated large language model (LLM) integrations. It provides both synchronous and asynchronous endpoints, making it easy to improve text either instantly or as part of background job processing. With caching and background processing support, it ensures efficient and scalable performance.

## Features 🚀

- **/improve**: Synchronous endpoint that receives a text query parameter and returns the improved text.
- **/improve-async**: Asynchronous endpoint that processes text improvement jobs in the background.
- **/job-status/{job_id}**: Endpoint to check the status of a submitted asynchronous job.

## Setup 🛠️

### Clone the repository

```bash
git clone https://github.com/petrunov/textstyler-py
cd textstyler-py
```

### Create and Activate a Virtual Environment

1. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

2. On **macOS/Linux**, activate it:

   ```bash
   source .venv/bin/activate
   ```

3. On **Windows**, activate it:
   ```bash
   .venv\Scripts\activate
   ```

### Install Dependencies

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Examples 💻

### Synchronous Text Improvement

Run a cURL request to improve text synchronously:

```bash
curl "http://127.0.0.1:8000/improve?text=I+has+a+apple"
```

This will return a JSON response with the improved text.

### Asynchronous Job Submission

Submit a job for text improvement:

```bash
curl -X POST "http://127.0.0.1:8000/improve-async" -H "Content-Type: application/json" -d '{"text": "I has a apple"}'
```

The response will contain a `job_id`.

### Check Job Status

Once you have a `job_id`, you can check the status of the job by visiting the following URL:

```bash
http://127.0.0.1:8000/job-status/<job_id>
```

Replace `<job_id>` with the actual job ID returned from the asynchronous request.

## Running Unit Tests 🧪

Unit tests are written using **pytest-asyncio** and **httpx's AsyncClient** for asynchronous testing. To run the tests:

1. Ensure your virtual environment is activated.
2. Run the tests with:

   ```bash
   pytest
   ```

   Or to run a specific test file:

   ```bash
   pytest tests/test_main_async.py
   ```

### What the Tests Cover

- **Endpoint Functionality**:

  - Verifies that the `/improve` endpoint correctly processes valid text.
  - Ensures caching is used to avoid duplicate LLM calls.
  - Validates error responses (e.g., 422 for missing parameters).

- **Asynchronous Job Processing**:

  - Simulates asynchronous LLM calls by monkey-patching the LLM functions.
  - Ensures jobs are queued and processed correctly.
  - Validates that the job status endpoint returns accurate results.

- **Error Conditions**:
  - Covers scenarios such as missing query parameters or non-existent job IDs.
  - Ensures appropriate HTTP error codes (422 for missing parameters, 404 for non-existent jobs).

## Code Quality and Linting 🧑‍💻

To ensure consistent code quality, the following tools are integrated into the project:

- **Black**: Automatic code formatting.
- **Flake8**: Linting to catch common style issues.
- **isort**: Consistent import ordering.
- **Pre-commit Hooks**: Automatically run these tools before commits (configured in `.pre-commit-config.yaml`).

### Running Code Quality Checks

To manually run the tools:

- **Black**:

  ```bash
  black .
  ```

- **Flake8**:

  ```bash
  flake8 .
  ```

- **isort**:
  ```bash
  isort .
  ```

## Additional Information 📝

### Lazy Imports for Testability

Key dependency imports (such as LLM functions) are performed lazily within endpoint functions. This helps improve testability and decouples external dependencies.

### Future Improvements

- Replace the in-memory cache with a persistent solution like **Redis** for better scalability.
- Integrate a robust task queue system (e.g., **Celery**) for production-grade asynchronous job processing.
- Update validators to ensure compatibility with future versions of **Pydantic**.

## License 📄

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for more details.
