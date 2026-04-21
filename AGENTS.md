# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment

- Windows-only (depends on a local MIKE+ install via pythonnet/CLR).
- Requires a valid MIKE+ license to run most functionality.
- At import time, `mikeplus/__init__.py` loads the .NET runtime (`coreclr`) and resolves MIKE+ assemblies from `C:/Program Files (x86)/DHI/MIKE+/<year>` by default. Override with env var `MIKEPLUSPY_INSTALL_ROOT` pointing at the MIKE+ install root (parent of `bin`).
- `major_assembly_version` in `mikeplus/__init__.py` must match the installed MIKE+ year (23 = 2025, 24 = 2026, …). The package `version` in `pyproject.toml` is intentionally aligned with the MIKE+ year (e.g. `2026.0.0`).
- Known conflicts (enforced at import via `mikeplus/conflicts.py`):
  - Import order must be `mikeio` → `modelskill` → `mikeplus` → `mikeio1d`.
  - Importing `mikeio1d` before `mikeplus` raises `ImportError`.
  - `mikeio` in the same process warns. Set `MIKEPLUSPY_DISABLE_CONFLICT_CHECKS=true` to silence.

## Common commands

Install dev deps (uses `uv` + `hatchling`):

```bash
uv pip install -e ".[dev]"   # or .[test] / .[docs]
```

Tests (pytest) — note that `pyproject.toml` sets `addopts = ["-m not slow", "-s", ...]`, so by default slow tests are skipped:

```bash
pytest                                  # fast suite only
pytest -m "slow"                        # just the slow tests
pytest -m "not license_required and not slow"   # CI selector
pytest tests/database/test_tables.py::TestFoo::test_bar   # single test
```

Additional markers defined in `pyproject.toml`: `slow`, `license_required`, `timeout`, `skip_ci`.

Lint / format / typecheck:

```bash
ruff check .
ruff format .
mypy mikeplus
```

Ruff is configured (in `pyproject.toml`) to only include `pyproject.toml` and `mikeplus/**/*.py`, and to skip `mikeplus/tables/auto_generated/**` and notebooks. Mypy also ignores the auto-generated tables package and DHI/.NET modules.

Regenerate auto-generated table classes (after a MIKE+ version bump or schema change):

```bash
python scripts/generate_tables.py
```

Docs build (requires quarto installed separately):

```bash
uv run docs/generate_table_docs.py       # regenerate table docs sections
cd docs && uv run quartodoc build && uv run quarto render
```

## Architecture

Top-level entry points live on the `mikeplus` package:

- `mikeplus.open(path)` / `mikeplus.create(path, ...)` (`mikeplus/shortcuts.py`) construct a `Database`.
- `mikeplus.Database` (`mikeplus/database.py`) wraps the .NET `BaseDataSource` + `DataTableContainer` from `DHI.Amelia.DataModule`. It owns:
  - `tables` → `TableCollection` (auto-generated, see below).
  - `scenarios` → `ScenarioCollection` backed by a lazily-created .NET `ScenarioManager`.
  - `alternative_groups` → `AlternativeGroupCollection`.
  - `_runner` → `SimulationRunner` (`mikeplus/simulation_runner.py`), exposed via `db.run(...)` for CS / EPANET / SWMM engines via `DHI.Amelia.Tools.EngineTool`.

The database layer is a thin Python veneer over .NET objects:

- `mikeplus/tables/base_table.py` wraps a .NET `IMuTable`. One concrete subclass per MIKE+ table is generated into `mikeplus/tables/auto_generated/` (≈330 files). **Do not hand-edit auto-generated code** — regenerate via `scripts/generate_tables.py`, which uses Jinja templates in `scripts/table_templates/` and introspects a live (or temporary) MIKE+ database to discover columns.
- `mikeplus/queries.py` implements a fluent `SelectQuery / InsertQuery / UpdateQuery / DeleteQuery` API (`table.select().where(...).to_dataframe()`, etc.) that builds and executes SQL against the .NET data source.
- `mikeplus/dotnet.py` centralizes .NET interop helpers (type conversion, unwrapping proxy objects). Use `get_implementation()` / `DotNetConverter` rather than touching .NET types directly.
- `mikeplus/tools/` wraps individual MIKE+ GUI tools (ImportTool, TopoRepairTool, InterpolationTool, ConnectionRepairTool, CathSlopeLengthProcess). Each loads its own `DHI.Amelia.Tools.*` assembly on import.
- `mikeplus/scenarios/` models MIKE+ scenarios and alternative groups; construction is lazy because the underlying `ScenarioManager` requires the DB to be open.

When adding new functionality, prefer extending the existing Python wrappers around the .NET objects (`_net_table`, `_data_source`, etc.) rather than introducing parallel abstractions.

## Test fixtures

`tests/conftest.py` defines a ladder of DB fixtures at **session / module / class / function** scope for each test database in `tests/testdata/Db/`. Use the most coarse-grained scope that is safe:

- `session_*_db` / `module_*_db` / `class_*_db`: **read-only**, copied once per scope — fast, shared across tests. Modifications leak between tests in that scope.
- Plain `sirius_db` / `epanet_demo_db` / `swmm_db` / etc.: function-scoped fresh copy — use whenever the test mutates the DB.

Available DBs: `sirius`, `epanet_demo`, `swmm`, `flood`, `repair_tool`, `interpolate`, `connection_repair`, `catch_slope_len`, `import`, `river_junction_couple`. Any test that actually runs a MIKE+ simulation or calls licensed APIs should be marked `@pytest.mark.license_required` and `@pytest.mark.slow` as appropriate.

## Releasing for a new MIKE+ version

See `DEVELOPMENT.md` for the full checklist. Short version: set `MIKEPLUSPY_INSTALL_ROOT`, regenerate tables (`python scripts/generate_tables.py`), review the diff under `mikeplus/tables/auto_generated/`, bump the assembly version in `mikeplus/__init__.py`, bump `project.version` in `pyproject.toml` to the new MIKE+ year, regenerate `docs/_table_generated_sections.yml`, and run the full test suite + notebooks.

## Caution

MIKE+Py writes directly to `.sqlite` / `.mupp` files with no undo. When working with example or user-provided databases, operate on a copy (the test fixtures already do this).
