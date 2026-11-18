Run from the repository root:

```bash
.env/bin/python lab3/serializing/run_sample.py
```

The script reads `../configs/sample.csv`, fills the banking templates, compiles
Java when needed, and runs each configuration five times. It saves the generated
programs in `generated/` and the results in `results.csv`.

The CSV contains the original factors, run number, years, precision, machine,
system, CPU architecture, runner, actual runtime version, command to repeat the run,
and answer.
Unavailable runtimes are reported in the terminal and skipped.
Edit the runtime paths and the three settings at the top of the script as needed.
`PYTHON_PYPY`, `JAVA_17` and `JAVA_21` can override the runtime executable paths.
Use `--sample path.csv` and `--output path.csv` to choose the input and output.
`--strict` fails on unavailable runtimes instead of skipping them.

All variants use `(balance - 1) * year`, starting from e, then subtract a final
one-euro fee. BigDecimal computes e using a Taylor series. Banking is deterministic,
so repeated runs of a configuration normally give the same answer.

## GitHub Actions

The `Banking results` workflow runs on pushes affecting `lab3` or its workflow,
and can also be started manually from the Actions tab.
Its matrix uses `ubuntu-24.04` (x86_64) and `ubuntu-24.04-arm` (ARM64).
Each runner installs CPython 3.10, 3.11 and 3.12, PyPy 3.10, and Temurin Java 17
and 21. CPython defaults to 3.12.

Each job samples the 14 configurations of `Banking.uvl` with seed 1, generates
the variants and runs each five times (50 years, precision 100). Missing runtimes
or failed variants fail the job. Each runner produces 70 result rows.

The final job downloads the CSV artifacts and commits the samples and results
to `lab3/serializing/results/` on the triggering branch, with one pair of files
per runner. These files are replaced on the next run; Git preserves their history.
Only this job has `contents: write`. The branch must allow the Actions bot to push.
Pushes containing only these CSV files do not trigger another experiment.
