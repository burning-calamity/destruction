import pkgutil
import importlib

__version__ = "0.1.7"
"cyphers are cool"
__all__ = [m.name for m in pkgutil.iter_modules(__path__)]

def __getattr__(name):
    if name in __all__:
        module = importlib.import_module(f"{__name__}.{name}")
        value = getattr(module, name, module)
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__} has no attribute {name}")
