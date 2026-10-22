# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Vault check: reads every Topic, Draft and Post note and every Channel rules
note in the Vault and reports each rule it breaks. Exits 1 on any violation,
0 when the Vault is clean.

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
    kind = note["fm"].get("kind") if note["fm"] else None
    return kind if isinstance(kind, str) and kind in REQUIRED_FIELDS else None


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


# Channel rules notes carry the Channel's limits in frontmatter; the check reads them from there.
CHANNEL_RULES_FOLDER = "Channel rules"


def is_count(value, minimum=1):
    return isinstance(value, int) and not isinstance(value, bool) and value >= minimum


def check_channel_rules(note):
    """Each Channel rules note must carry machine-readable limits."""
    fm = note["fm"]
    if fm is None:
        return []  # reported by frontmatter
    problems = []
    if not isinstance(fm.get("channel"), str) or not fm["channel"]:
        problems.append("channel is missing")
    text = fm.get("text")
    if not isinstance(text, dict) or not is_count(text.get("max_length")):
        problems.append("text.max_length must be a positive integer")
    media = fm.get("media")
    if not isinstance(media, dict) or not media:
        problems.append("media must map each media type to its limits")
    else:
        for name, limits in media.items():
            limits = limits if isinstance(limits, dict) else {}
            formats = limits.get("formats")
            size = limits.get("max_size_mb")
            if not is_count(limits.get("max_count")):
                problems.append(f"media.{name}.max_count must be a positive integer")
            if not (isinstance(formats, list) and formats and all(isinstance(f, str) for f in formats)):
                problems.append(f"media.{name}.formats must be a non-empty list")
            if isinstance(size, bool) or not isinstance(size, (int, float)) or size <= 0:
                problems.append(f"media.{name}.max_size_mb must be a positive number")
    hashtags = fm.get("hashtags")
    if not isinstance(hashtags, dict) or not is_count(hashtags.get("max"), minimum=0):
        problems.append("hashtags.max must be a non-negative integer")
    return problems


def load_channel_rules(vault):
    """Return ({channel: frontmatter} for each valid Channel rules note, violation lines)."""
    rules, violations = {}, []
    for path in sorted((vault / CHANNEL_RULES_FOLDER).glob("*.md")):
        note = read_note(path)
        problems = check_frontmatter(note) + check_channel_rules(note)
        violations += [f"{path.relative_to(vault)}: [channel-rules] {p}" for p in problems]
        if not problems:
            rules[note["fm"]["channel"]] = note["fm"]
    return rules, violations


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
    channel_rules, channel_violations = load_channel_rules(vault)
    return len(paths) + len(channel_rules), violations + channel_violations


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
