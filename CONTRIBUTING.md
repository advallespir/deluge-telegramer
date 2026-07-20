# Contributing to Telegramer

Thanks for your interest in contributing! Here's how to get started.

## Development Setup

```bash
git clone https://github.com/Avallone-io/deluge-telegramer.git
cd deluge-telegramer
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install pytest hypothesis python-telegram-bot>=20.0
```

## Running Tests

```bash
pytest tests/ -v
```

Tests use [Hypothesis](https://hypothesis.readthedocs.io/) for property-based testing.
They validate plugin logic without requiring a running Deluge instance or Telegram connection.

## Workflow

1. **Fork** the repository
2. **Create a branch** from `master`: `git checkout -b fix/your-description`
3. **Make your changes** — keep commits focused and atomic
4. **Run tests** locally: `pytest tests/ -v`
5. **Push** your branch and open a **Pull Request** against `master`
6. CI will run tests across Python 3.11–3.13 and build the egg

## Branch Naming

| Type     | Pattern                  | Example                          |
| -------- | ------------------------ | -------------------------------- |
| Bug fix  | `fix/short-description`  | `fix/polling-conflict-on-reload` |
| Feature  | `feat/short-description` | `feat/inline-keyboard-support`   |
| Docs     | `docs/short-description` | `docs/update-install-guide`      |
| CI/Infra | `ci/short-description`   | `ci/add-test-job`                |

## Pull Request Guidelines

- One logical change per PR
- Reference related issues (e.g. `Fixes #12`)
- Include a brief description of what changed and why
- If adding new functionality, add tests
- Ensure CI passes before requesting review

## Code Style

- Follow existing patterns in the codebase
- Use `log.info(prelog() + ...)` for important events, `log.debug(...)` for verbose output
- All Telegram handlers must check whitelist: `if str(update.message.chat.id) in self.whitelist:`
- Async handlers use `async def` with `Update` and `ContextTypes.DEFAULT_TYPE` parameters

## Releasing

Releases are automated via GitHub Actions:

1. Update version in `setup.py`
2. Merge PR to `master`
3. Tag: `git tag v2.2.0.1 && git push --tags`
4. CI builds eggs for all Python versions and creates a GitHub Release

## Reporting Issues

Use the issue templates:

- **Bug Report** — for something broken
- **Feature Request** — for new ideas

Include your Deluge version, Python version, container info, and relevant logs.
