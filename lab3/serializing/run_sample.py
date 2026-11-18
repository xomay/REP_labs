import argparse
import csv
import os
import platform
import shlex
import subprocess
import sys
from pathlib import Path
from jinja2 import Template

base_dir = Path(__file__).resolve().parent
runs = 5
years = 50
precision = 100

parser = argparse.ArgumentParser(description="Generate and run sampled banking variants.")
parser.add_argument("--sample", type=Path, default=base_dir.parent / "configs/sample.csv")
parser.add_argument("--output", type=Path, default=base_dir / "results.csv")
parser.add_argument("--strict", action="store_true", help="fail instead of skipping unavailable runtimes")
args = parser.parse_args()

# Change these paths if the runtimes are installed elsewhere.
python_versions = {
    "CPython": sys.executable,
    "PyPy": os.environ.get("PYTHON_PYPY", "pypy3"),
    "Python3-10": "python3.10",
    "Python3-11": "python3.11",
    "Python3-12": "python3.12",
}
java_versions = {
    "Java 17": os.environ.get("JAVA_17", "/usr/lib/jvm/java-17-openjdk-amd64/bin/java"),
    "Java 21": os.environ.get("JAVA_21", "/usr/lib/jvm/java-21-openjdk-amd64/bin/java"),
}


def execute(command):
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return (result.stdout + result.stderr).strip()


args.output.parent.mkdir(parents=True, exist_ok=True)
with args.sample.open(newline="") as sample, args.output.open("w", newline="") as results:
    reader = csv.DictReader(sample)
    columns = reader.fieldnames + ["run", "years", "precision", "machine", "system",
                                  "architecture", "runner", "runtime", "command", "answer"]
    writer = csv.DictWriter(results, fieldnames=columns)
    writer.writeheader()

    for config in reader:
        folder = base_dir / "generated" / config["config_id"]
        folder.mkdir(parents=True, exist_ok=True)
        try:
            if config["Language"] == "Java":
                java = java_versions[config["JavaVersion"]]
                runtime = execute([java, "-version"]).splitlines()[0]
                template = Template((base_dir / "Banking.java.jinja").read_text())
                source = folder / "Banking.java"
                source.write_text(template.render(implementation=config["Implementation"]))
                execute([str(Path(java).with_name("javac")), str(source)])
                command = [java, "-cp", str(folder), "Banking"]
            else:
                version = config["PythonVersion"] or config["Python"]
                python = python_versions[version]
                runtime = execute([python, "--version"])
                template = Template((base_dir / "banking.py.jinja").read_text())
                source = folder / "banking.py"
                source.write_text(template.render(implementation=config["Implementation"]))
                command = [python, str(source)]
            command += [str(years), str(precision)]

            for run in range(1, runs + 1):
                answer = execute(command)
                writer.writerow({**config, "run": run, "years": years,
                                 "precision": precision, "machine": platform.node(),
                                 "system": platform.platform(), "runtime": runtime,
                                 "architecture": platform.machine(),
                                 "runner": os.environ.get("RUNNER_LABEL", "local"),
                                 "command": shlex.join(command), "answer": answer})
            print(config["config_id"], "done")
        except (OSError, subprocess.CalledProcessError) as error:
            print(config["config_id"], "could not run:", error)
            if args.strict:
                raise

print("Results saved in", args.output)
