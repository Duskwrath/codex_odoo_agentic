Implement a new Odoo customization module for multi-level Sale Order approval.

Module name:
sale_order_approval

Business Requirements:
1. Add approval workflow for sale orders.
2. If untaxed amount < 5,000:
   - auto approve
3. If untaxed amount between 5,000 and 20,000:
   - Sales Manager approval required
4. If untaxed amount > 20,000:
   - Finance Manager approval required
   - General Manager final approval required
5. Prevent confirmation until approval chain is completed.
6. Add approval status field:
   - draft
   - waiting_manager
   - waiting_finance
   - waiting_gm
   - approved
   - rejected
7. Add approve/reject buttons.
8. Add approval history log model.
9. Send chatter notifications for approval actions.
10. Add access security groups:
   - sale_approval_manager
   - sale_approval_finance
   - sale_approval_gm

Technical Requirements:
1. Create clean modular Odoo addon structure.
2. Follow Odoo ORM best practices.
3. Use inheritance on sale.order.
4. Avoid raw SQL.
5. Add XML views for:
   - form view buttons
   - approval status badge
   - approval history tab
6. Add security:
   - ir.model.access.csv
   - record rules if needed
7. Add demo data for testing.

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
1. Analyze current sale module structure.
2. Create/update tests first.
3. Implement feature incrementally.
4. Run formatter.
5. Run lint.
6. Run module tests.
7. If tests fail:
   - inspect failures
   - fix code
   - rerun tests
8. Repeat until all tests pass.

Commands:
- make format
- make lint
- make test MODULE=sale_order_approval
- make smoke

Git Rules:
1. Never force push.
2. Never push to main/master.
3. Create feature branch:
   feat/sale-order-approval
4. Commit only after green tests.
5. Commit message:
   feat(sale_order_approval): implement multi-level approval workflow

Code Quality Rules:
1. Keep methods small and readable.
2. Add docstrings for non-trivial logic.
3. Avoid duplicated business logic.
4. Use meaningful variable names.
5. Use computed fields only when appropriate.
6. Keep security explicit.
7. Keep workflow extensible for future approval levels.

Deliverables:
1. Fully working Odoo addon
2. XML views
3. Security files
4. Automated tests
5. Demo data
6. Migration-safe implementation
7. Git commit after successful tests

Workflow:
1. Add/update tests.
2. Implement code.Follow SOLID and Odoo Coding Guide.
3. Run make lint.
4. Run make test MODULE=custom_module.
5. If failing, fix and rerun.
6. When green, create a git commit.
7. Run make safe-push.