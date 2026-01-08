"""Main FastAPI application entry point."""
import logging
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.controllers import auth, family_members, medications, medication_usage, google_drive, google_calendar, n8n_controller


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout,
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="LifeLine API",
    description="Family Health Tracking Application API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

logger.info("LifeLine API is starting up...")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(family_members.router, prefix="/family-members", tags=["Family Members"])
app.include_router(medications.router, prefix="/medications", tags=["Medications"])
app.include_router(medication_usage.router, prefix="/medication-usage", tags=["Medication Usage"])
app.include_router(google_drive.router, prefix="/drive", tags=["Google Drive"])
app.include_router(google_calendar.router, prefix="/calendar", tags=["Google Calendar"])
app.include_router(n8n_controller.router, prefix="/n8n", tags=["N8N"])



@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "LifeLine API", "version": "1.o.o"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

