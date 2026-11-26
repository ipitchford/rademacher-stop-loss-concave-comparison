#!/usr/bin/env python3
"""Exact finite checks of the two scalar bounds, plus Hilbert sanity checks.

The proofs in manuscript.tex cover real coefficients in every dimension.
This script only checks the finite families explicitly enumerated below.
Requires Python 3.8+ and the standard library.
"""
from collections import Counter
from itertools import combinations_with_replacement, product
from math import isqrt, sqrt


def require(condition, detail="check failed"):
    """Fail loudly even under python -O (no reliance on assert)."""
    if not condition:
        print("CHECK FAILED:", detail)
        raise SystemExit(1)


def signed_sum_counts(coefficients):
    counts = Counter({0: 1})
    for a in coefficients:
        updated = Counter()
        for total, ways in counts.items():
            updated[total + a] += ways
            updated[total - a] += ways
        counts = updated
    return counts


def sign_two_surd(a, b):
    """Sign of a + b times sqrt(2) for integer arguments."""
    if not a:
        return (b > 0) - (b < 0)
    if not b or (a > 0) == (b > 0):
        return (a > 0) - (a < 0)
    difference = a * a - 2 * b * b
    return ((difference > 0) - (difference < 0)) * (1 if a > 0 else -1)


def check_scalars(weights):
    energy = sum(x * x for x in weights)
    counts = signed_sum_counts(weights)
    mass = 1 << len(weights)
    require(sum(counts.values()) == mass, 'sum(counts.values()) == mass')
    require(sum(k * k * v for k, v in counts.items()) == mass * energy, 'sum(k * k * v for k, v in counts.items()) == mass * energy')
    capped = sum(v for x, v in counts.items() if x * x > energy)
    small_sum = sum(abs(x) * v for x, v in counts.items() if x * x <= energy)
    excess_sum = sum(abs(x) * v for x, v in counts.items() if x * x > energy)

    # Capped numerator equals small_sum/sqrt(energy) + capped.
    remainder = mass - 2 * capped
    if remainder < 0:
        equal_clip = False
    else:
        slack = (2 * small_sum) ** 2 - energy * remainder ** 2
        require(slack >= 0, weights)
        equal_clip = slack == 0
    require(equal_clip == (len(weights) == 2 and weights[0] == weights[1]), weights)

    # 2 excess_sum <= sqrt(energy) (mass sqrt(2) + 2 capped - mass).
    # The right side is strictly positive, so squaring preserves comparison.
    b = 2 * capped - mass
    rational = energy * (b * b + 2 * mass * mass) - 4 * excess_sum ** 2
    radical = 2 * energy * b * mass
    excess_slack_sign = sign_two_surd(rational, radical)
    require(excess_slack_sign >= 0, weights)
    return equal_clip, excess_slack_sign == 0




def check_pair_threshold_interval(weights):
    energy = sum(x * x for x in weights)
    counts = signed_sum_counts(weights)
    mass = 1 << len(weights)
    for numerator, denominator in ((3, 4), (1, 1), (201, 200)):
        tail = {x: v for x, v in counts.items()
                if denominator ** 2 * x * x > numerator ** 2 * energy}
        count = sum(tail.values())
        total = sum(abs(x) * v for x, v in tail.items())
        b = numerator * (2 * count - mass)
        rational = (energy * (b * b + 2 * denominator ** 2 * mass ** 2)
                    - (2 * denominator * total) ** 2)
        radical = 2 * energy * b * denominator * mass
        sign = sign_two_surd(rational, radical)
        require(sign >= 0, (weights, numerator, denominator))
        require((sign == 0) == (len(weights) == 2 and weights[0] == weights[-1]), '(sign == 0) == (len(weights) == 2 and weights[0] == weights[-1])')
    # The left endpoint t=1/sqrt(2) has a rational squared certificate.
    count = sum(v for x, v in counts.items() if 2 * x * x > energy)
    total = sum(abs(x) * v for x, v in counts.items() if 2 * x * x > energy)
    slack = energy * (mass + 2 * count) ** 2 - 8 * total ** 2
    require(slack >= 0, weights)
    require((slack == 0) == (len(weights) == 2 and weights[0] == weights[-1]), '(slack == 0) == (len(weights) == 2 and weights[0] == weights[-1])')


def check_three_coefficient_threshold(weights):
    energy = sum(x * x for x in weights)
    counts = signed_sum_counts(weights)
    mass = 1 << len(weights)
    count = sum(v for x, v in counts.items() if 3 * x * x > 4 * energy)
    total = sum(abs(x) * v for x, v in counts.items() if 3 * x * x > 4 * energy)
    slack = energy * (mass + 8 * count) ** 2 - 48 * total ** 2
    require(slack >= 0, weights)
    require((slack == 0) == (len(weights) == 3 and weights[0] == weights[-1]), weights)


def check_hilbert(vectors):
    energy = sum(sum(z * z for z in v) for v in vectors)
    mass = 1 << len(vectors)
    factor = 10 ** 10
    lower = upper = 0
    for signs in product((-1, 1), repeat=len(vectors)):
        norm_sq = sum(sum(e * v[i] for e, v in zip(signs, vectors)) ** 2
                      for i in range(len(vectors[0])))
        if norm_sq >= energy:
            lower += factor
            upper += factor
        else:
            root = isqrt(norm_sq * factor * factor // energy)
            lower += root
            upper += root + int(root * root * energy != norm_sq * factor * factor)
    # The known equality case involves only zeros and saturated entries,
    # so these rigorous lower endpoints suffice throughout this grid.
    require(2 * lower >= mass * factor, vectors)
    return lower / (mass * factor), upper / (mass * factor)


def main():
    scalar_count = clip_equal = excess_equal = 0
    for n in range(1, 11):
        for weights in combinations_with_replacement(range(1, 5), n):
            c, e = check_scalars(weights)
            check_three_coefficient_threshold(weights)
            check_pair_threshold_interval(weights)
            scalar_count += 1
            clip_equal += c
            excess_equal += e
    print(f"Verified {scalar_count} sorted positive integer coefficient tuples (1..4, dimensions 1..10).")
    print("Verified pair-optimal thresholds 1/sqrt(2), 3/4, 1 and 201/200, including equality cases.")
    print("Also verified threshold 2/sqrt(3), with only the three-equal-coefficient equalities.")
    print(f"Capped equality cases: {clip_equal}; excess-loss equality cases: {excess_equal}.")
    vectors = ((0, 1), (1, 0), (1, 1), (1, -1), (1, 2), (2, 1))
    vector_count = 0
    for n in range(1, 7):
        for selected in combinations_with_replacement(vectors, n):
            check_hilbert(selected)
            vector_count += 1
    print(f"Verified {vector_count} Hilbert tuples (six specified integer vectors, dimensions 1..6).")
    for name, case in [("two equal collinear", [(1, 0), (1, 0)]),
                       ("two orthogonal", [(1, 0), (0, 1)]),
                       ("four equal collinear", [(1, 0)] * 4),
                       ("three equal collinear", [(1, 0)] * 3)]:
        lo, hi = check_hilbert(case)
        print(f"{name}: clipped expectation in [{lo:.10f}, {hi:.10f}].")
    require(abs((sqrt(2) - 1) / 2 - 0.20710678118654752) < 1e-15, 'abs((sqrt(2) - 1) / 2 - 0.20710678118654752) < 1e-15')
    print("All checks passed.")


if __name__ == "__main__":
    main()
