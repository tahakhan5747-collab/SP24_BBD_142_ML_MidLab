# Python compatibility update

The project accepts regular 64-bit CPython 3.11, 3.12, 3.13 and 3.14. Free-threaded experimental builds are not covered.

Only three direct pins changed:

| Package | Previous | Updated | Reason |
| --- | --- | --- | --- |
| pandas | 2.2.3 | 2.3.3 | Ready-made Python 3.14 Windows x64 wheel |
| pydantic | 2.11.4 | 2.12.5 | Updated pydantic-core with Python 3.14 support |
| ipykernel | 6.29.5 | 7.4.0 | Current Python 3.14 notebook-kernel compatibility |

PyPI package metadata confirmed Windows x64 cp314 wheels for the pinned NumPy, pandas, SciPy, scikit-learn and Matplotlib. The whole notebook dependency set also resolved for Python 3.14 Windows x64 with binary-only installation required, including compiled transitive dependencies. Resolution verifies package availability, not actual Windows execution.

A fresh Linux Python 3.14.8 environment was installed for execution tests. Details and outcomes are in VALIDATION.md. The user's regular Python 3.14.2 uses the same cp314 wheel ABI, but that exact patch version and Windows system were not directly executed here.

setup_windows.bat checks the active environment and selects an available supported interpreter, rather than silently accepting arbitrary Python versions. It uses --only-binary=:all: to report missing wheels instead of starting a compiler build. Network/proxy or platform-specific issues can still cause installation failures.
