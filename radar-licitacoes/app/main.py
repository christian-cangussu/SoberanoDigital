from fastapi import FastAPI, Query
from sqlalchemy import select

from .db import init_db, SessionLocal, Opportunity
from .ingest import ingest_once

app = FastAPI(title="Radar Licitações MVP", version="0.1.0")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/ingest")
def ingest():
    return ingest_once()

@app.get("/opportunities")
def opportunities(
    min_score: int = Query(0, ge=0, le=100),
    limit: int = Query(50, ge=1, le=500),
):
    with SessionLocal() as db:
        rows = db.execute(
            select(Opportunity)
            .where(Opportunity.score >= min_score)
            .order_by(Opportunity.published_at.desc().nullslast(), Opportunity.id.desc())
            .limit(limit)
        ).scalars().all()

        return [
            {
                "id": r.id,
                "title": r.title,
                "summary": r.summary,
                "url": r.url,
                "published_at": r.published_at,
                "score": r.score,
                "matched_keywords": r.matched_keywords.split(",") if r.matched_keywords else [],
            }
            for r in rows
        ]
