<!--
=============================================================================
SYNC IMPACT REPORT — sp.constitution run: 2026-03-01
=============================================================================
Version change:     1.0.0 → 1.0.1
Bump type:          PATCH — Sync Impact Report added; no semantic changes.

Modified principles:
  (none — all 6 principles unchanged)

Added sections:
  (none)

Removed sections:
  (none)

Placeholder tokens resolved:
  All placeholders filled during initial implementation (2026-03-01).
  Zero unresolved tokens found in this run.

Template alignment audit (2026-03-01):
  ✅ .specify/templates/plan-template.md
      "Constitution Check" gate (line 30-34) aligns with all 6 principles.
      Principle I (Test-First) maps to the gate: "Re-check after Phase 1 design."
      No update required.

  ✅ .specify/templates/spec-template.md
      User stories use P1/P2/P3 priority — matches project workflow.
      "Functional Requirements" section uses MUST language — matches Principle V.
      No update required.

  ✅ .specify/templates/tasks-template.md
      TDD rule ("Tests MUST be written and FAIL before implementation") — maps
      directly to Principle I (Test-First NON-NEGOTIABLE).
      Phase structure (Setup → Foundational → Stories → Polish) matches tasks.md.
      No update required.

  ✅ .specify/templates/checklist-template.md
      Generic structure; no project-specific principle references. Acceptable.
      No update required.

  ✅ .specify/templates/phr-template.prompt.md
      Stage/routing fields coherent with constitution governance requirements.
      No update required.

  ✅ .specify/templates/adr-template.md
      Not audited this run (ADR not yet created). Will align when /sp.adr runs.

Deferred TODOs:
  (none — all fields resolved)

Suggested commit message:
  docs: validate constitution v1.0.1 — sync impact report added (no semantic changes)
=============================================================================
-->

# MVP Ecommerce Store Constitution

## Core Principles

### I. Test-First (NON-NEGOTIABLE)

TDD MUST be followed for all implementation work:

- Tests MUST be written first, confirmed to FAIL, before any production code is written.
- The Red-Green-Refactor cycle is strictly enforced on every task.
- No production code may be introduced without a failing test that justifies it.
- Test fixtures MUST use an isolated in-memory SQLite database (never the real `instance/store.db`).

**Rationale**: Prevents regression, forces explicit thinking about behaviour before
implementation, and keeps the test suite as the living specification.

### II. Smallest Viable Change

- Every commit MUST change one logical thing; unrelated edits are forbidden.
- Speculative abstractions and premature generalisations are NOT permitted (YAGNI).
- Refactoring MUST be a separate commit from feature work.
- Only the scope defined in the active task (from `tasks.md`) MUST be implemented.

**Rationale**: Keeps diffs reviewable, reduces blast radius of bugs, and maintains
a clear traceability chain from task → commit → test.

### III. Security by Default

- Raw SQL is FORBIDDEN; all database access MUST use the SQLAlchemy ORM
  (parameterised queries only).
- Secrets (keys, passwords, tokens) MUST NOT appear in source code;
  use `.env` + `python-dotenv`.
- All user-supplied inputs (query strings, form fields) MUST be validated at
  the route layer before use.
- `.gitignore` MUST cover: `instance/`, `.env`, `__pycache__/`, `*.pyc`, `*.db`.

**Rationale**: Eliminates the most common web vulnerability classes (SQL injection,
credential leakage) by default, not by discipline.

### IV. Flask Application Factory

- All Flask application setup MUST live inside `create_app()` in `app/__init__.py`.
- Configuration MUST be loaded from environment variables (via `python-dotenv`).
- All extensions (SQLAlchemy, etc.) MUST be initialised using the `init_app()` pattern,
  never at module import time.
- Features MUST be organised as Flask Blueprints (e.g., `catalog_bp`), registered
  inside `create_app()`.

**Rationale**: Enables multiple app instances (test isolation), clean config per
environment, and avoids circular imports.

### V. Readable, Maintainable Code

- Code MUST comply with PEP 8; maximum line length is 100 characters.
- Variable and function names MUST be fully descriptive; abbreviations are
  only permitted for established conventions (`db`, `app`, `p` in loops).
- Jinja2 templates MUST use inheritance from `base.html`; inline `style=` attributes
  are forbidden.
- All frontend logic MUST reside in `static/js/`; all custom CSS in `static/css/`.

**Rationale**: Lowers the cost of future changes and onboarding; separates concerns
between Python logic and presentation.

### VI. Separation of Concerns

- `app/models.py` MUST contain only data definitions and column declarations —
  no HTTP logic, no business rules.
- Route handlers in `app/routes/` MUST only handle HTTP in/out and delegate
  to model queries; they MUST NOT contain SQL-like filter expressions directly.
- Jinja2 templates MUST only handle display — no computed values, no conditionals
  beyond simple `if/for` on passed context variables.
- Seed data MUST be isolated in `seeds/products.py` and never embedded in application
  startup code directly.

**Rationale**: Each layer can be tested, replaced, or extended independently.

## Technology Standards

| Concern      | Choice                                      | Notes                          |
|--------------|---------------------------------------------|--------------------------------|
| Backend      | Flask 3.x + Flask-SQLAlchemy 3.x            | Application factory pattern    |
| Database     | SQLite 3 (development)                      | File: `instance/store.db`      |
| Frontend     | Jinja2 + Bootstrap 5.3 CDN + Vanilla JS     | No build step                  |
| Testing      | pytest 8.x + pytest-flask 1.x               | In-memory SQLite fixtures      |
| Python       | 3.14 (`.venv/` at project root)             | PEP 8, max 100 chars/line      |
| Config       | `python-dotenv` loading `.env`              | Never commit `.env`            |

## Development Workflow

1. Pick a task from `specs/<feature>/tasks.md` and mark it `in_progress`.
2. Write the test(s) for that task — confirm RED (tests FAIL).
3. Implement the minimum code to make the tests GREEN.
4. Refactor if needed (tests MUST remain GREEN throughout).
5. Commit with a clear message referencing the task ID (e.g., `feat: T015 catalog index route`).
6. Mark the task `completed` in `tasks.md`.

## Governance

This constitution supersedes all other development practices in this project.

**Amendment procedure**:
- Amendments require a written rationale added to this file.
- `LAST_AMENDED_DATE` MUST be updated on every change.
- `CONSTITUTION_VERSION` MUST be bumped following semantic versioning:
  - MAJOR: removal or redefinition of a principle (backward-incompatible governance change).
  - MINOR: new principle or section added, or materially expanded guidance.
  - PATCH: clarifications, wording, or non-semantic refinements.

**Compliance**:
- All implementation tasks MUST reference the task ID they satisfy.
- All PRs/commits MUST be reviewed against the 6 principles above.
- Complexity violations (e.g., extra abstraction layers) MUST be justified in
  `specs/<feature>/plan.md` under a "Complexity Tracking" table.

**Version**: 1.0.1 | **Ratified**: 2026-03-01 | **Last Amended**: 2026-03-01
