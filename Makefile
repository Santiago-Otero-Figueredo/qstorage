
install:
	pip install -r requirements/production.txt

install-test:
	pip install -r requirements/test.txt

coverage:
	coverage run --source="." manage.py test ./apps/$(app)

lint:
	@if [ "$(app)" = "" ]; then \
		pylint ./apps/*/*.py --disable=C0114,R0901,C0115,E1101,R0903; \
	else \
		pylint ./apps/$(app)/*.py --disable=C0114,R0901,C0115,E1101,R0903; \
	fi

code-checker:
	flake8 apps/$(app) \
	--exclude .git,__pycache__,"apps/*/migrations/" \
	--max-line-length 120 \
	--ignore=E128,E124

coverage-test:
	coverage json --fail-under=$(limit)

coverage-report:
	coverage html --skip-covered --skip-empty --precision=2

coverage-report-json:
	coverage json --pretty-print

test: lint code-checker