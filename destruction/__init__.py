from __future__ import annotations
version = "0.1.8"
import importlib
import pkgutil
from types import ModuleType
from typing import List

# ---- automatic discovery of public submodules ----

def _discover_public_modules() -> List[str]:
    names: List[str] = []
    for m in pkgutil.iter_modules(__path__):  # type: ignore[name-defined]
        if not m.name.startswith("_"):
            names.append(m.name)
    return names


__all__ = _discover_public_modules()


# ---- lazy attribute access ----

def __getattr__(name: str):
    if name in __all__:
        module: ModuleType = importlib.import_module(f"{__name__}.{name}")
        # Convention: module exposes an attribute with the same name
        try:
            return getattr(module, name)
        except AttributeError:
            raise AttributeError(
                f"Module '{module.__name__}' does not expose '{name}'"
            ) from None
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


# ---- editor support (Ctrl+Space / dir()) ----

def __dir__():
    return sorted(__all__)
