# Two equal coins: a sharp Rademacher stop-loss bound

**A sharp stop-loss bound for Rademacher sums, the constant two in a concave comparison, and local extremal sets on
the discrete cube**

Version 0.1.0 · DOI [10.5281/zenodo.24548728](https://doi.org/10.5281/zenodo.24548728) (all versions:
[10.5281/zenodo.24548727](https://doi.org/10.5281/zenodo.24548727)) · Author: Anonymous · Text CC0-1.0, code MIT ·
Release page: https://evidencepress.org/releases/rademacher-stop-loss-concave-comparison/

**Status: unrefereed research candidate.** The proofs and computations were checked by internal AI-assisted review,
proof audits and clean replays only (see [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md)). This is not peer review,
independent reproduction or formal verification.

## What this is about

Flip some fair coins and give each coin a weight, with the squared weights adding up to one. Add the weights of the
coins that land heads and subtract the weights of those that land tails. The result is a random number S centred at
zero with spread (standard deviation) one; it is called a Rademacher sum. How much of S, on average, sticks out more
than one unit from zero? In symbols: how large can the average overshoot E(|S| − 1)₊ be?

In 2024 Aryeh Kontorovich asked on MathOverflow whether, for independent symmetric random variables and every
increasing concave function f with f(0) = 0, the average of f at the square function is at most twice its average at
the absolute value of the sum. George Lowther reduced the question to Rademacher sums, proved it with the constant
2.187 instead of 2, and observed that the sharp constant would follow if the average overshoot beyond one were never
more than (√2 − 1)/2 ≈ 0.207, the value for two equal coins. That bound was left open.

Why care? Kontorovich needed the inequality to bound the total variation distance between two product distributions
from below by the distances between their pieces. Average overshoots ("stop-loss" quantities) are basic objects in
probability and insurance mathematics. And the same inequality measures how lopsided a subset of the cube {−1, 1}ⁿ can
be: this is the classical problem of Ahlswede and Katona of choosing a set of binary words whose average distance from
each other is as small as possible.

## What is new

1. **The sharp stop-loss bound.** E(|S| − t)₊ ≤ (√2 − t)/2 for every threshold t from 1/√2 to 201/200, with equality
   only for two equal weights, and a quadratic stability estimate. At t = 1 this is Lowther's bound.
2. **The constant two.** Kontorovich's comparison holds with the sharp constant 2, also for sign-invariant vectors in
   any Hilbert space, with linear stability.
3. **Product measures.** The constant in Kontorovich's lower bound for the total variation distance between product
   measures improves from 0.1798 to (1 − e^(−1/2))/2 ≈ 0.1967.
4. **Three equal weights.** Fang and Huang's capped three-weight inequality holds without the cap, with stability.
5. **The cube near density 1/4 (unconditional).** Sets of nearly maximal first-level Fourier weight are close to
   two-coordinate faces, and the maximal weight rises by about 2h² log(1/h) at density 1/4 ± h.
6. **Finer structure (assuming Lei Yu's 2026 small-density theorem, an unrefereed preprint).** An exact formula near
   density 1/4, the next-order terms, and the split of added mass between two neighbouring faces in proportions about
   98:2, given by the equation m = tanh(2m) of the Curie–Weiss–Potts model; the same theory near density 1/8.

**Idea of the proof.** Compare (|x| − 1)₊ with a parabola corrected by a cosine. The expectation of the cosine
factorises over the coins, which settles every case except two large weights; that case is a direct four-term
calculation.

## Limits

- The thresholds are proved only on [1/√2, 1.005]. The largest possible interval, [2 − √2, 2√2 − √3], is a conjecture
  supported by numerical evidence.
- The cube results are local (densities very close to 1/4 and 1/8), and the neighbourhoods are not explicit.
- The finer cube results rely on Yu's unrefereed preprint.
- The transfer method seems to work only for 2, 3 and perhaps 4 fixed coordinates; density 1/16 remains open.

Credits: the question and the total-variation application are Kontorovich's; the reduction and the proposed bound are
Lowther's; Yu's Theorem 5 (arXiv:2504.02593v2) is used for the finer cube results; Fang and Huang's capped three-weight
lemma, majorant and density-1/8 value are used and extended as the paper states.

## Contents

| Path | What it is |
|---|---|
| [manuscript.pdf](manuscript.pdf), [manuscript.tex](manuscript.tex) | The paper (18 pages); Section 9 describes the computations |
| [code/verify.py](code/verify.py) | Standard library. Exact checks of the stop-loss bound at four thresholds and the three-weight bound for 1,000 integer weight tuples; 923 Hilbert-space tuples → [results/verification.txt](results/verification.txt) |
| [code/cube_census.py](code/cube_census.py) | mpmath 1.3.0. All 65,536 subsets of the four-dimensional cube; constants to 80 digits → [results/cube_census.txt](results/cube_census.txt) |
| [code/verify_asymptotic.py](code/verify_asymptotic.py) | SciPy 1.17.0, NumPy 2.3.5. Numerical illustration of the asymptotic constants (evidence, not proof) → [results/asymptotic.txt](results/asymptotic.txt) |
| [code/check_extensions.py](code/check_extensions.py) | mpmath 1.3.0. Margins, interval endpoints, constants, conjecture evidence and the equal-weight envelope → [results/extensions.json](results/extensions.json) |
| [refs.bib](refs.bib) | Bibliography |
| [AI_INDEX.md](AI_INDEX.md), [RESEARCH_GATES.json](RESEARCH_GATES.json) | Machine-readable claim map; prior-art and limitation record |
| [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md), [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md), [ENVIRONMENT.txt](ENVIRONMENT.txt) | Checking record |
| [MANIFEST.sha256](MANIFEST.sha256), [LICENSE.md](LICENSE.md), [CITATION.cff](CITATION.cff) | Hashes, licences, citation |

## Replay

From the package root, with [uv](https://docs.astral.sh/uv/) (about five minutes in total; check_extensions.py takes
about four and a half minutes of one CPU):

```sh
uv run --python 3.12 python3 -I -B -O code/verify.py > results/verification.txt
uv run --python 3.12 --with mpmath==1.3.0 python3 -I -B -O code/cube_census.py > results/cube_census.txt
uv run --python 3.12 --with scipy==1.17.0 --with numpy==2.3.5 python3 -I -B -O code/verify_asymptotic.py > results/asymptotic.txt
uv run --python 3.12 --with mpmath==1.3.0 python3 -I -B -O code/check_extensions.py --output results/extensions.json
```

The last lines read `All checks passed.`, `All high-precision constant checks passed.`, `All numerical sanity checks
passed.` and `ALL CHECKS PASSED`; every script exits 0, and any failed check exits non-zero, also under `-O`.

Comparison policy: verification.txt and cube_census.txt are compared exactly. In asymptotic.txt (floating point,
SciPy; the arg-max is printed to six decimals because it is tolerance-limited) each number may differ by one unit in
its last printed decimal or by relative 1e-8, whichever is larger. In sections F and G of extensions.json (float or
30-digit evaluations) numbers are compared with relative tolerance 1e-8. All other text and fields are compared
exactly. GitHub CI ([.github/workflows/replay.yml](.github/workflows/replay.yml)) runs the three quick scripts
on Linux with this policy and a negative control; the slow check_extensions.py is replayed on the release host (see
[REPLAY_RECEIPT.md](REPLAY_RECEIPT.md)) and is kept off the CI critical path.

## Cite

Anonymous (2026). *A sharp stop-loss bound for Rademacher sums, the constant two in a concave comparison, and local
extremal sets on the discrete cube* (version 0.1.0). Evidence Press. https://doi.org/10.5281/zenodo.24548728
