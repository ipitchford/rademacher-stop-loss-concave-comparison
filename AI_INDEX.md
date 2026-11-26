# AI index: A sharp stop-loss bound for Rademacher sums (v0.1.0)

Machine-oriented map of claims, evidence and limits. Human readers should start with [README.md](README.md) ("What
this is about") and the paper [manuscript.pdf](manuscript.pdf) (source [manuscript.tex](manuscript.tex); Section 1
states the question, why it matters, what was known, what is new and a roadmap; Section 10 lists open problems).
DOI 10.5281/zenodo.24548728 (concept 10.5281/zenodo.24548727). Status: unrefereed candidate; internal AI-assisted
review, proof audits and computation only.

## Notation

ε_i independent fair signs; a ∈ R^n with Σ a_i² = 1; S_a = Σ a_i ε_i (Rademacher sum, variance 1). x₊ = max(x, 0).
E_2 = vectors with two equal nonzero weights ±1/√2. On the cube {−1,1}^n, b_A = E[ε 1_A] (unnormalised centroid);
‖b_A‖² is the first-level Fourier weight of 1_A; W(μ) is the dimension-free maximal weight at density μ.
[Yu] = L. Yu, arXiv:2504.02593v2, Theorem 5 (unrefereed preprint). [FH] = Fang and Huang, arXiv:2610.40486v1.

## Claims and where they are proved

| ID | Claim | Location | Status / dependence |
|---|---|---|---|
| A | E(|S_a| − t)₊ ≤ (√2 − t)/2 for all unit a and t ∈ [1/√2, 201/200]; equality only on E_2; at t = 1 deficit ≥ dist(a, E_2)²/1000 | Theorem 3.1 | written proof (quadratic majorant with cosine correction; two-large-weight case by direct calculation); unconditional |
| B | The pair is not optimal outside [2 − √2, 2√2 − √3] | Proposition 3.3 | written proof; unconditional |
| C | E min(|S_a|, 1) ≥ 1/2; Kontorovich's comparison with sharp constant 2 for nondecreasing f, f(0) = 0, f(t)/t nonincreasing; inf_a E min(|S_a|, t) = t/2 for 0 < t ≤ 201/200 | Corollaries 4.1, 4.3 | written proof; reduction due to Lowther |
| D | The comparison for sign-invariant vectors in any Hilbert space | Theorem 4.4 | written proof |
| E | Kontorovich's TV tensorization constant improves from 0.1798 to (1 − e^{−1/2})/2 ≈ 0.1967 | Corollary 4.5 | written proof against arXiv:2409.10368v2 |
| F | Linear stability in Hilbert space with explicit constants | Theorem 5.1, Remark 5.2 | written proof; constants use Eskenazis–Nayar–Tkocz (published) or Fang–Wang (preprint) |
| G | FH's capped inequality E(|S| − 2)₊ ≤ 1/4 (variance 3) holds without the cap, with stability, near the threshold | Theorem 6.1 | written proof; unconditional |
| H | Near density 1/4, near-optimal sets are close to two-coordinate faces; W(1/4 ± h) = 2 min(1/4, 1/4 ± h)² + (2 + o(1)) h² log(1/h) | Proposition 7.1, Theorem 7.2 | written proof; unconditional |
| I | Exact three-parameter formula near 1/4, nonattainment in finite dimension, expansion through h²; added mass split λ* : 1 − λ* with λ* = 0.97875… (m = tanh(2m)) | Corollary 7.3, Theorem 7.4 | written proof assuming [Yu] Theorem 5 |
| J | Transfer principle: a stable stop-loss inequality with k equal extremal weights gives the local theory near density 2^{−k}; applies for k = 2, 3; numerically not for k = 5, 6 | Theorem 8.1, Corollary 8.2, Remark 8.3 | written proof assuming [Yu] Theorem 5 |
| K | Conjecture: claim A holds on [2 − √2, 2√2 − √3] | Conjecture 10.1 | numerical evidence only (not proved) |

## Evidence

| Check | Program | Expected output | Arithmetic |
|---|---|---|---|
| A, G (spot checks), C/D (Hilbert tuples) | [code/verify.py](code/verify.py) | 1,000 tuples; thresholds 1/√2, 3/4, 1, 201/200 and 2/√3; 923 Hilbert tuples; `All checks passed.` | integers and Q(√2), interval enclosures |
| Cube census, constants of H, I, J | [code/cube_census.py](code/cube_census.py) | 65,536 subsets; 32/256 at density 1/4 (24 two-faces), 12/256 at 1/8 (32 three-faces); m*, λ*, κ₂, p*, κ₃ to 80 digits; `All high-precision constant checks passed.` | exact counts; deficits in floating point with tolerance 1e-14; mpmath |
| Asymptotics of I, J (illustration only) | [code/verify_asymptotic.py](code/verify_asymptotic.py) | corrections approach κ₂ = 2.0393…, κ₃ = 3.0816… with error of order 1/log(1/q); `All numerical sanity checks passed.` | SciPy floating point |
| Margins of A; endpoints of B; constants of E, F, H; evidence for K; envelope of J | [code/check_extensions.py](code/check_extensions.py) | [results/extensions.json](results/extensions.json); `ALL CHECKS PASSED` | mpmath; sections F, G float or 30-digit |

Negative control: changing `masses[4]==32` to 33 in cube_census.py makes it exit 1 under python -O
([REPLAY_RECEIPT.md](REPLAY_RECEIPT.md); also run in CI).

Numbers quoted on the release page: (√2 − 1)/2 ≈ 0.207; Lowther's 2.187; constant 2; 0.1798 → 0.1967; thresholds
1/√2 to 1.005 (201/200) proved, 2 − √2 ≈ 0.586 to 2√2 − √3 ≈ 1.096 conjectured; densities 1/4 and 1/8; about
2h² log(1/h); 98:2 (λ* = 0.97875…); 65,536 subsets; 1,000 and 923 tuples.

## Limits

Claim A is proved only for t ∈ [1/√2, 201/200]; K is a conjecture. Cube results are local near densities 1/4 and
1/8 with non-explicit neighbourhoods; I and J rely on Yu's unrefereed preprint. The transfer method is expected to
work only for k ∈ {2, 3, 4}; density 1/16 (FH Conjecture 3.1) is open. Floating-point outputs (asymptotic.txt,
extensions F and G, census deficits) are evidence, not proof.

## Replay and records

Replay commands: [README.md](README.md), [ENVIRONMENT.txt](ENVIRONMENT.txt), [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md), CI
[.github/workflows/replay.yml](.github/workflows/replay.yml). Review: [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md). Prior art
and limitation triage: [RESEARCH_GATES.json](RESEARCH_GATES.json). Bibliography: [refs.bib](refs.bib). Licences:
[LICENSE.md](LICENSE.md). Citation: [CITATION.cff](CITATION.cff). Hashes: [MANIFEST.sha256](MANIFEST.sha256).
