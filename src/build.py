#!/usr/bin/env python3
import shutil
import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
DIST_DIR = BASE_DIR / "dist"
YAML_PATH = BASE_DIR / "resume.yaml"

ACCENT = "#eab308"
ACCENT_HOVER = "#facc15"


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def prepare_data(data):
    cv = data.get("cv", {})

    experience = cv.get("experience", [])
    experience.sort(key=lambda x: x.get("start_date", ""), reverse=True)
    cv["experience"] = experience

    skills = cv.get("skills", {})
    skills_list = []
    for key, items in skills.items():
        name = key.replace("_", " ").title()
        skills_list.append({"name": name, "tools": items})
    cv["skills_list"] = skills_list

    personal = cv.get("personal_information", {})
    contact = personal.get("contact", {})
    li_username = contact.get("linkedin", "")
    if li_username and not li_username.startswith("http"):
        contact["linkedin_url"] = f"https://linkedin.com/in/{li_username}"

    languages = cv.get("languages", {})
    lang_list = []
    for name, details in languages.items():
        if isinstance(details, str):
            lang_list.append({"name": name.title(), "level": details})
        elif isinstance(details, dict):
            values = sorted({v for v in details.values() if v})
            label = ", ".join(values) if values else ""
            lang_list.append({"name": name.title(), "level": label})
    cv["languages_list"] = lang_list

    return cv


def build():
    raw = load_yaml(YAML_PATH)
    context = prepare_data(raw)

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=True)

    DIST_DIR.mkdir(exist_ok=True)

    avatar_src = BASE_DIR / "avatar.png"
    if avatar_src.exists():
        shutil.copy2(str(avatar_src), str(DIST_DIR / "avatar.png"))

    html = env.get_template("base.html.j2").render(
        **context, accent=ACCENT, accent_hover=ACCENT_HOVER
    )
    (DIST_DIR / "index.html").write_text(html)

    css = env.get_template("style.css.j2").render(
        accent=ACCENT, accent_hover=ACCENT_HOVER
    )
    (DIST_DIR / "style.css").write_text(css)

    print("Resume built successfully in dist/")


if __name__ == "__main__":
    build()
