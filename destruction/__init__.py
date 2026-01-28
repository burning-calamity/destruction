import pkgutil
import importlib

__all__ = []

for module in pkgutil.iter_modules(__path__):
    name = module.name
    importlib.import_module(f"{__name__}.{name}")
    __all__.append(name)
