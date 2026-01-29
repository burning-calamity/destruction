# letter frequency (English + Romance mix)
FREQ = {
    "E": 12.0, "T": 9.1, "A": 8.1, "O": 7.6, "I": 7.3,
    "N": 7.0, "R": 6.0, "S": 6.3, "L": 4.0,
}


def detect_language_score(text: str) -> float:
    """
    Very lightweight language detection via letter frequency.
    Higher = more language-like.
    """
    score = 0.0
    total = 0

    for ch in text.upper():
        if "A" <= ch <= "Z":
            total += 1
            score += FREQ.get(ch, 0)

    if total == 0:
        return 0.0

    return score / total
