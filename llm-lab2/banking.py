"""Placement initial e exact ; frais avant chaque multiplication annuelle."""

import math
from decimal import Decimal, ROUND_HALF_UP, localcontext


def stable_balance(years=50, cutoff=250, precision=100):
    """B_n = n! * somme_{k=n+1}^infini 1/k!, sans annulation numerique."""
    with localcontext() as ctx:
        ctx.prec = precision
        tail = Decimal(0)
        # B_n = (1 + (1 + (1 + ...)/(n+3))/(n+2))/(n+1).
        for k in range(cutoff, years, -1):
            tail = (1 + tail) / k
        return tail


def main():
    with localcontext() as ctx:
        ctx.prec = 100
        balance = stable_balance()
        withdrawal = balance - 1
        print("Capital initial : e exact ; duree : 50 ans.")
        print(f"Solde avant retrait : {balance} EUR")
        print(f"Apres le frais de retrait de 1 EUR : {withdrawal} EUR")
        cents = withdrawal.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        print(f"Arrondi au centime : {cents} EUR")
        print("Le solde ne couvre meme pas le frais de retrait.")

        reference = stable_balance(cutoff=350, precision=120)
        if abs(balance - reference) > Decimal("1e-98"):
            raise ArithmeticError("Precision insuffisante")

    naive = math.e
    for year in range(1, 51):
        naive = (naive - 1) * year
    print(f"Calcul naif avec math.e et float, apres retrait : {naive - 1:.17g} EUR")


if __name__ == "__main__":
    main()
