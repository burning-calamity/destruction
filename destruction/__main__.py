import sys
from destruction.caesar import caesar
from destruction.rot13 import rot13
from destruction.vigenere import vigenere
from destruction.enigma import enigma
from destruction.bruteforce import brute_force_caesar


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m destruction <cipher> [args]")
        return

    cmd = sys.argv[1].lower()

    try:
        if cmd == "caesar":
            print(caesar(sys.argv[2], int(sys.argv[3])))
        elif cmd == "rot13":
            print(rot13(sys.argv[2]))
        elif cmd == "vigenere":
            print(vigenere(sys.argv[2], sys.argv[3]))
        elif cmd == "enigma":
            print(enigma(sys.argv[2], sys.argv[3]))
        elif cmd == "bruteforce":
            for s, t, score in brute_force_caesar(sys.argv[2]):
                print(f"{s:2d} | {score:.2f} | {t}")
        else:
            print("Unknown command")
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
