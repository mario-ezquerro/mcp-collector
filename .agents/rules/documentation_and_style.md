# Documentation and Language Guidelines

## 1. Language Policy
- **Universal English**: All documentation, markdown files (`README.md`, `SPEC.md`, `walkthrough.md`), UI copy in `app/static/index.html`, API docstrings, and CLI scripts must be written exclusively in clear, professional English.

## 2. Version Synchronization
- When bumping releases, update the root `VERSION` file.
- Do not hardcode static version numbers across multiple files; rely on `from app import __version__` and `GET /api/version`.

## 3. Code Aesthetics & Quality
- Keep Python code formatted and typed with Type Hints (`typing`, `Pydantic`).
- Maintain rich UI aesthetics: sleek dark mode palettes, glassmorphism, responsive grid layouts, and interactive micro-animations.
