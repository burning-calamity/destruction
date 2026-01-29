from __future__ import annotations

__version__ = "0.1.11"

import importlib
import pkgutil
import sys
from typing import List

# ---- automatic discovery of public submodules ----

def _discover_public_modules() -> List[str]:
    names: List[str] = []
    for m in pkgutil.iter_modules(__path__):  # type: ignore[name-defined]
        if not m.name.startswith("_"):
            names.append(m.name)
    return names


__all__ = _discover_public_modules()

# ---- editor support ----

def __dir__():
    return sorted(__all__)

# ---- lazy loading + callable modules (FIXED) ----

def __getattr__(name):
    try:
        module = importlib.import_module(f"{__name__}.{name}")
    except ModuleNotFoundError:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

    # If module exposes a function with same name → promote it
    if hasattr(module, name) and callable(getattr(module, name)):
        func = getattr(module, name)
        setattr(sys.modules[__name__], name, func)  # ← CRITICAL LINE
        return func

    # Otherwise expose the module normally
    setattr(sys.modules[__name__], name, module)
    return module
