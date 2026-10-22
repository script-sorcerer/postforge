# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Vault check: reads every Topic, Draft, Post and Fact sheet note and every
Channel rules note in the Vault and reports each rule it breaks. Exits 1 on
any violation, 0 when the Vault is clean.

Usage: uv run scripts/vault_check.py [VAULT]   (default: this repository)

To add a rule: write a `check_<name>(note)` function returning a list of
messages and append it to RULES. The rule is reported as `<name>` with
underscores turned into hyphens.
"""

import functools
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


# Fact sheet: one per Project, proposed by the Scout, approved only by the Owner.
NOTE_FOLDERS.append("Fact sheets")
REQUIRED_FIELDS["fact-sheet"] = ["kind", "status", "project"]
LIFECYCLES["fact-sheet"] = ["proposed", "approved"]


def check_fact_sheet(note):
    """public_name may be empty until the name is public; the key must still be there."""
    if kind_of(note) != "fact-sheet":
        return []
    fm, messages = note["fm"], []
    if not isinstance(fm.get("public_name", 0), (str, type(None))):
        messages.append("public_name is missing or not text (leave it empty until the name is public)")
    if not isinstance(fm.get("shown_publicly", 0), (list, type(None))):
        messages.append("shown_publicly is missing or not a list")
    return messages


RULES.append(check_fact_sheet)


# Digest: a ranked batch of Topics. Its `topics` list links each Topic note, best first.
NOTE_FOLDERS.append("Digests")
REQUIRED_FIELDS["digest"] = ["kind", "project", "date", "topics"]
LIFECYCLES["digest"] = []  # a Digest has no status; its Topics carry the Owner's verdicts
REQUIRED_FIELDS["topic"] += ["rank", "needs_media", "promotional"]

RUBRICS = [
    "Devlog", "Design decision", "Gameplay moment", "Building with AI agents",
    "Ask the audience", "How-to", "Humor / Meme", "Bug of the week",
    "Before / After", "By the numbers", "Player challenge",
]


def check_rubric(note):
    rubric = note["fm"].get("rubric") if kind_of(note) == "topic" else None
    if rubric is None or rubric in RUBRICS:
        return []  # a missing rubric is reported by required-fields
    return [f"rubric {rubric!r} is not one of {', '.join(RUBRICS)}"]


def check_rejection_reason(note):
    fm = note["fm"]
    if kind_of(note) == "topic" and fm.get("status") == "rejected" and not fm.get("reason"):
        return ["rejected topic has no reason"]
    return []


def digest_topics(note):
    """Return (Topic frontmatters found, links with no Topic note) for a Digest note."""
    links = note["fm"].get("topics") or []
    topics_dir = note["path"].parent.parent / "Topics"
    found, missing = [], []
    for link in links:
        name = str(link).strip("[]").split("|")[0].split("/")[-1]
        path = topics_dir / f"{name}.md"
        topic = read_note(path) if path.is_file() else None
        if topic and topic["fm"]:
            found.append(topic["fm"])
        else:
            missing.append(str(link))
    return found, missing


def check_digest_links(note):
    if kind_of(note) != "digest":
        return []
    return [f"topic {link} has no note in Topics/" for link in digest_topics(note)[1]]


def check_digest_size(note):
    if kind_of(note) != "digest":
        return []
    count = len(note["fm"].get("topics") or [])
    return [] if 5 <= count <= 8 else [f"digest holds {count} topics, expected 5 to 8"]


def check_digest_rubrics(note):
    if kind_of(note) != "digest":
        return []
    rubrics = [t.get("rubric") for t in digest_topics(note)[0]]
    crowded = sorted({r for r in rubrics if r and rubrics.count(r) > 2})
    return [f"more than two topics of rubric {r!r}" for r in crowded]


def check_digest_promotional(note):
    if kind_of(note) != "digest":
        return []
    topics = digest_topics(note)[0]
    promo = sum(1 for t in topics if t.get("promotional") is True)
    if 3 * promo <= len(topics):
        return []
    return [f"{promo} of {len(topics)} topics are promotional, at most a third allowed"]


RULES += [
    check_rubric, check_rejection_reason,
    check_digest_links, check_digest_size, check_digest_rubrics, check_digest_promotional,
]


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


# Draft: written by the Writer through six Passes, always in this order.
PASSES = ["angle", "hooks", "draft", "voice", "humanize", "channel-fit"]
# The Post text ends at the first callout (the Hook alternatives) or `## ` heading (Writer notes).
POST_TEXT_END = re.compile(r"^(> \[!|## )", re.MULTILINE)


def draft_vault(note):
    """The Vault holding a Draft note: the folder above its `Drafts` ancestor."""
    return next((p.parent for p in note["path"].parents if p.name == "Drafts"), note["path"].parent.parent)


def link_name(link):
    return str(link).strip("[]").split("|")[0].split("/")[-1]


def check_draft_topic(note):
    topic = note["fm"].get("topic") if kind_of(note) == "draft" else None
    if not topic:
        return []  # a missing topic is reported by required-fields
    path = draft_vault(note) / "Topics" / f"{link_name(topic)}.md"
    linked = read_note(path) if path.is_file() else None
    if linked and kind_of(linked) == "topic":
        return []
    return [f"topic {topic} has no Topic note in Topics/"]


def check_draft_passes(note):
    """A Draft records its Passes in order; only a drafting Draft may stop short of all six."""
    if kind_of(note) != "draft":
        return []
    passes = note["fm"].get("passes") or []
    if not isinstance(passes, list) or passes != PASSES[: len(passes)]:
        return [f"passes {passes} are not in order {', '.join(PASSES)}"]
    if note["fm"].get("status") != "drafting" and len(passes) < len(PASSES):
        return [f"passes {passes} are incomplete; all of {', '.join(PASSES)} must run"]
    return []


@functools.cache
def channel_limits(vault):
    return load_channel_rules(vault)[0]


def post_text(path):
    """The Post text of a Draft: the body after the frontmatter, up to the Hook alternatives
    callout or the first `## ` heading, stripped."""
    body = FRONTMATTER.sub("", path.read_text(encoding="utf-8"), count=1)
    return POST_TEXT_END.split(body, maxsplit=1)[0].strip()


def check_draft_length(note):
    if kind_of(note) != "draft":
        return []
    # shortcut: a Draft whose Channel has no rules note is not length-checked; add a rule once every Channel has one.
    rules = channel_limits(draft_vault(note)).get(note["fm"].get("channel"))
    if not rules:
        return []
    # URLs count as written: stricter than X, which counts each as 23 characters.
    length = len(post_text(note["path"]))
    limit = rules["text"]["max_length"]
    return [] if length <= limit else [f"post text is {length} characters, {rules['channel']} allows {limit}"]


RULES += [check_draft_topic, check_draft_passes, check_draft_length]


# The Project's GitHub repository is private: no note may link to it or its issues.
REPO_SLUGS = []  # filled by check_vault from each Projects/<project>.md `github` field


def load_repo_slugs(vault):
    notes = (read_note(p) for p in sorted((vault / "Projects").glob("*.md")))
    return [n["fm"]["github"] for n in notes if n["fm"] and isinstance(n["fm"].get("github"), str) and n["fm"]["github"]]


def check_private_repo_link(note):
    if kind_of(note) not in ("topic", "draft", "post"):
        return []
    text = note["path"].read_text(encoding="utf-8")
    # [/:] covers https and ssh remotes; the slug may end in .git, /issues/91, ) or end of line.
    return [
        f"links to the private repository {slug}"
        for slug in REPO_SLUGS
        if re.search(rf"github\.com[/:]{re.escape(slug)}(?![\w-])", text, re.IGNORECASE)
    ]


RULES.append(check_private_repo_link)


# Editor loop: at most two Editor rounds per Draft, then it goes to the Owner whatever the score.
MAX_EDITOR_ROUNDS = 2


def check_editor_rounds(note):
    if kind_of(note) != "draft" or "editor_rounds" not in note["fm"]:
        return []
    rounds = note["fm"]["editor_rounds"]
    if is_count(rounds, minimum=0) and rounds <= MAX_EDITOR_ROUNDS:
        return []
    return [f"editor_rounds {rounds!r} must be a whole number from 0 to {MAX_EDITOR_ROUNDS}"]


RULES.append(check_editor_rounds)


def check_vault(vault):
    """Return (notes checked, list of 'note: [rule] message' lines)."""
    REPO_SLUGS[:] = load_repo_slugs(vault)
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
