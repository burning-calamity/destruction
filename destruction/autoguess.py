from .bruteforce import brute_force_caesar
from .rot13 import rot13


def auto_guess(text: str):
    guesses = []

    guesses.append(("rot13", rot13(text)))

    for shift, decoded, score in brute_force_caesar(text):
        guesses.append((f"caesar({shift})", decoded))

    return guesses
