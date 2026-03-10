from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import date
import csv
import io
from sqlalchemy.orm import Session
from models import MoodEntry, engine
from ai_service import analyze_patterns, generate_insights

router = APIRouter()

# ---------------------------------------------------------------------------
# Dependency – provide a DB session per request
# ---------------------------------------------------------------------------
from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------
class EntryCreate(BaseModel):
    date: date = Field(..., description="ISO8601 date of the entry")
    emoji: str = Field(..., description="Unicode emoji character")
    note: Optional[str] = Field(None, max_length=255, description="Optional short note")

    @validator("emoji")
    def emoji_must_be_nonempty(cls, v):
        if not v:
            raise ValueError("emoji cannot be empty")
        return v

class EntryResponse(BaseModel):
    id: str
    date: date
    emoji: str
    note: Optional[str] = None

    class Config:
        orm_mode = True

class AnalyzeRequest(BaseModel):
    days: int = Field(..., ge=7, le=30, description="Number of days to analyse (7‑30)")
    pattern_type: str = Field(..., description="Pattern type, e.g., weekly_trend")

class InsightsRequest(BaseModel):
    days: int = Field(..., ge=7, le=30)
    focus: str = Field(..., description="Insight focus, e.g., recommendations")

# ---------------------------------------------------------------------------
# Mood entry endpoints
# ---------------------------------------------------------------------------
@router.post("/entries", response_model=EntryResponse, status_code=201)
def create_entry(entry: EntryCreate, db: Session = Depends(get_db)):
    db_entry = MoodEntry(date=entry.date, emoji=entry.emoji, note=entry.note)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.get("/entries", response_model=List[EntryResponse])
def list_entries(db: Session = Depends(get_db)):
    entries = db.query(MoodEntry).order_by(MoodEntry.date.desc()).all()
    return entries

@router.get("/entries/export")
def export_entries(start_date: Optional[date] = Query(None), end_date: Optional[date] = Query(None), db: Session = Depends(get_db)):
    query = db.query(MoodEntry)
    if start_date:
        query = query.filter(MoodEntry.date >= start_date)
    if end_date:
        query = query.filter(MoodEntry.date <= end_date)
    rows = query.order_by(MoodEntry.date).all()

    def generate():
        output = io.StringIO()
        writer = csv.writer(output)
        # Header
        writer.writerow(["id", "date", "emoji", "note"])
        yield output.getvalue()
        output.seek(0)
        output.truncate(0)
        for row in rows:
            writer.writerow([str(row.id), row.date.isoformat(), row.emoji, row.note or ""])
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)

    filename = f"mood_entries_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.csv"
    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"'
    }
    return StreamingResponse(generate(), media_type="text/csv", headers=headers)

# ---------------------------------------------------------------------------
# AI‑powered endpoints (premium)
# ---------------------------------------------------------------------------
@router.post("/ai/analyze-patterns")
async def ai_analyze_patterns(request: AnalyzeRequest):
    # Build a simple message payload for the model
    messages = [
        {"role": "system", "content": "You are a mood‑pattern analysis assistant."},
        {"role": "user", "content": f"Analyze a {request.pattern_type} over the past {request.days} days based on mood emojis."}
    ]
    result = await analyze_patterns(messages)
    return {"status": "success", "analysis": result}

@router.post("/ai/generate-insights")
async def ai_generate_insights(request: InsightsRequest):
    messages = [
        {"role": "system", "content": "You are a personal‑wellness insight generator."},
        {"role": "user", "content": f"Provide {request.focus} based on the last {request.days} days of mood entries."}
    ]
    result = await generate_insights(messages)
    return {"status": "success", "insights": result}
