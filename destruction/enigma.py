ROTORS = [
    "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    "AJDKSIRUXBLHWTMCQGZNPYFVOE",
    "BDFHJLCPRTXVZNYEIWGAKMUSQO",
]

REFLECTOR = "YRUHQSLDPXNGOKMIEBFZCWVJAT"


def enigma(text: str, key: str = "AAA") -> str:
    """
    Simplified Enigma-like cipher.
    Same function encrypts and decrypts.
    """
    pos = [ord(c.upper()) - 65 for c in key[:3]]
    result = []

    for ch in text.upper():
        if not ch.isalpha():
            result.append(ch)
            continue

        c = ord(ch) - 65

        # forward rotors
        for i in range(3):
            c = (ord(ROTORS[i][(c + pos[i]) % 26]) - 65)

        # reflector
        c = ord(REFLECTOR[c]) - 65

        # reverse rotors
        for i in reversed(range(3)):
            c = (ROTORS[i].index(chr(c + 65)) - pos[i]) % 26

        result.append(chr(c + 65))

        # step rotors
        pos[0] = (pos[0] + 1) % 26
        if pos[0] == 0:
            pos[1] = (pos[1] + 1) % 26
            if pos[1] == 0:
                pos[2] = (pos[2] + 1) % 26

    return "".join(result)
