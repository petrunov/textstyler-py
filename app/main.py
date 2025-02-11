import logging

from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from starlette.responses import JSONResponse

from app.routes.text_improvement import router as text_router

# Set up basic logging.
logging.basicConfig(level=logging.INFO)

# Set up a rate limiter that uses the remote address.
limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter

app.add_middleware(SlowAPIMiddleware)


# Register a rate limit exceeded exception handler.
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please try again later."},
    )


# Include the API router.
app.include_router(text_router)
