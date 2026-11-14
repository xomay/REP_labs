import subprocess
import sys
from pathlib import Path
from jinja2 import Template

base_dir = Path(__file__).resolve().parent
template = Template((base_dir / "propcheck.py.jinja").read_text())
properties = {"assoc_add": ("(x + y) + z", "x + (y + z)"),
              "assoc_mul": ("(x * y) * z", "x * (y * z)"),
              "distri_mul": ("x * (y + z)", "x * y + x * z")}
output_dir = base_dir / "generated"
output_dir.mkdir(exist_ok=True)
for name, (lhs, rhs) in properties.items():
    path = output_dir / f"{name}.py"
    path.write_text(template.render(lhs=lhs, rhs=rhs, repetitions=10000))
    result = subprocess.run([sys.executable, path], capture_output=True, text=True)
    print(name, result.stdout.strip())
