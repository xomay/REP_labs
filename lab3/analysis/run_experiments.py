"""Produce CSV evidence OUTSIDE the notebook. Run with Python 3.12 and Jinja2."""

import csv
import hashlib
import math
import os
import platform
import random
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from decimal import Decimal, localcontext
from pathlib import Path

from jinja2 import Template

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
TEMPLATES = BASE.parent / "serializing"
STAMP = datetime.now(timezone.utc).isoformat()


def tail(years, precision, cutoff=500):
    with localcontext() as ctx:
        ctx.prec = precision
        balance = Decimal(0)
        for k in range(cutoff, years, -1):
            balance = (1 + balance) / k
        return balance


def save(name, rows):
    with (DATA / name).open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(name, len(rows), "rows")


def main():
    DATA.mkdir(exist_ok=True)
    references = []
    with localcontext() as ctx:
        ctx.prec = 180
        for years in (10, 30, 50):
            after = tail(years, 180)
            assert abs(after - tail(years, 200, 600)) < Decimal("1e-175")
            before = 1 + after
            references.append(dict(years=years, before_fee=str(before),
                                   after_fee=str(after), precision=180, cutoff=500))
    save("references.csv", references)

    rows = []
    runtime_ids = {}

    def record(experiment, runtime_id, language, implementation, precision, answer,
               run=1, years=50, fee=1, delta="0"):
        rows.append(dict(experiment=experiment, runtime_id=runtime_id, language=language,
                         implementation=implementation, precision=precision, years=years,
                         withdrawal_fee=fee, initial_delta=delta, run=run, answer=str(answer),
                         runtime=runtime_ids[runtime_id], architecture=platform.machine(),
                         system=platform.platform(), timestamp_utc=STAMP))

    python_version = subprocess.check_output([sys.executable, "--version"], text=True).strip()
    runtime_ids["CPython"] = python_version
    runtimes = [("CPython", "Python", sys.executable, ["math_exp", "Decimal_exp"])]
    for version in (17, 21):
        java = os.environ.get(f"JAVA_{version}",
                              f"/usr/lib/jvm/java-{version}-openjdk-amd64/bin/java")
        runtime_ids[f"Java{version}"] = subprocess.check_output(
            [java, "-version"], stderr=subprocess.STDOUT, text=True).splitlines()[0]
        runtimes.append((f"Java{version}", "Java", java, ["Math_E", "BigDecimal"]))

    # Same generated programs as the original experiment, now sweeping precision.
    with tempfile.TemporaryDirectory(prefix="rep-causal-") as tmp:
        for runtime_id, language, executable, implementations in runtimes:
            for implementation in implementations:
                java = language == "Java"
                filename = "Banking.java" if java else "banking.py"
                source = Path(tmp) / filename
                source.write_text(Template((TEMPLATES / (filename + ".jinja")).read_text())
                                  .render(implementation=implementation))
                if java:
                    subprocess.run([str(Path(executable).with_name("javac")), str(source)],
                                   check=True, capture_output=True, text=True)
                command = ([executable, "-cp", tmp, "Banking"] if java
                           else [executable, str(source)])
                for precision in (16, 28, 50, 65, 80, 100, 120):
                    for run in (1, 2, 3):
                        answer = subprocess.check_output(command + ["50", str(precision)], text=True).strip()
                        record("precision", runtime_id, language, implementation, precision, answer, run)

    # Algorithm intervention: same language, precision, years and withdrawal fee.
    for precision in (16, 28, 50, 65, 80, 100, 120):
        with localcontext() as ctx:
            ctx.prec = precision
            record("algorithm", "CPython", "Python", "stable_tail", precision,
                   tail(50, precision))

    # Initial-condition intervention: high precision held fixed, change only delta.
    with localcontext() as ctx:
        ctx.prec = 180
        e = Decimal(1).exp()
        for years in (10, 30, 50):
            for delta in ("0", "1e-80", "-1e-80", "1e-40", "-1e-40"):
                balance = e + Decimal(delta)
                for year in range(1, years + 1):
                    balance = (balance - 1) * year
                record("initial_delta", "CPython", "Python", "forward_decimal", 180,
                       balance - 1, years=years, delta=delta)
        # Withdrawal intervention: one completed trajectory, toggle only the final fee.
        balance = e
        for year in range(1, 51):
            balance = (balance - 1) * year
        for fee in (0, 1):
            record("withdrawal_fee", "CPython", "Python", "forward_decimal", 180,
                   balance - fee, fee=fee)
        # Isolate the initial binary64 approximation from subsequent float rounding.
        for initial in (e, Decimal.from_float(math.e)):
            balance = initial
            for year in range(1, 51):
                balance = (balance - 1) * year
            record("rounded_initial", "CPython", "Python", "forward_decimal", 180,
                   balance - 1, delta=str(initial - e))
    save("causal_banking.csv", rows)

    association = []
    for samples in (10_000, 100_000):
        for seed in (1, 2, 3):
            for mode in ("float_unit", "decimal_unit_exact", "float_wide",
                         "float_cancellation", "int_exact"):
                rng = random.Random(seed)
                matches = 0
                with localcontext() as ctx:
                    ctx.prec = 100  # Enough to add exactly the sampled dyadic fractions.
                    for _ in range(samples):
                        if mode in ("float_unit", "decimal_unit_exact"):
                            x, y, z = (rng.random() for _ in range(3))
                            if mode == "decimal_unit_exact":
                                x, y, z = map(Decimal.from_float, (x, y, z))
                        elif mode == "float_wide":
                            x, y, z = (math.ldexp(rng.uniform(-2, 2), rng.randint(-500, 500))
                                       for _ in range(3))
                        elif mode == "float_cancellation":
                            x, y, z = 1e16, -1e16, rng.random()
                        else:
                            x, y, z = (rng.randint(-10**30, 10**30) for _ in range(3))
                        matches += (x + y) + z == x + (y + z)
                association.append(dict(mode=mode, samples=samples, seed=seed, matches=matches,
                                        percent=100 * matches / samples, runtime=python_version,
                                        architecture=platform.machine(), timestamp_utc=STAMP))
    save("causal_associativity.csv", association)

    sources = [Path(__file__), TEMPLATES / "banking.py.jinja", TEMPLATES / "Banking.java.jinja"]
    save("provenance.csv", [dict(path=str(p.relative_to(BASE.parent.parent)),
                                 sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                                 timestamp_utc=STAMP) for p in sources])


if __name__ == "__main__":
    main()
