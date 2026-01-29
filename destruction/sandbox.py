from __future__ import annotations

import importlib
import multiprocessing as mp
import traceback
import time
from typing import Any, Dict, Tuple

class SandboxError(RuntimeError):
    pass


def _estimate_size(obj: Any) -> int:
    if isinstance(obj, (str, bytes, bytearray)):
        return len(obj)
    if isinstance(obj, (list, tuple)):
        return sum(_estimate_size(x) for x in obj)
    if isinstance(obj, dict):
        return sum(_estimate_size(k) + _estimate_size(v) for k, v in obj.items())
    return 32  # conservative fallback


def _worker(func_path: Tuple[str, str], args, kwargs, q: mp.Queue):
    try:
        mod = importlib.import_module(func_path[0])
        fn = getattr(mod, func_path[1])
        out = fn(*args, **kwargs)
        q.put(("ok", out))
    except Exception as e:
        q.put(("err", f"{type(e).__name__}: {e}", traceback.format_exc()))


def sandbox(
    cipher: str,
    *args,
    timeout: float = 1.0,
    max_size: int = 200_000,
    **kwargs,
):
    """
    Safe cipher runner.

    - subprocess isolation
    - hard timeout
    - input size guard
    - no global state leakage

    Usage:
        destruction.sandbox("caesar", "HELLO", 3)
    """
    if not cipher.isidentifier():
        raise SandboxError("Invalid cipher name")

    size = sum(_estimate_size(a) for a in args) + sum(_estimate_size(v) for v in kwargs.values())
    if size > max_size:
        raise SandboxError("Input too large")

    q: mp.Queue = mp.Queue()
    p = mp.Process(
        target=_worker,
        args=((f"destruction.{cipher}", cipher), args, kwargs, q),
        daemon=True,
    )

    p.start()
    p.join(timeout)

    if p.is_alive():
        p.terminate()
        raise SandboxError("Execution timed out")

    if q.empty():
        raise SandboxError("No output from cipher")

    msg = q.get()
    if msg[0] == "ok":
        return msg[1]

    raise SandboxError(msg[1])
