from destruction.caesar import caesar
from destruction.wordscore import score_text

def brute_caesar(text: str):
    results = []
    for i in range(26):
        cand = caesar(text, i)
        results.append((score_text(cand), i, cand))
    return sorted(results, reverse=True)
