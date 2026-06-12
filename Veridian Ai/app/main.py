from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload

# Create FastAPI app
app = FastAPI(
    title="Veridian AI - Carbon Compliance Automation",
    description="API for automated invoice processing and carbon compliance",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Veridian AI",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    return {
        "message": "Welcome to Veridian AI - Carbon Compliance Automation API",
        "docs": "/docs",
        "redoc": "/redoc"
    }