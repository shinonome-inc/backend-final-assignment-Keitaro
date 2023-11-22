run:
	python3 manage.py runserver

test:
	python3 manage.py test

fix-code: lint format fix-import

lint:
	flake8

format:
	black .

fix-import:
	isort .
