"""Exhaustive census of the four-dimensional cube and high-precision profile constants.

Requires mpmath for the root solves. The finite cube census uses integers
for weights and equality sets, with floating-point supporting deficits.
"""
from itertools import product
from math import sqrt
from collections import defaultdict
import mpmath as mp


def require(condition, detail="check failed"):
    """Fail loudly even under python -O (no reliance on assert)."""
    if not condition:
        print("CHECK FAILED:", detail)
        raise SystemExit(1)

def run():
    n=4
    points=list(product((-1,1), repeat=n))
    masses=defaultdict(int)
    maximisers=defaultdict(list)
    for mask in range(1<<len(points)):
        values=[sum(points[j][k] for j in range(len(points)) if (mask>>j)&1) for k in range(n)]
        mass=mask.bit_count()
        weight=sum(v*v for v in values)
        deficit=(sqrt(2)-1)/4-sqrt(weight)/16+mass/16
        require(deficit>=-1e-14, 'deficit>=-1e-14')
        triple_deficit=1/(8*sqrt(3))-sqrt(weight)/16+(2/sqrt(3))*mass/16
        require(triple_deficit>=-1e-14, 'triple_deficit>=-1e-14')
        if weight>masses[mass]:
            masses[mass]=weight
            maximisers[mass]=[mask]
        elif weight==masses[mass]:
            maximisers[mass].append(mask)
    faces=set()
    for i in range(n):
        for j in range(i+1,n):
            for si,sj in product((-1,1),repeat=2):
                faces.add(sum(1<<v for v,x in enumerate(points) if x[i]==si and x[j]==sj))
    require(masses[4]==32, 'masses[4]==32')
    require(set(maximisers[4])==faces, 'set(maximisers[4])==faces')
    edges=set()
    for free in range(n):
        fixed=[i for i in range(n) if i!=free]
        for signs in product((-1,1),repeat=n-1):
            edges.add(sum(1<<v for v,x in enumerate(points)
                          if all(x[i]==s for i,s in zip(fixed,signs))))
    require(masses[2]==12, 'masses[2]==12')
    require(set(maximisers[2])==edges, 'set(maximisers[2])==edges')
    print('All 65,536 subsets of the four-dimensional sign cube verified.')
    print('Supporting deficit nonnegative within 1e-14 floating tolerance.')
    print('Exact quarter-density maximum numerator:', masses[4], 'over denominator 256.')
    print('Exact maximisers:', len(maximisers[4]), 'two-coordinate faces.')
    print('Exact eighth-density maximum numerator:', masses[2], 'over denominator 256.')
    print('Exact eighth-density maximisers:',len(maximisers[2]),'one-dimensional faces.')
    print('Both supporting deficits numerically verified.')
    print('Exact weight numerators by mass:',dict(sorted(masses.items())))


def check_profile_constants():
    """Reproduce the stationary allocations and both forms of each constant."""
    with mp.workdps(80):
        tolerance = mp.mpf("1e-70")
        magnetisation = mp.findroot(
            lambda value: value - mp.tanh(2 * value),
            (mp.mpf("0.9"), mp.mpf("0.99")),
        )
        fraction = (1 + magnetisation) / 2
        entropy_two = (
            -fraction * mp.log(fraction)
            -(1 - fraction) * mp.log(1 - fraction)
        )
        kappa_two = 2 * entropy_two + 2 * magnetisation ** 2
        kappa_two_general = (
            -2 + 4 * (fraction ** 2 + (1 - fraction) ** 2)
            + 2 * entropy_two
        )
        require(0 < magnetisation < 1, '0 < magnetisation < 1')
        require(abs(magnetisation - mp.tanh(2 * magnetisation)) < tolerance, 'abs(magnetisation - mp.tanh(2 * magnetisation)) < tolerance')
        require(abs(mp.log(fraction / (1 - fraction))
                    - 4 * magnetisation) < tolerance, "two-face stationarity")
        require(abs(kappa_two - kappa_two_general) < tolerance, 'abs(kappa_two - kappa_two_general) < tolerance')
        require(16 - 2 / (fraction * (1 - fraction)) < 0, '16 - 2 / (fraction * (1 - fraction)) < 0')
        require(kappa_two > max(mp.mpf(2), 2 * mp.log(2)), 'kappa_two > max(mp.mpf(2), 2 * mp.log(2))')

        dominant = mp.findroot(
            lambda value: mp.log(2 * value / (1 - value)) - 6 * value + 2,
            (mp.mpf("0.9"), mp.mpf("0.97")),
        )
        minor = (1 - dominant) / 2
        entropy_three = (
            -dominant * mp.log(dominant) - 2 * minor * mp.log(minor)
        )
        kappa_three = (
            -1 + 4 * (dominant ** 2 + 2 * minor ** 2)
            + 2 * entropy_three
        )
        kappa_three_reduced = (
            -1 + 4 * dominant ** 2 + 2 * (1 - dominant) ** 2
            - 2 * dominant * mp.log(dominant)
            - 2 * (1 - dominant) * mp.log((1 - dominant) / 2)
        )
        require(mp.mpf(1) / 3 < dominant < 1, 'mp.mpf(1) / 3 < dominant < 1')
        require(abs(mp.log(2 * dominant / (1 - dominant))
                    - 6 * dominant + 2) < tolerance, "three-face root equation")
        require(abs(4 * dominant - mp.log(dominant)
                    - 4 * minor + mp.log(minor)) < tolerance, "three-face stationarity")
        require(abs(kappa_three - kappa_three_reduced) < tolerance, 'abs(kappa_three - kappa_three_reduced) < tolerance')
        require(12 - 2 / (dominant * (1 - dominant)) < 0, '12 - 2 / (dominant * (1 - dominant)) < 0')
        require(kappa_three > max(mp.mpf(3), mp.mpf(1) / 3 + 2 * mp.log(3)), 'kappa_three > max(mp.mpf(3), mp.mpf(1) / 3 + 2 * mp.log(3))')

        gaussian_two = 2 - mp.log(64 * mp.pi)
        gaussian_three = 2 - mp.log(256 * mp.pi)
        require(abs(gaussian_three - gaussian_two + mp.log(4)) < tolerance, 'abs(gaussian_three - gaussian_two + mp.log(4)) < tolerance')
        values = (
            ("m_star", magnetisation),
            ("lambda_star", fraction),
            ("kappa_2", kappa_two),
            ("p_star", dominant),
            ("each_minor_fraction", minor),
            ("kappa_3", kappa_three),
            ("2-log(64*pi)", gaussian_two),
            ("2-log(256*pi)", gaussian_three),
        )
        print("Profile constants calculated with 80 decimal digits of precision.")
        for name, value in values:
            print(f"{name} = {mp.nstr(value, 42)}")
        print("Stationarity and equivalent formula residuals are below 1e-70.")
        print("Both allocation second derivatives are negative.")
        print("Both constants exceed their uniform and endpoint values.")
        print("All high-precision constant checks passed.")


if __name__=='__main__':
    run()
    check_profile_constants()
