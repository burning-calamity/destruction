# destruction/transliterate.py

from __future__ import annotations

# ---------------- core transliteration maps ----------------

GREEK = {
    "α":"a","β":"b","γ":"g","δ":"d","ε":"e","ζ":"z","η":"i","θ":"th",
    "ι":"i","κ":"k","λ":"l","μ":"m","ν":"n","ξ":"x","ο":"o","π":"p",
    "ρ":"r","σ":"s","ς":"s","τ":"t","υ":"y","φ":"f","χ":"ch","ψ":"ps","ω":"o",
}

CYRILLIC = {
    "а":"a","б":"b","в":"v","г":"g","д":"d","е":"e","ё":"yo","ж":"zh",
    "з":"z","и":"i","й":"y","к":"k","л":"l","м":"m","н":"n","о":"o",
    "п":"p","р":"r","с":"s","т":"t","у":"u","ф":"f","х":"kh","ц":"ts",
    "ч":"ch","ш":"sh","щ":"shch","ы":"y","э":"e","ю":"yu","я":"ya",
}

ARABIC = {
    "ا":"a","ب":"b","ت":"t","ث":"th","ج":"j","ح":"h","خ":"kh",
    "د":"d","ذ":"dh","ر":"r","ز":"z","س":"s","ش":"sh","ص":"s",
    "ض":"d","ط":"t","ظ":"z","ع":"a","غ":"gh","ف":"f","ق":"q",
    "ك":"k","ل":"l","م":"m","ن":"n","ه":"h","و":"w","ي":"y",
}

HEBREW = {
    "א":"a","ב":"b","ג":"g","ד":"d","ה":"h","ו":"v","ז":"z",
    "ח":"h","ט":"t","י":"y","כ":"k","ל":"l","מ":"m","נ":"n",
    "ס":"s","ע":"a","פ":"p","צ":"ts","ק":"q","ר":"r","ש":"sh","ת":"t",
}

JAPANESE = {
    "あ":"a","い":"i","う":"u","え":"e","お":"o",
    "か":"ka","き":"ki","く":"ku","け":"ke","こ":"ko",
    "さ":"sa","し":"shi","す":"su","せ":"se","そ":"so",
    "ん":"n",
}

# ---------------- registry ----------------

SCRIPTS = {
    "greek": GREEK,
    "cyrillic": CYRILLIC,
    "arabic": ARABIC,
    "hebrew": HEBREW,
    "japanese": JAPANESE,
}

# ---------------- auto detection ----------------

def _detect_script(ch: str) -> str | None:
    code = ord(ch)
    if 0x0370 <= code <= 0x03FF:
        return "greek"
    if 0x0400 <= code <= 0x04FF:
        return "cyrillic"
    if 0x0600 <= code <= 0x06FF:
        return "arabic"
    if 0x0590 <= code <= 0x05FF:
        return "hebrew"
    if 0x3040 <= code <= 0x309F:
        return "japanese"
    return None

# ---------------- public API ----------------

def transliterate(text: str, target: str = "latin") -> str:
    """
    Universal transliteration to Latin.
    """
    out = []
    for ch in text:
        script = _detect_script(ch.lower())
        if script and script in SCRIPTS:
            out.append(SCRIPTS[script].get(ch.lower(), ch))
        else:
            out.append(ch)
    return "".join(out)


transliterate.__call__ = transliterate
