from datetime import datetime
import feedparser
import httpx
from sqlalchemy.exc import IntegrityError

from .config import settings
from .db import SessionLocal, Opportunity
from .matcher import score_text

def _parse_dt(value: str | None):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)
    except Exception:
        return None

def ingest_once() -> dict:
    if not settings.placsp_atom_url:
        return {"ok": False, "reason": "PLACSP_ATOM_URL not configured", "inserted": 0}

    with httpx.Client(timeout=60, follow_redirects=True) as client:
        response = client.get(settings.placsp_atom_url)
        response.raise_for_status()

    feed = feedparser.parse(response.content)
    inserted = 0
    considered = 0

    with SessionLocal() as db:
        for entry in feed.entries:
            title = getattr(entry, "title", "") or ""
            summary = getattr(entry, "summary", "") or ""
            link = getattr(entry, "link", "") or ""
            external_id = getattr(entry, "id", "") or link or title
            published = getattr(entry, "published", None) or getattr(entry, "updated", None)

            score, matched = score_text(f"{title}\n{summary}", settings.keywords)
            if score < settings.min_score:
                continue

            considered += 1
            row = Opportunity(
                external_id=external_id,
                title=title[:5000],
                summary=summary[:20000],
                url=link[:5000],
                published_at=_parse_dt(published),
                score=score,
                matched_keywords=",".join(matched),
            )
            db.add(row)
            try:
                db.commit()
                inserted += 1
            except IntegrityError:
                db.rollback()

    return {
        "ok": True,
        "feed_entries": len(feed.entries),
        "considered": considered,
        "inserted": inserted,
    }
