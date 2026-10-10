"""Deterministic synthetic pilot fixtures; held-out tests stay outside agent workspace."""
from pathlib import Path

TASKS = {
    "bug-fix": {
        "objective": "Fix clamp so values below lower bound return lower and above upper return upper.",
        "starter": "def clamp(value, low, high):\n    return min(low, max(value, high))\n",
        "tests": "from app import clamp\nassert clamp(2, 0, 10) == 2\nassert clamp(-3, 0, 10) == 0\nassert clamp(20, 0, 10) == 10\n",
    },
    "test-addition": {
        "objective": "Add tests/test_app.py using unittest for is_even, including negative, zero, and odd inputs. Do not modify app.py.",
        "starter": "def is_even(number):\n    return number % 2 == 0\n",
        "tests": "from pathlib import Path\nimport unittest\np = Path('tests/test_app.py')\nassert p.is_file()\nsource = p.read_text()\nassert 'unittest' in source and 'assert' in source\nsuite = unittest.defaultTestLoader.discover('tests')\nresult = unittest.TextTestRunner(verbosity=0).run(suite)\nassert result.wasSuccessful() and result.testsRun >= 3\n",
    },
    "refactoring": {
        "objective": "Refactor total_cost to remove the explicit loop while preserving results and signature.",
        "starter": "def total_cost(prices):\n    total = 0\n    for price in prices:\n        total += price\n    return total\n",
        "tests": "from app import total_cost\nimport ast\nfrom pathlib import Path\nassert total_cost([]) == 0\nassert total_cost([2, 3, 5]) == 10\ntree = ast.parse(Path('app.py').read_text())\nfn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'total_cost')\nassert not any(isinstance(n, (ast.For, ast.While)) for n in ast.walk(fn))\n",
    },
    "documentation": {
        "objective": "Add README.md explaining how to call slugify, its input and output, and one executable Python example.",
        "starter": "def slugify(text):\n    return '-'.join(text.lower().split())\n",
        "tests": "from pathlib import Path\np = Path('README.md')\nassert p.is_file()\ns = p.read_text().lower()\nassert 'slugify' in s and 'python' in s and 'hello' in s\n",
    },
    "feature": {
        "objective": "Add unique_sorted(values) to app.py; return sorted distinct values without modifying the input.",
        "starter": "def identity(value):\n    return value\n",
        "tests": "from app import unique_sorted\nvalues = [3, 1, 3, 2]\nassert unique_sorted(values) == [1, 2, 3]\nassert values == [3, 1, 3, 2]\nassert unique_sorted([]) == []\n",
    },
}


def materialize_fixture(name, workspace, evaluator):
    if name not in TASKS:
        raise ValueError("Unknown synthetic task")
    workspace = Path(workspace)
    evaluator = Path(evaluator)
    if workspace.resolve() == evaluator.resolve() or workspace.exists() or evaluator.exists():
        raise ValueError("Workspace and evaluator must be distinct, absent destinations")
    task = TASKS[name]
    workspace.mkdir(parents=True)
    evaluator.mkdir(parents=True)
    (workspace / "app.py").write_text(task["starter"], encoding="utf-8")
    (workspace / "TASK.md").write_text(task["objective"] + "\n", encoding="utf-8")
    (evaluator / "acceptance.py").write_text(task["tests"], encoding="utf-8")
    return {"task": name, "workspace": str(workspace), "evaluator": str(evaluator)}
