# Resume — David Eduardo Carrera del Castillo

Static HTML resume generated from a YAML source of truth.

## How it works

```
resume.yaml  ──►  src/build.py  ──►  dist/
                                        ├── index.html
                                        ├── style.css
                                        └── avatar.png
```

Edit `resume.yaml` and run `make build` to regenerate the static site in `dist/`.

## Usage

```bash
make build   # Install deps + generate HTML/CSS from YAML
make serve   # Preview at http://localhost:8000
make clean   # Remove dist/
```

First run creates a Python virtual environment (`.venv/`) and installs dependencies automatically.

## Project structure

```
├── resume.yaml              # Resume data (source of truth)
├── src/build.py             # Python build script (PyYAML + Jinja2)
├── templates/
│   ├── base.html.j2         # HTML layout
│   ├── style.css.j2         # Dark theme CSS with yellow accent
│   └── sections/            # Per-section Jinja2 partials
├── dist/                    # Generated output (gitignored)
├── .github/workflows/       # CI/CD
├── avatar.png               # Profile picture
├── requirements.txt         # Python dependencies
└── Makefile                 # Convenience commands
```

## Deployment

The GitHub Actions workflow (`.github/workflows/deploy.yml`) automatically builds and deploys to **GitHub Pages** whenever `resume.yaml` changes on `main`.

1. Push to a GitHub repository
2. Go to **Settings → Pages → Source: GitHub Actions**
3. Done — every `resume.yaml` change triggers a redeploy
