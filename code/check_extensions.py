#!/usr/bin/env python3
"""Checks for the numerical statements added in the revised manuscript.

Every check prints PASS or FAIL and the script exits with status 1 if any
check fails, also under ``python -O`` (no ``assert`` statements are used).

Sections
  A  margins used in the proof of Theorem 3.1 (50-digit mpmath)
  B  competitors bounding the pair-optimal threshold interval (Proposition 3.3)
  C  the improved constant in Kontorovich's tensorization theorem (Corollary 4.5)
  D  explicit Hilbert stability constants (Remark 5.2)
  E  explicit localisation constants (Proposition 7.1)
  F  numerical evidence for Conjecture 10.1 on the interval [2-sqrt2, 2sqrt2-sqrt3]
  G  the equal-coefficient stop-loss envelope (Remark 8.3)

Sections A-E are exact or high-precision evaluations of closed forms.
Sections F and G are finite numerical evidence with a declared tolerance;
they do not prove the conjecture or the remark.

Usage: python3 check_extensions.py [--output results/extensions.json]
Requires mpmath (tested with mpmath 1.3.0).
"""
import argparse
import json
import random
import sys
from collections import Counter
from itertools import combinations_with_replacement, product
from math import comb

import mpmath as mp

mp.mp.dps = 50
FAILURES = []
RESULTS = {}


def check(name, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {name}" + (f": {detail}" if detail else ""))
    if not condition:
        FAILURES.append(name)


def s(x, digits=20):
    return mp.nstr(x, digits)


# ---------------------------------------------------------------- A
def section_a():
    r2, pi2 = mp.sqrt(2), mp.pi ** 2
    gap = (r2 - 1) / 2 - mp.mpf(1) / 4 + mp.mpf(9) / (20 * pi2)
    residual = gap - mp.mpf(1) / 400
    # the same computation with the decimal bounds quoted in the proof
    gap_dec = (mp.mpf("1.4142") - 1) / 2 - mp.mpf(1) / 4 + mp.mpf(9) / (20 * mp.mpf("9.88"))
    residual_dec = gap_dec - mp.mpf(1) / 400
    check("A1 sqrt2 > 1.4142 and pi^2 < 9.88", r2 > mp.mpf("1.4142") and pi2 < mp.mpf("9.88"))
    check("A2 exterior gap at t=1 exceeds 1/400", gap > mp.mpf(1) / 400, s(gap))
    check("A3 residual after Lipschitz extension to t=201/200 is > 1.4e-4",
          residual_dec > mp.mpf("1.4e-4") and residual > residual_dec,
          f"exact {s(residual, 12)}, with quoted decimals {s(residual_dec, 12)}")
    check("A4 sin^2(pi/10) < 1/10 and exp(-pi^2/2) < 1/10",
          mp.sin(mp.pi / 10) ** 2 < mp.mpf(1) / 10 and mp.exp(-pi2 / 2) < mp.mpf(1) / 10)
    c1 = mp.mpf(1) / 2 - 5 * r2 / 16
    c2 = mp.mpf(1) / 2 - 50 * r2 / 156
    check("A5 interior coefficient at t=1: 1/2 - 5sqrt2/16 > 0", c1 > 0, s(c1, 12))
    check("A6 interior coefficient on interval: 1/2 - (50/39)sqrt2/4 > 0", c2 > 0, s(c2, 12))
    check("A7 stability coefficient (1/2-5sqrt2/16)/sqrt2 > 1/1000", c1 / r2 > mp.mpf(1) / 1000, s(c1 / r2, 12))
    check("A8 exterior case: 1/400 > 2/1000 (d^2 <= 2)", mp.mpf(1) / 400 > mp.mpf(2) / 1000)
    RESULTS["A_theorem_3_1_margins"] = {
        "gap_at_t1": s(gap), "residual_at_201_200": s(residual, 12),
        "residual_with_quoted_decimals": s(residual_dec, 12),
        "interior_coefficient_t1": s(c1, 12), "interior_coefficient_interval": s(c2, 12),
        "stability_coefficient": s(c1 / r2, 12)}


# ---------------------------------------------------------------- B
def pair(t):
    return (mp.sqrt(2) - t) / 2


def single(t):
    return max(1 - t, 0)


def triple(t):
    r3 = mp.sqrt(3)
    if t <= 1 / r3:
        return (3 * (1 / r3 - t) + (r3 - t)) / 4
    return (r3 - t) / 4


def section_b():
    lo = 2 - mp.sqrt(2)
    hi = 2 * mp.sqrt(2) - mp.sqrt(3)
    check("B1 single coefficient ties the pair at 2-sqrt2", abs(single(lo) - pair(lo)) < mp.mpf("1e-45"))
    check("B2 three equal coefficients tie the pair at 2sqrt2-sqrt3", abs(triple(hi) - pair(hi)) < mp.mpf("1e-45"))
    ok_below = all(single(lo - mp.mpf(k) / 1000) > pair(lo - mp.mpf(k) / 1000) for k in range(1, 400))
    ok_above = all(triple(hi + mp.mpf(k) / 1000) > pair(hi + mp.mpf(k) / 1000) for k in range(1, 300))
    check("B3 single beats pair on (2-sqrt2-0.399, 2-sqrt2)", ok_below)
    check("B4 triple beats pair on (2sqrt2-sqrt3, 2sqrt2-sqrt3+0.299)", ok_above)
    RESULTS["B_interval_endpoints"] = {"lower_2_minus_sqrt2": s(lo), "upper_2sqrt2_minus_sqrt3": s(hi)}


# ---------------------------------------------------------------- C
def section_c():
    old = (1 / mp.sqrt(2) - mp.mpf(1) / 4) * (2 - 2 * mp.exp(-mp.mpf(1) / 2)) / 2
    new = (1 - mp.exp(-mp.mpf(1) / 2)) / 2
    check("C1 Kontorovich's printed constant: c > 0.1798 from Lowther's factor",
          old > mp.mpf("0.1798"), s(old, 10))
    check("C2 sharp factor 1/2 gives c = (1-e^{-1/2})/2 > 0.1967", new > mp.mpf("0.1967"), s(new, 10))
    RESULTS["C_tensorization_constant"] = {"previous": s(old, 10), "improved": s(new, 10)}


# ---------------------------------------------------------------- D
def section_d():
    out = {}
    for label, c0 in (("ENT_published_8e-5", mp.mpf("8e-5")), ("Fang_Wang_preprint_1_20", mp.mpf(1) / 20)):
        K = (2 + 24 * mp.sqrt(2)) / c0 + 48
        cH = min(1 / (200 * K), 1 / (4 * mp.sqrt(2)))
        out[label] = {"c0": s(c0, 6), "K": s(K, 10), "c_H": s(cH, 6)}
    check("D1 c_H with c0 = 8e-5 exceeds 1.1e-8", mp.mpf(out["ENT_published_8e-5"]["c_H"]) > mp.mpf("1.1e-8"),
          out["ENT_published_8e-5"]["c_H"])
    check("D2 c_H with c0 = 1/20 exceeds 6.5e-6", mp.mpf(out["Fang_Wang_preprint_1_20"]["c_H"]) > mp.mpf("6.5e-6"),
          out["Fang_Wang_preprint_1_20"]["c_H"])
    RESULTS["D_hilbert_stability_constants"] = out


# ---------------------------------------------------------------- E
def section_e():
    g = mp.sqrt(2) - 1
    cinv = 2 / g + 8000 / g ** 2
    check("E1 localisation constant 1/c = 2/gamma + 8000/gamma^2 < 46,700", cinv < 46700, s(cinv, 10))
    RESULTS["E_localisation"] = {"one_over_c": s(cinv, 10), "C": s(1 + mp.sqrt(2), 12)}


# ---------------------------------------------------------------- F
def counts_of(weights):
    counts = Counter({0: 1})
    for a in weights:
        nxt = Counter()
        for total, ways in counts.items():
            nxt[total + a] += ways
            nxt[total - a] += ways
        counts = nxt
    return counts


def stop_loss_integer(weights, t):
    energy = sum(w * w for w in weights)
    root = mp.sqrt(energy)
    counts = counts_of(weights)
    mass = mp.mpf(2) ** len(weights)
    return sum(v * max(abs(x) / root - t, 0) for x, v in counts.items()) / mass


def section_f():
    lo = 2 - mp.sqrt(2)
    hi = 2 * mp.sqrt(2) - mp.sqrt(3)
    ts = [lo + (hi - lo) * mp.mpf(j) / 24 for j in range(1, 24)]
    worst = mp.mpf(-1)
    worst_where = None
    tuples = 0
    for n in range(1, 10):
        for weights in combinations_with_replacement(range(1, 6), n):
            tuples += 1
            is_pair = n == 2 and weights[0] == weights[1]
            for t in ts:
                excess = stop_loss_integer(weights, t) - pair(t)
                if is_pair:
                    if abs(excess) > mp.mpf("1e-40"):
                        worst = max(worst, excess)
                elif excess > worst:
                    worst, worst_where = excess, (weights, s(t, 8))
    check("F1 integer tuples (entries 1..5, length <= 9): no tuple exceeds the pair at 23 interior thresholds",
          worst < mp.mpf("-1e-12"), f"{tuples} tuples, largest excess over pair {s(worst, 8)} at {worst_where}")
    rng = random.Random(20261125)
    worst_r = -1.0
    trials = 0
    for _ in range(3000):
        n = rng.randint(2, 12)
        a = [abs(rng.gauss(0, 1)) ** rng.choice((0.5, 1, 2, 4)) for _ in range(n)]
        norm = sum(x * x for x in a) ** 0.5
        a = [x / norm for x in a]
        sums = [abs(sum(e * x for e, x in zip(signs, a))) for signs in product((-1, 1), repeat=n)]
        for t in ts:
            tf = float(t)
            val = sum(max(v - tf, 0.0) for v in sums) / len(sums)
            worst_r = max(worst_r, val - float(pair(t)))
        trials += 1
    check("F2 3000 seeded random unit vectors (n <= 12, float, tolerance 1e-12): none exceeds the pair",
          worst_r < 1e-12, f"largest excess {worst_r:.3e}")
    RESULTS["F_conjecture_evidence"] = {"integer_tuples": tuples, "thresholds": 23,
                                       "largest_integer_excess": s(worst, 8),
                                       "random_vectors": trials, "largest_random_excess": f"{worst_r:.3e}"}


# ---------------------------------------------------------------- G
def equal_value(k, t):
    return sum(comb(k, j) * max(abs(k - 2 * j) / mp.sqrt(k) - t, 0) for j in range(k + 1)) / mp.mpf(2) ** k


def gauss_value(t):
    return 2 * (mp.npdf(t) - t * (1 - mp.ncdf(t)))


def section_g():
    mp.mp.dps = 30
    kmax = 120
    grid = [mp.mpf("0.55") + mp.mpf(j) / 1000 for j in range(0, 1451)]
    winners = []
    for t in grid:
        vals = [(equal_value(k, t), k) for k in range(1, kmax + 1)]
        vals.append((gauss_value(t), "G"))
        winners.append(max(vals, key=lambda p: p[0])[1])
    segs = []
    for t, w in zip(grid, winners):
        if not segs or segs[-1][0] != w:
            segs.append([w, s(t, 4), s(t, 4)])
        else:
            segs[-1][2] = s(t, 4)
    print("   equal-coefficient envelope (winner, from t, to t):", segs[:8])
    margins = {}
    for k in (5, 6):
        a = (k - 2) / mp.sqrt(k)
        b = mp.sqrt(k)
        worst = mp.inf
        for j in range(1, 2000):
            t = a + (b - a) * mp.mpf(j) / 2000
            mine = equal_value(k, t)
            other = max([equal_value(m, t) for m in range(1, kmax + 1) if m != k] + [gauss_value(t)])
            worst = min(worst, other - mine)
        margins[k] = worst
        check(f"G{k} on ((k-2)/sqrt k, sqrt k) for k={k}, another equal vector or the Gaussian is larger",
              worst > mp.mpf("1e-4"), f"minimum margin {s(worst, 6)}")
    def winner_at(t):
        vals = [(equal_value(k, t), k) for k in range(1, kmax + 1)] + [(gauss_value(t), "G")]
        return max(vals, key=lambda p: p[0])[1]
    probes = {"0.8": 2, "1.3": 3, "1.6": 4}
    got = {x: winner_at(mp.mpf(x)) for x in probes}
    check("G1 among equal vectors the winner is k=2 at t=0.8, k=3 at t=1.3, k=4 at t=1.6",
          all(got[x] == probes[x] for x in probes), str(got))
    RESULTS["G_equal_coefficient_envelope"] = {"segments": segs, "k5_min_margin": s(margins[5], 6),
                                              "k6_min_margin": s(margins[6], 6), "kmax": kmax}
    mp.mp.dps = 50


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    for f in (section_a, section_b, section_c, section_d, section_e, section_f, section_g):
        f()
    RESULTS["failures"] = FAILURES
    if args.output:
        with open(args.output, "w") as fh:
            json.dump(RESULTS, fh, indent=2, sort_keys=True)
    if FAILURES:
        print("SOME CHECKS FAILED:", FAILURES)
        sys.exit(1)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
