# DASHBOARD_BACKEND/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from starlette.applications import Starlette # Not used, can be removed
# from starlette.routing import Mount       # Not used, can be removed
import uvicorn
import os
import re # 🚨 FIX 1: Must import 're' for regex to work!

# Import the standalone QC API application instance
from qc_api import qc_router

# Import the Dashboard routes APIRouter
from app.dashboard_routes import dashboard_router 

# --- CONFIGURATIONS ---

master_app = FastAPI(
    title="Master Data Processing & Dashboard API",
    version="2.0.0"
)

# 1. CORS Middleware (Applied to the master app)

# Define a list of allowed origins, including static ones.
# 🚨 FIX 2: We must dynamically inject the current deployment URL from the environment,
# OR use a temporary wildcard solution.
# We will use an environment variable for the CURRENT Vercel deployment URL.

# Get the current dynamic Vercel URL from an environment variable (set this on Render!)
VERCEL_DEPLOYMENT_URL = os.getenv("VERCEL_DEPLOYMENT_URL") 
# Example: VERCEL_DEPLOYMENT_URL=https://pm-aqt9-l1fdp88vu-bharath-raj-g-sources-projects.vercel.app

origins = [
    "http://localhost:3000",                 
    "https://pm-aqt9.vercel.app", # The stable Vercel domain
]

# Add the current dynamic URL if it's set
if VERCEL_DEPLOYMENT_URL:
    # Use re.match to validate it's actually a Vercel URL before adding it (for security)
    if re.match(r"^https:\/\/[a-zA-Z0-9-]+\.vercel\.app$", VERCEL_DEPLOYMENT_URL):
        origins.append(VERCEL_DEPLOYMENT_URL)
    
master_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Now uses the dynamically built list
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"], 
    allow_headers=["*"],
)

# --- ROUTING/MOUNTING ---
    
# 1. Include the QC API Router
master_app.include_router(qc_router, prefix="/api/qc", tags=["QC Automation"])

# 2. Include the Dashboard Router
master_app.include_router(dashboard_router)

# --- SERVER ---
PORT = int(os.getenv("PORT", 8000))

if __name__ == "__main__":
    uvicorn.run(master_app, host="0.0.0.0", port=PORT)