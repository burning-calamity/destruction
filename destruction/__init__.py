from __future__ import annotations

__version__ = "0.1.11"

import importlib
import pkgutil
from typing import List

# ---- automatic discovery of public submodules ----

def _discover_public_modules() -> List[str]:
    names: List[str] = []
    for m in pkgutil.iter_modules(__path__):  # type: ignore[name-defined]
        if not m.name.startswith("_"):
            names.append(m.name)
    return names


__all__ = _discover_public_modules()

# ---- editor support (Ctrl+Space / dir()) ----

def __dir__():
    return sorted(__all__)

# ---- lazy attribute access + callable modules ----

def __getattr__(name):
    try:
        module = importlib.import_module(f"{__name__}.{name}")
    except ModuleNotFoundError:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

    # If module has a function with the same name, return it directly
    if hasattr(module, name) and callable(getattr(module, name)):
        return getattr(module, name)

    return module
