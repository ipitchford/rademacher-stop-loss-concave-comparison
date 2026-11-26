#!/usr/bin/env python3
"""Numerical checks of the adjacent-face asymptotic. Requires SciPy.

These computations illustrate a proved limit. They do not certify it.
The maximising fractions are tolerance-limited (optimizer xatol 1e-11 and
floating point), so they are printed to six decimals only.
"""
from math import exp, log, pi, sqrt, tanh
from scipy.optimize import brentq, minimize_scalar
from scipy.special import ndtri


def require(condition, detail="check failed"):
    """Fail loudly even under python -O (no reliance on assert)."""
    if not condition:
        print("CHECK FAILED:", detail)
        raise SystemExit(1)


def gaussian_tail_ratio(p):
    if p == 0:
        return 0.0
    z = ndtri(p)
    return exp(-0.5 * z * z - 0.5 * log(2 * pi) - log(p))


def excess_coefficient(q, fraction):
    base = gaussian_tail_ratio(q)
    mixture = (fraction * gaussian_tail_ratio(q * fraction)
               + (1 - fraction) * gaussian_tail_ratio(q * (1 - fraction)))
    return 2 * (2 * fraction - 1) ** 2 + (mixture - base) * (mixture + base)



def excess_three_face_coefficient(q, proportion):
    small = (1 - proportion) / 2
    base = gaussian_tail_ratio(q)
    mixture = (proportion * gaussian_tail_ratio(q * proportion)
               + 2 * small * gaussian_tail_ratio(q * small))
    return (-1 + 4 * (proportion ** 2 + 2 * small ** 2)
            + (mixture - base) * (mixture + base))


def main():
    m_star = brentq(lambda m: tanh(2 * m) - m, 0.5, 0.99999, xtol=1e-14)
    lambda_star = (1 + m_star) / 2
    entropy = -lambda_star * log(lambda_star) - (1 - lambda_star) * log(1 - lambda_star)
    kappa = 2 * entropy + 2 * m_star * m_star
    print(f"Limit maximising fraction = {lambda_star:.12f}")
    print(f"Limit correction kappa = {kappa:.12f}")
    print("q, maximising fraction, correction, error from kappa")
    for q in (1e-3, 1e-6, 1e-12, 1e-25, 1e-50, 1e-100, 1e-200):
        result = minimize_scalar(lambda fraction: -excess_coefficient(q, fraction),
                                 bounds=(0.5, 1), method="bounded",
                                 options={"xatol": 1e-11})
        val = -result.fun
        require(result.success, 'result.success')
        require(abs(result.x - lambda_star) < 0.03, 'abs(result.x - lambda_star) < 0.03')
        require(2 < val < kappa + 0.03, '2 < val < kappa + 0.03')
        print(f"{q:.0e}, {result.x:.6f}, {val:.8f}, {val-kappa:+.6f}")
    p_star = brentq(lambda p: log(2 * p / (1 - p)) - 6 * p + 2,
                    0.8, 0.99999, xtol=1e-14)
    small = (1 - p_star) / 2
    kappa_three = (-1 + 4 * (p_star ** 2 + 2 * small ** 2)
                   - 2 * (p_star * log(p_star) + 2 * small * log(small)))
    print(f"Three-face allocation = ({p_star:.12f}, {small:.12f}, {small:.12f})")
    print(f"Three-face correction kappa_3 = {kappa_three:.12f}")
    print("q, maximising dominant fraction, correction, error from kappa_3")
    for q in (1e-3, 1e-6, 1e-12, 1e-25, 1e-50, 1e-100, 1e-200):
        result = minimize_scalar(lambda p: -excess_three_face_coefficient(q, p),
                                 bounds=(0.8, 1), method="bounded",
                                 options={"xatol": 1e-11})
        val = -result.fun
        require(result.success, 'result.success')
        require(abs(result.x - p_star) < 0.03, 'abs(result.x - p_star) < 0.03')
        require(3 < val < kappa_three + 0.03, '3 < val < kappa_three + 0.03')
        print(f"{q:.0e}, {result.x:.6f}, {val:.8f}, {val-kappa_three:+.6f}")
    print("All numerical sanity checks passed.")


if __name__ == "__main__":
    main()
