"""L'associativite depend du type de nombres et de leur distribution."""

import argparse
import math
import random


def wide_float(rng):
    """Mantisse uniforme dans [1, 2), exposant entier dans [-500, 500]."""
    value = math.ldexp(1.0 + rng.random(), rng.randint(-500, 500))
    return value if rng.getrandbits(1) else -value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("samples", nargs="?", type=int, default=1_000_000)
    args = parser.parse_args()
    if args.samples <= 0:
        parser.error("le nombre de triplets doit etre positif")

    seed = 20261102
    rng = random.Random(seed)
    counts = [0, 0, 0, 0]
    for _ in range(args.samples):
        # Les int Python ont une precision arbitraire : aucune perte par debordement.
        a, b, c = (rng.randint(-(2**63), 2**63 - 1) for _ in range(3))
        counts[0] += (a + b) + c == a + (b + c)
        x, y, z = (rng.random() for _ in range(3))
        counts[1] += (x + y) + z == x + (y + z)
        x, y, z = (wide_float(rng) for _ in range(3))
        counts[2] += (x + y) + z == x + (y + z)
        z = rng.random()
        counts[3] += (x + -x) + z == x + (-x + z)

    print(f"{args.samples} triplets par experience, graine {seed}")
    labels = (
        "int Python (entiers exacts)",
        "float, valeurs uniformes dans [0, 1)",
        "float, signes et exposants varies",
        "float, (x, -x, z), z dans [0, 1)",
    )
    for label, count in zip(labels, counts):
        print(f"{label} : {100 * count / args.samples:.6f} % ({count}/{args.samples})")
    print("Sur les reels mathematiques exacts : 100 %.")
    print("Ces estimations ne sont pas une loi universelle pour float.")
    x, y, z = 1e16, -1e16, 1.0
    print(f"Exemple : (1e16 + -1e16) + 1 = {(x + y) + z}")
    print(f"          1e16 + (-1e16 + 1) = {x + (y + z)}")


if __name__ == "__main__":
    main()
