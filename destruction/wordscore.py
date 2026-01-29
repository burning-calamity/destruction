
from __future__ import annotations

# ---- language word banks (uppercase) ----
# Keep words short/common to reduce false negatives.

WORD_BANKS = {
    "EN": {
        "THE","AND","TO","OF","IS","IN","THAT","IT","FOR","ON","WITH","AS","ARE","WAS",
        "BE","BY","THIS","FROM","OR","AN","AT","NOT","HAVE","HAS","YOU","YOUR","WE",
        "THEY","THEIR","I","ME","MY","HE","SHE","HIS","HER","WHAT","WHEN","WHERE",
        "WHY","HOW","ALL","ANY","SOME","NO","YES","DO","DID","DONE","CAN","COULD",
        "WOULD","SHOULD","IF","ELSE","THEN","THERE","HERE","WHO","WHOM","WHICH"
    },
    "IT": {
        "IL","LO","LA","I","GLI","LE","UN","UNO","UNA","DI","A","DA","IN","CON","SU",
        "PER","TRA","FRA","CHE","E","O","MA","NON","SI","NO","PIU","MENO","ANCHE",
        "COME","QUANDO","DOVE","PERCHE","QUESTO","QUELLO","ESSERE","AVERE","SONO",
        "ERA","ERANO","HO","HA","HANNO","MIO","MIA","TUO","SUA","LORO","NOI","VOI"
    },
    "FR": {
        "LE","LA","LES","UN","UNE","DES","DE","DU","ET","OU","MAIS","PAS","EST","EN",
        "DANS","POUR","SUR","AVEC","CE","CET","CETTE","CES","QUI","QUE","QUOI",
        "QUAND","OU","POURQUOI","COMMENT","JE","TU","IL","ELLE","NOUS","VOUS","ILS",
        "ELLES","SON","SA","SES","AVOIR","ETRE","AI","A","ONT","ETAIT"
    },
    "ES": {
        "EL","LA","LOS","LAS","UN","UNA","DE","DEL","Y","O","PERO","NO","SI","ES",
        "EN","CON","POR","PARA","QUE","QUI","CUANDO","DONDE","PORQUE","COMO",
        "YO","TU","ELLA","NOSOTROS","USTED","ELLOS","SU","SUS","MI","MIS","ERA"
    },
    "DE": {
        "DER","DIE","DAS","UND","ODER","ABER","NICHT","IST","SIND","WAR","IM","IN",
        "MIT","ZU","VON","FUR","AUF","DASS","WER","WAS","WANN","WO","WARUM","ICH",
        "DU","ER","SIE","WIR","IHR","SEIN","HABEN","HAT","HATTEN"
    },
    "PT": {
        "O","A","OS","AS","UM","UMA","DE","DO","DA","E","OU","MAS","NAO","SIM","EM",
        "COM","PARA","POR","QUE","QUANDO","ONDE","PORQUE","COMO","EU","VOCE",
        "ELE","ELA","NOS","ELES","SEU","SUA","ERA"
    },
    "NL": {
        "DE","HET","EEN","EN","OF","MAAR","NIET","IS","IN","MET","VOOR","OP","DAT",
        "WIE","WAT","WANNEER","WAAR","WAAROM","IK","JE","HIJ","ZIJ","WIJ","HUN"
    },
    "SV": {
        "OCH","DET","ATT","I","EN","SOM","AR","VAR","INTE","PA","MED","FOR","TILL",
        "VAD","NAR","VAR","HUR","JAG","DU","HAN","HON","VI","DE"
    },
    "PL": {
        "I","ORAZ","ALE","NIE","JEST","SA","BYL","W","Z","DO","NA","ZE","KTORY",
        "KTO","CO","KIEDY","GDZIE","DLACZEGO","JA","TY","ON","ONA","MY","WY"
    },
    "LA": {
        "ET","IN","EST","NON","AD","CUM","QUI","QUAE","QUOD","SUNT","ERAT","FUIT",
        "HOC","ILLE","ILLA","EGO","TU","NOS","VOS","SE"
    }
}

# ---- weights per language (tweakable) ----
LANG_WEIGHTS = {
    "EN": 1.2,
    "IT": 1.1,
    "FR": 1.1,
    "ES": 1.1,
    "DE": 1.0,
    "PT": 1.0,
    "NL": 0.9,
    "SV": 0.9,
    "PL": 0.9,
    "LA": 0.8,
}

# ---- scoring ----

def word_score(text: str) -> float:
    """
    Returns a weighted score based on presence of common words
    across multiple languages.
    """
    if not text:
        return 0.0

    t = text.upper()
    score = 0.0

    for lang, words in WORD_BANKS.items():
        weight = LANG_WEIGHTS.get(lang, 1.0)
        hits = 0
        for w in words:
            # whole-word-ish check (simple but fast)
            if f" {w} " in f" {t} ":
                hits += 1
        score += hits * weight

    return score


def detect_language(text: str) -> str | None:
    """
    Returns best-guess language code or None.
    """
    t = text.upper()
    best_lang = None
    best_score = 0.0

    for lang, words in WORD_BANKS.items():
        hits = sum(1 for w in words if f" {w} " in f" {t} ")
        weighted = hits * LANG_WEIGHTS.get(lang, 1.0)
        if weighted > best_score:
            best_score = weighted
            best_lang = lang

    return best_lang if best_score > 0 else None
