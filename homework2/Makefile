# Makefile (repo root)

PY ?= python
MANAGE := $(PY) manage.py

.PHONY: venv run migrate superuser collectstatic test render-build render-start

venv:
	python3 -m venv hw2venv --system-site-packages
	. hw2venv/bin/activate && pip install -r requirements.txt

run:
	$(MANAGE) runserver 0.0.0.0:3000

migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

superuser:
	$(MANAGE) createsuperuser

collectstatic:
	$(MANAGE) collectstatic --noinput

test:
	$(MANAGE) test bookings -v 2

# For Render: set these as the Build/Start commands in the dashboard
render-build:
	pip install -r requirements.txt
	$(MANAGE) collectstatic --noinput

render-start:
	gunicorn movie_theater_booking.wsgi:application
