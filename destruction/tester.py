from __future__ import annotations
import importlib
import pkgutil
import traceback
import sys
from types import ModuleType

PACKAGE = __name__.rsplit(".", 1)[0]

# Minimal test vectors per module/function
TESTS = {
    "caesar": lambda m: m.caesar("Hello", 3) == "Khoor",
    "rot13": lambda m: m.rot13("Hello") == "Uryyb",
    "atbash": lambda m: m.atbash("abcXYZ") == "zyxCBA",
    "vigenere": lambda m: m.vigenere("HELLO", "KEY") == "RIJVS",
    "rail_fence": lambda m: m.rail_fence("HELLOWORLD", 3) == "HOLELWRDLO",
    "baconian": lambda m: isinstance(m.baconian("AB"), str),
    "columnar": lambda m: isinstance(m.columnar("HELLO", "KEY"), str),
    "affine": lambda m: m.affine("ABC", 5, 8) == "INS",
    "playfair": lambda m: isinstance(m.playfair("HELLO", "KEY"), str),
    "hill": lambda m: isinstance(m.hill("TEST", (3,3,2,5)), str),
    "xor": lambda m: isinstance(m.xor_cipher("abc", 23), str),
    "base64c": lambda m: m.b64decode(m.b64encode("test")) == "test",
    "langdetect": lambda m: m.detect_language("Hello world") in {"EN","FR","DE","ES","IT"},
    "autoguess": lambda m: isinstance(m.auto_guess("Uryyb"), list),
    "uninstaller": lambda m: hasattr(m, "print_uninstall_hint"),
    "updater": lambda m: hasattr(m, "print_update_hint"),
}

def _iter_modules():
    pkg = sys.modules.get(PACKAGE)
    if not pkg:
        pkg = importlib.import_module(PACKAGE)

    for info in pkgutil.iter_modules(pkg.__path__):
        if info.name.startswith("_"):
            continue
        yield info.name

def tester():
    print("=" * 60)
    print("DESTRUCTION TESTER — MODULE HEALTH CHECK")
    print("=" * 60)

    results = []
    for name in sorted(_iter_modules()):
        try:
            mod: ModuleType = importlib.import_module(f"{PACKAGE}.{name}")

            if name in TESTS:
                ok = TESTS[name](mod)
                if ok is True:
                    results.append((name, "OK", None))
                else:
                    results.append((name, "FAIL", "Test returned False"))
            else:
                # Module imported but no test defined
                results.append((name, "SKIP", "No test defined"))

        except Exception as e:
            results.append(
                (
                    name,
                    "ERROR",
                    "".join(traceback.format_exception_only(type(e), e)).strip(),
                )
            )

    # Print report
    ok = fail = err = skip = 0
    for name, status, info in results:
        if status == "OK":
            ok += 1
            print(f"[ OK ] {name}")
        elif status == "SKIP":
            skip += 1
            print(f"[SKIP] {name} — {info}")
        elif status == "FAIL":
            fail += 1
            print(f"[FAIL] {name} — {info}")
        else:
            err += 1
            print(f"[ERR ] {name} — {info}")

    print("-" * 60)
    print(f"Summary: OK={ok}  FAIL={fail}  ERROR={err}  SKIP={skip}")
    print("=" * 60)

    return {
        "ok": ok,
        "fail": fail,
        "error": err,
        "skip": skip,
        "details": results,
    }
