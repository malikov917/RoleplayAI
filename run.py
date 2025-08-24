#!/usr/bin/env python3
"""
AI Roleplay Trainer - Entry point

This script starts the FastAPI application server.
"""

import uvicorn
from main import app
from config import settings

if __name__ == "__main__":
    print(f"Starting {settings.APP_NAME}...")
    print(f"Debug mode: {settings.DEBUG}")
    print(f"Supabase URL: {settings.SUPABASE_URL}")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info" if not settings.DEBUG else "debug"
    )