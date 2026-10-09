import ast
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[2] / "src"
GUI_DIR = SRC_DIR / "tracker_tool_gui"
CORE_DIR = SRC_DIR / "tracker_tool"

# docs/gui/GUI_DEVELOPMENT_PLAN.md §3: the GUI may use only the Core
# integration boundary. It never imports readers, writers, Canonical
# validation, or conversion orchestration directly.
ALLOWED_CORE_MODULES = {
    "tracker_tool.app",
    "tracker_tool.config",
    "tracker_tool.contract",
}

# Contract values owned by Core. The GUI must import them from
# tracker_tool.contract instead of defining its own copies.
CORE_CONTRACT_LITERALS = {
    "3DE_R5",
    "PFTRACK_2017",
    "SYNTHEYES_2304",
    "AUTOTRACK",
    "USERTRACK",
    "MISSING_REQUIRED_SHOT_METADATA",
    "INVALID_SHOT_METADATA",
    "OBSERVATION_OUTSIDE_SHOT_RANGE",
    "CROSS_SOURCE_TRACK_NAME_COLLISION",
    "SAME_SOURCE_CONVERSION_NOT_ALLOWED",
    "UNSUPPORTED_SOURCE_SOFTWARE",
    "UNSUPPORTED_TARGET_SOFTWARE",
}


def _python_files(directory):
    files = sorted(directory.rglob("*.py"))

    assert files

    return files


def _imported_modules(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name

        elif isinstance(node, ast.ImportFrom) and node.level == 0:
            yield node.module

            for alias in node.names:
                yield f"{node.module}.{alias.name}"


def _is_module_or_submodule(module, package):
    return module == package or module.startswith(f"{package}.")


def test_gui_imports_only_the_core_integration_boundary():
    violations = [
        f"{path.name}: {module}"
        for path in _python_files(GUI_DIR)
        for module in _imported_modules(path)
        if _is_module_or_submodule(module, "tracker_tool")
        and module != "tracker_tool"
        and not any(
            _is_module_or_submodule(module, allowed)
            for allowed in ALLOWED_CORE_MODULES
        )
    ]

    assert violations == []


def test_gui_does_not_import_core_package_root():
    # "from tracker_tool import x" is checked as "tracker_tool.x" above;
    # a bare "import tracker_tool" would expose everything.
    violations = [
        path.name
        for path in _python_files(GUI_DIR)
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8")))
        if isinstance(node, ast.Import)
        and any(alias.name == "tracker_tool" for alias in node.names)
    ]

    assert violations == []


def test_gui_does_not_define_core_contract_literals():
    violations = [
        f"{path.name}: {node.value}"
        for path in _python_files(GUI_DIR)
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8")))
        if isinstance(node, ast.Constant)
        and node.value in CORE_CONTRACT_LITERALS
    ]

    assert violations == []


def test_core_does_not_import_gui():
    violations = [
        f"{path.name}: {module}"
        for path in _python_files(CORE_DIR)
        for module in _imported_modules(path)
        if _is_module_or_submodule(module, "tracker_tool_gui")
    ]

    assert violations == []
