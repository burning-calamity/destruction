from __future__ import annotations

import importlib
import multiprocessing as mp
import traceback
from typing import Any, Dict, Tuple


class SandboxError(RuntimeError):
    pass


def _is_too_big(obj: Any, max_chars: int) -> bool:
    # Conservative: only measure strings/bytes/iterables of strings
    try:
        if isinstance(obj, (str, bytes, bytearray)):
            return len(obj) > max_chars
        if isinstance(obj, (list, tuple)):
            total = 0
            for x in obj:
                if isinstance(x, (str, bytes, bytearray)):
                    total += len(x)
                else:
                    total += 16
                if total > max_chars:
                    return True
            return False
    except Exception:
        return True
    return False


def _worker(func_path: Tuple[str, str], args: Tuple[Any, ...], kwargs: Dict[str, Any], q: mp.Queue):
    try:
        mod_name, attr_name = func_path
        mod = importlib.import_module(mod_name)
        fn = getattr(mod, attr_name)

        out = fn(*args, **kwargs)
        q.put({"ok": True, "result": out})
    except Exception as e:
        q.put(
            {
                "ok": False,
                "error": f"{type(e).__name__}: {e}",
                "traceback": traceback.format_exc(),
            }
        )


def sandbox(
    cipher: str,
    *args: Any,
    timeout: float = 1.0,
    max_chars: int = 200_000,
    allow_bytes: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Sandbox runner:
      - runs cipher in a subprocess (timeout enforced)
      - rejects overly large inputs
      - returns the cipher result or raises SandboxError

    Usage:
      destruction.sandbox("atbash", "hello")
      destruction.sandbox("caesar", "HELLO", 3)
    """
    if not isinstance(cipher, str) or not cipher:
        raise SandboxError("cipher must be a non-empty string (module/function name).")

    # Basic size checks
    for obj in args:
        if not allow_bytes and isinstance(obj, (bytes, bytearray)):
            raise SandboxError("bytes inputs disabled in sandbox.")
        if _is_too_big(obj, max_chars):
            raise SandboxError(f"input too large (max_chars={max_chars}).")

    for k, v in kwargs.items():
        if _is_too_big(v, max_chars):
            raise SandboxError(f"kwarg '{k}' too large (max_chars={max_chars}).")

    # Resolve function by importing the module destruction.<cipher> and calling <cipher>(...)
    func_path = (f"destruction.{cipher}", cipher)

    q: mp.Queue = mp.Queue()
    p = mp.Process(target=_worker, args=(func_path, args, kwargs, q), daemon=True)
    p.start()
    p.join(timeout=timeout)

    if p.is_alive():
        p.terminate()
        p.join(0.2)
        raise SandboxError(f"timeout after {timeout}s running cipher '{cipher}'.")

    if q.empty():
        raise SandboxError(f"cipher '{cipher}' produced no result (process ended unexpectedly).")

    msg = q.get()
    if msg.get("ok"):
        return msg.get("result")

    # Keep error short by default; user can inspect traceback if needed
    raise SandboxError(f"cipher '{cipher}' failed: {msg.get('error')}")
