# Odoo Agentic Development Rules

You are working on an Odoo addon repository.

## Main workflow

1. Understand the requested change.
2. Inspect the relevant addon files.
3. Write or update tests first when possible.
4. Implement the smallest correct change.
5. Run formatting and linting.
6. Run Odoo tests.
7. If tests fail, inspect the failure, fix the code, and rerun.
8. Repeat until tests pass.
9. Commit only when all checks pass.
10. Push only through `scripts/git-safe-push.sh`.

## Commands

Use these commands only:

- `make lint`
- `make format`
- `make test MODULE=custom_module`
- `make test-all`
- `make smoke`
- `make safe-push`

## Odoo rules

- Keep business logic in `models/`.
- Keep HTTP/API logic in `controllers/`.
- Never put business logic in XML.
- Add access rules in `security/ir.model.access.csv`.
- Add record rules when data visibility matters.
- Every non-trivial model method needs a test.
- Use Odoo ORM patterns, not raw SQL, unless justified.
- Tests must live in `addons/<module>/tests/`.

## Git rules

- Never commit failing tests.
- Never use `git push --force`.
- Commit message format:
  - `ADD(module): short description`
  - `FIX(module): short description`
  - `TEST(module): short description`
  - `REF(module): short description`
  - `REM(module): short description`