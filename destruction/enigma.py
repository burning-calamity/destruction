import string

ALPHA = string.ascii_uppercase

ROTORS = {
    "I":   "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    "II":  "AJDKSIRUXBLHWTMCQGZNPYFVOE",
    "III": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
}

REFLECTOR = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

def _shift(c, wiring, pos, reverse=False):
    idx = (ALPHA.index(c) + pos) % 26
    if reverse:
        return ALPHA[(wiring.index(ALPHA[idx]) - pos) % 26]
    return ALPHA[(ALPHA.index(wiring[idx]) - pos) % 26]

def enigma(
    text: str,
    rotors=("I", "II", "III"),
    positions=(0, 0, 0),
):
    r = [ROTORS[x] for x in rotors]
    p = list(positions)

    out = []

    for ch in text.upper():
        if not ch.isalpha():
            out.append(ch)
            continue

        # rotor stepping
        p[2] = (p[2] + 1) % 26
        if p[2] == 0:
            p[1] = (p[1] + 1) % 26
            if p[1] == 0:
                p[0] = (p[0] + 1) % 26

        c = ch
        for i in (2, 1, 0):
            c = _shift(c, r[i], p[i])

        c = REFLECTOR[ALPHA.index(c)]

        for i in (0, 1, 2):
            c = _shift(c, r[i], p[i], reverse=True)

        out.append(c)

    return "".join(out)
