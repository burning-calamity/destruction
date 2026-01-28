# destruction/__init__.py
import pkgutil
import importlib

__version__ = "0.1.4"

__all__ = [m.name for m in pkgutil.iter_modules(__path__)]

def __getattr__(name):
    if name in __all__:
        module = importlib.import_module(f"{__name__}.{name}")
        globals()[name] = module
        return module
    raise AttributeError(f"module {__name__} has no attribute {name}")
