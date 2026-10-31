"""Optional command-line runner. Normally use Jupyter's Run All Cells button.

Executes the notebook in-process with IPython, saves actual outputs, and exports
models/results/report through the notebook's own cells. No backend code is used.
"""

from pathlib import Path
import os
import nbformat
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output

ROOT = Path(__file__).resolve().parent
path = ROOT / "notebook/ML_Lab_Project.ipynb"
notebook = nbformat.read(path, as_version=4)
os.chdir(path.parent)
shell = InteractiveShell.instance()
count = 0
for cell in notebook.cells:
    if cell.cell_type != "code":
        continue
    count += 1
    with capture_output() as captured:
        result = shell.run_cell(cell.source, store_history=False)
    if result.error_before_exec or result.error_in_exec:
        print(captured.stdout, captured.stderr)
        raise RuntimeError(f"Notebook code cell {count} failed. See the error above.")
    cell.execution_count = count
    outputs = []
    if captured.stdout:
        outputs.append(
            nbformat.v4.new_output("stream", name="stdout", text=captured.stdout)
        )
    if captured.stderr:
        outputs.append(
            nbformat.v4.new_output("stream", name="stderr", text=captured.stderr)
        )
    for item in captured.outputs:
        outputs.append(
            nbformat.v4.new_output(
                "display_data", data=item.data, metadata=item.metadata
            )
        )
    cell.outputs = outputs
    print(f"Completed code cell {count}", flush=True)
nbformat.validate(notebook)
nbformat.write(notebook, path)
print(
    f"All {count} code cells passed; notebook outputs, models and report saved.",
    flush=True,
)
