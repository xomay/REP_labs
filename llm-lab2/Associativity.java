import java.util.Locale;
import java.util.Random;

/** Experiences reproductibles : le pourcentage depend du domaine echantillonne. */
public final class Associativity {
    private static final long SEED = 20261102L;

    public static void main(String[] args) {
        int samples = args.length == 0 ? 1_000_000 : Integer.parseInt(args[0]);
        if (samples <= 0) {
            throw new IllegalArgumentException("Le nombre de triplets doit etre positif.");
        }
        Random random = new Random(SEED);
        long integers = 0, unit = 0, wide = 0, cancellation = 0;
        for (int i = 0; i < samples; i++) {
            int a = random.nextInt(), b = random.nextInt(), c = random.nextInt();
            if ((a + b) + c == a + (b + c)) integers++;
            double x = random.nextDouble(), y = random.nextDouble(), z = random.nextDouble();
            if (same(x, y, z)) unit++;
            x = wideDouble(random);
            y = wideDouble(random);
            z = wideDouble(random);
            if (same(x, y, z)) wide++;
            // Forte annulation : une petite valeur peut etre absorbee par -x.
            if (same(x, -x, random.nextDouble())) cancellation++;
        }
        System.out.printf("%d triplets par experience, graine %d%n", samples, SEED);
        report("int Java (addition modulo 2^32)", integers, samples);
        report("double, valeurs uniformes dans [0, 1)", unit, samples);
        report("double, signes et exposants varies", wide, samples);
        report("double, (x, -x, z), z dans [0, 1)", cancellation, samples);
        System.out.println("Sur les entiers et reels mathematiques exacts : 100 %.");
        System.out.println("Ces estimations ne sont pas une loi universelle pour double.");
        System.out.println("Exemple : (1e16 + -1e16) + 1 = " + ((1e16 + -1e16) + 1));
        System.out.println("          1e16 + (-1e16 + 1) = " + (1e16 + (-1e16 + 1)));
    }

    private static boolean same(double x, double y, double z) {
        return (x + y) + z == x + (y + z);
    }

    private static double wideDouble(Random random) {
        // Exposant uniforme entier dans [-500, 500], mantisse dans [1, 2).
        // Toutes les valeurs et sommes restent finies : pas de NaN ni d'infini.
        double value = Math.scalb(1.0 + random.nextDouble(), random.nextInt(1001) - 500);
        return random.nextBoolean() ? value : -value;
    }

    private static void report(String label, long matches, int samples) {
        System.out.printf(Locale.ROOT, "%s : %.6f %% (%d/%d)%n",
                label, 100.0 * matches / samples, matches, samples);
    }
}
