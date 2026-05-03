"""
server.py — Lightweight backend that serves the frontend
and proxies requests to the FST API (running on port 8000).

Run:
    uvicorn server:app --reload --port 3000
"""
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Pullinguistics Website")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")

# Serve index.html at root
@app.get("/")
async def root():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

# Serve all static assets (css, js, images)
app.mount("/", StaticFiles(directory=FRONTEND_DIR), name="static")
