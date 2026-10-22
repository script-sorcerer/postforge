# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Vault check: reads every Topic, Draft and Post note in the Vault and reports
each rule it breaks. Exits 1 on any violation, 0 when the Vault is clean.

Usage: uv run scripts/vault_check.py [VAULT]   (default: this repository)

To add a rule: write a `check_<name>(note)` function returning a list of
messages and append it to RULES. The rule is reported as `<name>` with
underscores turned into hyphens.
"""

import re
import sys
from pathlib import Path

import yaml

# Folders holding notes with a lifecycle. Publish packages are Posts not yet published.
NOTE_FOLDERS = ["Topics", "Drafts", "Publish packages", "Posts"]

REQUIRED_FIELDS = {
    "topic": ["kind", "status", "project", "rubric", "channels", "language"],
    "draft": ["kind", "status", "project", "topic", "channel", "language"],
    "post": ["kind", "status", "project", "topic", "channel", "language"],
}

LIFECYCLES = {
    "topic": ["proposed", "approved", "rejected", "parked"],
    "draft": ["drafting", "in-review", "revising", "ready"],
    "post": ["ready", "published"],
}

FRONTMATTER = re.compile(r"\A---\r?\n(.*?)^---\s*$", re.DOTALL | re.MULTILINE)


def read_note(path):
    """Return {path, fm, error}: fm is the frontmatter dict, or None with an error."""
    match = FRONTMATTER.match(path.read_text(encoding="utf-8"))
    if not match:
        return {"path": path, "fm": None, "error": "no YAML frontmatter block"}
    try:
        fm = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        return {"path": path, "fm": None, "error": f"invalid YAML: {e.problem}"}
    if not isinstance(fm, dict):
        return {"path": path, "fm": None, "error": "frontmatter is not a mapping"}
    return {"path": path, "fm": fm, "error": None}


def kind_of(note):
    fm = note["fm"]
    return fm.get("kind") if fm and fm.get("kind") in REQUIRED_FIELDS else None


def check_frontmatter(note):
    return [note["error"]] if note["error"] else []


def check_kind(note):
    if note["fm"] is None or kind_of(note):
        return []
    return [f"kind is {note['fm'].get('kind')!r}, expected one of {', '.join(REQUIRED_FIELDS)}"]


def check_required_fields(note):
    kind = kind_of(note)
    if not kind:
        return []
    missing = [f for f in REQUIRED_FIELDS[kind] if note["fm"].get(f) in (None, "", [])]
    return [f"{kind} is missing {', '.join(missing)}"] if missing else []


def check_status(note):
    kind = kind_of(note)
    status = note["fm"].get("status") if kind else None
    if status is None or status in LIFECYCLES[kind]:
        return []  # a missing status is reported by required-fields
    return [f"{kind} status {status!r} is not one of {', '.join(LIFECYCLES[kind])}"]


def check_published_link(note):
    fm = note["fm"]
    if kind_of(note) == "post" and fm.get("status") == "published" and not fm.get("published_url"):
        return ["published post has no published_url"]
    return []


RULES = [check_frontmatter, check_kind, check_required_fields, check_status, check_published_link]


def check_vault(vault):
    """Return (notes checked, list of 'note: [rule] message' lines)."""
    paths = sorted(p for folder in NOTE_FOLDERS for p in (vault / folder).rglob("*.md"))
    violations = []
    for path in paths:
        note = read_note(path)
        for rule in RULES:
            name = rule.__name__.removeprefix("check_").replace("_", "-")
            for message in rule(note):
                violations.append(f"{path.relative_to(vault)}: [{name}] {message}")
    return len(paths), violations


def main(argv):
    vault = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent.parent
    if not vault.is_dir():
        print(f"Vault not found: {vault}", file=sys.stderr)
        return 2
    count, violations = check_vault(vault)
    for line in violations:
        print(line)
    if violations:
        print(f"Vault check failed: {len(violations)} violation(s) in {count} note(s).")
        return 1
    print(f"Vault check passed: {count} note(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
