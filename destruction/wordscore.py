COMMON_WORDS = {
    "THE", "AND", "TO", "OF", "IS", "IN", "THAT", "IT", "FOR", "ON",
    "IL", "LO", "LA", "DI", "CHE", "E", "UN", "UNA",
}


def word_score(text: str) -> int:
    text = text.upper()
    return sum(1 for w in COMMON_WORDS if w in text)
