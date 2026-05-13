# Odoo Agentic Development With Codex CLI

This document explains how to use Codex CLI for agentic Odoo addon
development. The goal is to give Codex enough project context, clear delivery
rules, and repeatable verification commands so it can safely build, test, and
review Odoo customizations.

The `sale_order_approval` prompt near the end is only an example of a good
feature request prompt.

## What This Workflow Is For

Use this workflow when you want Codex CLI to help with Odoo work such as:

- Creating a new custom addon.
- Extending an existing addon.
- Adding models, fields, business methods, views, security rules, and demo data.
- Writing Odoo tests.
- Reviewing an implementation for ORM, security, upgrade, and deployment risks.
- Running local checks before commit.

## Repository Expectations

Codex works best when the repository has predictable Odoo structure and clear
agent rules.

```text
.
|-- AGENTS.md
|-- Makefile
|-- addons/
|   `-- <module_name>/
|-- config/
|-- docker-compose.yaml
`-- scripts/
```

Important locations:

- `AGENTS.md`: local rules Codex should follow.
- `addons/`: custom Odoo addons.
- `addons/<module_name>/models/`: Odoo business logic.
- `addons/<module_name>/views/`: XML views.
- `addons/<module_name>/security/`: groups, access rules, and record rules.
- `addons/<module_name>/data/`: required data loaded in normal installs.
- `addons/<module_name>/demo/`: optional demo data.
- `addons/<module_name>/tests/`: automated Odoo tests.
- `scripts/`: helper scripts used by `make`.

## Prerequisites

- Codex CLI installed and authenticated.
- Docker and Docker Compose available for Odoo runtime checks.
- An Odoo development workspace with custom addons under `./addons`.
- A git branch for the task.
- A test database or disposable development database.

Check Codex CLI:

```bash
codex --help
```

Log in if needed:

```bash
codex login
```

## Starting Codex CLI

Run Codex from the repository root so it can read `AGENTS.md`, inspect the
project, and use the correct relative paths.

Interactive mode:

```bash
cd /home/slo/Documents/codex_odoo_agentic
codex
```

Start with an initial prompt:

```bash
codex -C /home/slo/Documents/codex_odoo_agentic "Inspect this Odoo addon workspace and summarize the development rules."
```

Run a non-interactive task:

```bash
codex exec -C /home/slo/Documents/codex_odoo_agentic "Review the custom addons and report missing tests or security files."
```

Review uncommitted changes:

```bash
codex -C /home/slo/Documents/codex_odoo_agentic review --uncommitted
```

## Step-by-Step Agentic Workflow

1. Start from a clean branch.

   ```bash
   git status --short
   git checkout -b feat/<feature-name>
   ```

2. Start Codex CLI from the repository root.

   ```bash
   codex
   ```

3. Give Codex a complete task prompt.

   A good Odoo prompt should include:

   - Target Odoo version.
   - Module name.
   - Business requirements.
   - Technical requirements.
   - Security requirements.
   - View requirements.
   - Test requirements.
   - Commands to run.
   - Git and deployment rules.

4. Ask Codex to inspect before editing.

   Codex should read `AGENTS.md`, inspect the relevant addon files, check
   existing patterns, and explain the intended change before writing files.

5. Ask Codex to add or update tests first when practical.

   Odoo tests should live in:

   ```text
   addons/<module_name>/tests/
   ```

6. Let Codex implement the smallest complete change.

   A normal addon should follow this shape:

   ```text
   addons/<module_name>/
   |-- __init__.py
   |-- __manifest__.py
   |-- models/
   |-- views/
   |-- security/
   |-- data/
   |-- demo/
   `-- tests/
   ```

7. Verify Python syntax.

   ```bash
   python3 -m compileall addons
   ```

8. Run formatting.

   ```bash
   make format
   ```

9. Run lint checks.

   ```bash
   make lint
   ```

10. Run module tests.

    ```bash
    make test MODULE=<module_name>
    ```

11. Start Odoo services.

    ```bash
    docker compose -f docker-compose.yaml up -d
    ```

12. Upgrade the module in a test database.

    This repository's Compose service is named `web`.

    ```bash
    docker compose exec web odoo -u <module_name> -d <database_name>
    ```

13. Run a smoke test.

    ```bash
    make smoke
    ```

14. Review the diff.

    ```bash
    git diff
    git status --short
    ```

15. Ask Codex for a review pass.

    ```bash
    codex -C /home/slo/Documents/codex_odoo_agentic review --uncommitted
    ```

16. Commit only after checks pass.

    ```bash
    git add addons/<module_name>
    git commit -m "feat(<module_name>): <short description>"
    ```

17. Push through the safe push helper.

    ```bash
    make safe-push
    ```

## Prompt Template

Use this structure for new Odoo agentic tasks:

```text
Implement an Odoo customization.

Target Odoo version: 19.
Custom addons path: ./addons

Module name:
<module_name>

Business Requirements:
1. <business rule>
2. <business rule>
3. <business rule>

Technical Requirements:
1. Follow standard Odoo module structure.
2. Use Odoo ORM patterns.
3. Avoid raw SQL unless justified.
4. Add or update XML views.
5. Add security files:
   - ir.model.access.csv
   - record rules if needed
6. Add demo or data files if needed.
7. Keep the implementation migration-safe and backward compatible.

Testing Requirements:
1. Add automated tests.
2. Test the main business logic.
3. Test permission restrictions.
4. Test failure and edge cases.
5. Use TransactionCase or SavepointCase.
6. Ensure tests are isolated and repeatable.

Commands to run:
- python3 -m compileall addons
- make format
- make lint
- make test MODULE=<module_name>
- docker compose -f docker-compose.yaml up -d
- docker compose exec web odoo -u <module_name> -d <database_name>
- make smoke

Git Rules:
1. Never force push.
2. Never push directly to main or master.
3. Commit only after green tests.
4. Use this commit message:
   feat(<module_name>): <short description>
5. Run make safe-push only after the commit is ready.

Deliverables:
1. Working Odoo addon changes.
2. XML views if needed.
3. Security files if needed.
4. Automated tests.
5. Demo or data files if needed.
6. Migration-safe implementation.
7. Git commit after successful checks.
```

## Example Prompt: Sale Order Approval

The following prompt is an example only. It demonstrates how to write a complete
Codex CLI request for an Odoo addon.

```text
Implement a new Odoo customization module for multi-level Sale Order approval.

Target Odoo version: 19.
Custom addons path: ./addons

Module name:
sale_order_approval

Business Requirements:
1. Add an approval workflow for sale orders.
2. If the untaxed amount is less than 5,000:
   - Auto approve.
3. If the untaxed amount is between 5,000 and 20,000:
   - Sales Manager approval is required.
4. If the untaxed amount is greater than 20,000:
   - Finance Manager approval is required.
   - General Manager final approval is required.
5. Prevent sale order confirmation until the approval chain is completed.
6. Add an approval status field with these values:
   - draft
   - waiting_manager
   - waiting_finance
   - waiting_gm
   - approved
   - rejected
7. Add approve and reject buttons.
8. Add an approval history log model.
9. Send chatter notifications for approval actions.
10. Add access security groups:
    - sale_approval_manager
    - sale_approval_finance
    - sale_approval_gm

Technical Requirements:
1. Create a clean modular Odoo addon structure.
2. Follow Odoo ORM best practices.
3. Use inheritance on sale.order.
4. Avoid raw SQL.
5. Add XML views for:
   - form view buttons
   - approval status badge
   - approval history tab
6. Add security files:
   - ir.model.access.csv
   - record rules if needed
7. Add demo data for testing.
8. Keep the implementation migration-safe and backward compatible.

Testing Requirements:
1. Create full automated tests.
2. Test approval routing logic.
3. Test permission restrictions.
4. Test rejection flow.
5. Test confirm blocking before approval.
6. Test chatter message creation.
7. Use TransactionCase or SavepointCase.
8. Ensure tests are isolated and repeatable.

Development Workflow:
1. Analyze the current sale module structure.
2. Create or update tests first when practical.
3. Implement the feature incrementally.
4. Run the formatter.
5. Run lint checks.
6. Run module tests.
7. If tests fail:
   - inspect failures
   - fix code
   - rerun tests
8. Repeat until all tests pass.

Commands to run:
- python3 -m compileall addons
- make format
- make lint
- make test MODULE=sale_order_approval
- docker compose -f docker-compose.yaml up -d
- docker compose exec web odoo -u sale_order_approval -d <database_name>
- make smoke

Git Rules:
1. Never force push.
2. Never push directly to main or master.
3. Commit only after green tests.
4. Use this commit message:
   feat(sale_order_approval): implement multi-level approval workflow
5. Run make safe-push only after the commit is ready.

Code Quality Rules:
1. Keep methods small and readable.
2. Add docstrings for non-trivial logic.
3. Avoid duplicated business logic.
4. Use meaningful variable names.
5. Use computed fields only when appropriate.
6. Keep security explicit.
7. Keep the workflow extensible for future approval levels.

Deliverables:
1. Fully working Odoo addon.
2. XML views.
3. Security files.
4. Automated tests.
5. Demo data.
6. Migration-safe implementation.
7. Git commit after successful tests.
```

## Review Prompt

Use this after implementation:

```text
Review the Odoo addon changes for ORM issues, security mistakes, workflow bugs,
missing tests, migration risks, and deployment risks. Prioritize findings by
severity and include file and line references.
```

## Database, Migration, and Deployment Risks

Ask Codex to explain these risks before finalizing any Odoo feature:

- New fields can affect existing records during module upgrade.
- Default values must be safe for existing data.
- Security groups and access rules can block legitimate users if configured
  incorrectly.
- XML ID changes can break upgrades, views, rules, or demo data.
- Chatter, automated actions, and cron jobs can create unexpected side effects
  on bulk updates.
- Module upgrades should be tested on a staging database before production.

## Useful Commands

```bash
python3 -m compileall addons
make format
make lint
make test MODULE=<module_name>
docker compose -f docker-compose.yaml up -d
docker compose exec web odoo -u <module_name> -d <database_name>
make smoke
make safe-push
```
## Alert !!
add ./config and other crt file to .gitignore in production server 
