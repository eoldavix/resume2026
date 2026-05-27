.PHONY: build clean serve

.venv/bin/python:
	python3 -m venv .venv
	.venv/bin/pip install -q -r requirements.txt

build: .venv/bin/python dist/index.html dist/style.css

dist/index.html dist/style.css: assets/resume.yaml src/build.py templates/base.html.j2 templates/style.css.j2 $(wildcard templates/sections/*.html.j2)
	.venv/bin/python src/build.py

serve: build
	python3 -m http.server -d dist

clean:
	rm -rf dist
