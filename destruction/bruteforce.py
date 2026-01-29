from .caesar import caesar
from .langdetect import detect_language_score
from .wordscore import word_score


def brute_force_caesar(text: str, top: int = 5):
    """
    Try all 26 Caesar shifts and rank by language likelihood.
    Returns list of (shift, text, score).
    """
    results = []

    for shift in range(26):
        decoded = caesar(text, shift)
        score = detect_language_score(decoded) + word_score(decoded) * 10
        results.append((shift, decoded, score))

    results.sort(key=lambda x: x[2], reverse=True)
    return results[:top]
