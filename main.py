from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import form_extraction, auth_requests
from app.core.config import settings
from starlette.requests import Request

app = FastAPI(
    title="Prior Auth Copilot API",
    description="API for automated medical prior authorization form filling",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(form_extraction.router, prefix="/api/v1", tags=["form-extraction"])
app.include_router(auth_requests.router, prefix="/api/v1/auth-requests", tags=["authorization-requests"])

@app.middleware("http")
async def log_headers(request: Request, call_next):
    print("Incoming headers:", dict(request.headers))
    response = await call_next(request)
    return response

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
