# Replay receipt (v0.1.0, 26 November 2026)

Release replay by the publisher from a fresh copy of the approved candidate (code, requirements.txt), macOS arm64,
working directory the package root, run through the host's shared job queue on one CPU. Interpreters as printed inside
the run (see [ENVIRONMENT.txt](ENVIRONMENT.txt)): CPython 3.12.11 with mpmath 1.3.0, or with SciPy 1.17.0 and NumPy
2.3.5; CPython 3.14.7 (uv shim) for the standard-library verify.py.

| Program | Flags | Exit | Output |
|---|---|---|---|
| code/verify.py | -I -B -O | 0 | results/verification.txt, byte-identical to the approved file; `All checks passed.` |
| code/cube_census.py | -I -B -O | 0 | results/cube_census.txt, byte-identical; 65,536 subsets; 32/256 (24 two-faces) and 12/256 (32 three-faces); `All high-precision constant checks passed.` |
| code/verify_asymptotic.py | -I -B -O | 0 | results/asymptotic.txt, byte-identical; `All numerical sanity checks passed.` |
| code/check_extensions.py --output results/extensions.json | -I -B -O | 0 | results/extensions.json, byte-identical; `ALL CHECKS PASSED` |
| Negative control | cube_census.py with the expectation `masses[4]==32` changed to 33, -I -B -O | 1 | `CHECK FAILED: masses[4]==32` |

stderr was empty for all passing runs. The outputs match the lead's clean replay of 24-25 November 2026 and the
independent rerun of check_extensions.py in the verification round. After the replay only the title-page DOI line of
manuscript.tex, the rebuilt PDF and the release records changed; the code, results and requirements are
byte-identical to the approved candidate.

Comparison policy for other platforms: see [ENVIRONMENT.txt](ENVIRONMENT.txt) and [README.md](README.md).
