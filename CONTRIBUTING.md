# Contributing to uSipipo Support Bot

First off, thank you for considering contributing to uSipipo Support Bot! It's people like you that make uSipipo such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## I don't want to read this whole thing I just have a question!!!

> **Please don't open an issue for questions.** Check existing issues first, and if you don't find your answer, ask in our team channels.

## What We Are Looking For

We welcome contributions in the following areas:

- Bug reports and fixes
- Feature requests and implementations
- Documentation improvements
- Test coverage improvements
- Performance optimizations

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Run tests: `uv run pytest`
6. Run linters: `uv run ruff check src tests && uv run mypy src`
7. Commit your changes
8. Push to your fork
9. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/usipipo-support-bot.git
cd usipipo-support-bot

# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync --dev

# Set up pre-commit hooks
uv run pre-commit install

# Copy environment file
cp example.env .env

# Run tests
uv run pytest
```

## Pull Request Guidelines

- **Keep it small:** Smaller PRs are easier to review and merge
- **Write tests:** All new features should have tests
- **Update documentation:** Update README.md and docs/ if needed
- **Follow style:** Use ruff and mypy to check code style
- **Be descriptive:** Write clear commit messages and PR descriptions

### Commit Messages

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new ticket category
fix: resolve authentication issue
docs: update README.md
test: add tests for ticket handlers
refactor: improve error handling
```

### Code Review

All PRs require at least one approval from a maintainer. Be respectful and constructive in code reviews.

## Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **Environment details** (Python version, OS, etc.)

**Example:**
```markdown
**Bug Summary**
Ticket creation fails when category is missing

**Steps to Reproduce**
1. Send /nuevoticket
2. Don't select a category
3. Bot crashes

**Expected:** Bot should show error message
**Actual:** Bot crashes with KeyError

**Environment:**
- Python: 3.13
- OS: Ubuntu 22.04
```

## Feature Requests

Feature requests are welcome! Please include:

- **Use case:** Why do you need this feature?
- **Proposed solution:** How should it work?
- **Alternatives considered:** What other approaches did you consider?

## Testing

We strive for 90%+ test coverage:

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/bot/test_tickets_handlers.py
```

## Questions?

Feel free to reach out to the maintainers if you have any questions!

Thank you for contributing to uSipipo Support Bot! 🎉
