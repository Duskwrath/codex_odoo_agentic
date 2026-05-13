MODULE ?= custom_module
DB ?= odoo_test
ODOO_BIN ?= ./odoo/odoo-bin
ODOO_CONF ?= ./config/odoo.conf

.PHONY: start lint format test test-all smoke commit safe-push

start:
	./scripts/start-odoo.sh

lint:
	./scripts/lint.sh

format:
	./scripts/format.sh

test:
	./scripts/run-module-tests.sh $(MODULE) $(DB)

test-all:
	./scripts/run-tests.sh $(DB)

smoke:
	./scripts/smoke-test.sh

safe-push:
	./scripts/git-safe-push.sh