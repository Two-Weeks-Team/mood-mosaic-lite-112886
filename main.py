import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from routes import router
from models import Base, engine

# Create tables if they do not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mood Mosaic Lite API", version="0.1.0")

app.include_router(router, prefix="/api")

@app.get("/health", response_model=dict)
def health_check():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
def root():
    html = """
    <html>
    <head>
        <title>Mood Mosaic Lite Backend</title>
        <style>
            body { background-color: #0d1117; color: #c9d1d9; font-family: Arial, Helvetica, sans-serif; padding: 2rem; }
            h1 { color: #58a6ff; }
            a { color: #58a6ff; }
            .endpoint { margin-bottom: 1rem; }
            .section { margin-top: 2rem; }
        </style>
    </head>
    <body>
        <h1>🌈 Mood Mosaic Lite - Backend</h1>
        <p>One‑click daily mood logging with heat‑map visualisation.</p>
        <div class="section">
            <h2>Available Endpoints</h2>
            <div class="endpoint"><strong>GET</strong> <code>/health</code> – health check.</div>
            <div class="endpoint"><strong>POST</strong> <code>/api/entries</code> – create a mood entry.</div>
            <div class="endpoint"><strong>GET</strong> <code>/api/entries</code> – list all entries.</div>
            <div class="endpoint"><strong>GET</strong> <code>/api/entries/export</code> – download CSV export.</div>
            <div class="endpoint"><strong>POST</strong> <code>/api/ai/analyze-patterns</code> – AI pattern detection (premium).</div>
            <div class="endpoint"><strong>POST</strong> <code>/api/ai/generate-insights</code> – AI‑driven personal insights (premium).</div>
        </div>
        <div class="section">
            <h2>Tech Stack</h2>
            <ul>
                <li>FastAPI 0.115.0</li>
                <li>Uvicorn 0.30.0</li>
                <li>SQLAlchemy 2.0.35 (PostgreSQL)</li>
                <li>DigitalOcean Serverless Inference (openai-gpt-oss-120b)</li>
                <li>Python 3.12</li>
            </ul>
        </div>
        <div class="section">
            <p>API docs: <a href="/docs">/docs</a> | <a href="/redoc">/redoc</a></p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html, status_code=200)
