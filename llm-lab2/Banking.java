import java.math.BigDecimal;
import java.math.MathContext;
import java.math.RoundingMode;
import java.util.Locale;

/** Frais preleves AVANT la multiplication annuelle ; capital initial = e exact. */
public final class Banking {
    public static void main(String[] args) {
        final int years = 50;
        MathContext mc = new MathContext(100, RoundingMode.HALF_EVEN);
        BigDecimal balance = stableBalance(years, 250, mc);
        BigDecimal withdrawal = balance.subtract(BigDecimal.ONE);
        System.out.println("Capital initial : e exact ; duree : 50 ans.");
        System.out.println("Solde avant retrait : " + balance.toPlainString() + " EUR");
        System.out.println("Apres le frais de retrait de 1 EUR : "
                + withdrawal.toPlainString() + " EUR");
        System.out.println("Arrondi au centime : "
                + withdrawal.setScale(2, RoundingMode.HALF_UP) + " EUR");
        System.out.println("Le solde ne couvre meme pas le frais de retrait.");

        double naive = Math.E;
        for (int year = 1; year <= years; year++) naive = (naive - 1) * year;
        System.out.printf(Locale.ROOT,
                "Calcul naif avec Math.E et double, apres retrait : %.17g EUR%n", naive - 1);

        // Controle avec une troncature plus longue et davantage de precision.
        BigDecimal reference = stableBalance(years, 350,
                new MathContext(120, RoundingMode.HALF_EVEN));
        if (balance.subtract(reference).abs().compareTo(BigDecimal.ONE.scaleByPowerOfTen(-98)) > 0) {
            throw new AssertionError("Precision insuffisante");
        }
    }

    private static BigDecimal stableBalance(int years, int cutoff, MathContext mc) {
        // B_n = n! (e - somme_{k=0}^n 1/k!)
        //     = 1/(n+1) * (1 + 1/(n+2) * (1 + ...)).
        // La forme imbriquee evite la soustraction de nombres presque egaux.
        BigDecimal tail = BigDecimal.ZERO;
        for (int k = cutoff; k > years; k--) {
            tail = BigDecimal.ONE.add(tail, mc).divide(BigDecimal.valueOf(k), mc);
        }
        return tail;
    }
}
