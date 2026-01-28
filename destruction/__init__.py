__version__ = "0.1.0"
REQUIRED = [
    "numpy", "scipy", "pandas", "torch", "tensorflow",
    "fastapi", "django", "sqlalchemy"
]

for pkg in REQUIRED:
    __import__(pkg)
