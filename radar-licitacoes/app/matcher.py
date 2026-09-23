def score_text(text: str, keywords: list[str]) -> tuple[int, list[str]]:
    haystack = (text or "").lower()
    matched = [kw for kw in keywords if kw in haystack]
    # MVP heuristic: each keyword hit = 20 points, capped at 100.
    return min(100, len(matched) * 20), matched
