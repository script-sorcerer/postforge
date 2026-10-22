#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Vault check: reads every Topic, Draft, Post, Fact sheet, Digest and Trend scan
note and every Channel rules note in the Vault and reports each rule it breaks.
Exits 1 on any violation, 0 when the Vault is clean.

Usage: scripts/vault_check.py [VAULT]   (default: this repository; needs uv)
       scripts/vault_check.py --seal NOTE   (the Owner only: record NOTE's Owner edits)

The schema (folders, required fields, lifecycles, Rubrics, Channels, Topic
sections, Passes) is the tables at the top. To add a rule: write a
`check_<name>(note)` function returning a list of messages and add it to the
RULES list above check_vault. The rule is reported as `<name>` with
underscores turned into hyphens.
"""

import datetime
import hashlib
import re
import sys
from pathlib import Path

import yaml

# Folders holding checked notes. Publish packages are Posts not yet published.
NOTE_FOLDERS = ["Topics", "Drafts", "Publish packages", "Posts", "Fact sheets", "Digests", "Trend scans"]
# Channel rules notes carry each Channel's limits in frontmatter; see load_channel_rules.
CHANNEL_RULES_FOLDER = "Channel rules"

# kind -> fields every note of that kind must fill.
REQUIRED_FIELDS = {
    "topic": ["kind", "status", "project", "rubric", "channels", "language", "rank", "needs_media", "promotional"],
    "draft": ["kind", "status", "project", "topic", "channel", "language"],
    "post": ["kind", "status", "project", "topic", "channel", "language"],
    "fact-sheet": ["kind", "status", "project"],  # one per Project, approved only by the Owner
    # `topics` links each Topic note, best first; `trend_scan` links the Trend scan it built on.
    "digest": ["kind", "project", "date", "topics", "trend_scan"],
    "trend-scan": ["kind", "date"],
}

# kind -> allowed statuses. A Digest has none (its Topics carry the Owner's verdicts);
# a Trend scan has none (it goes stale by date).
LIFECYCLES = {
    "topic": ["proposed", "approved", "rejected", "parked"],
    "draft": ["drafting", "in-review", "revising", "ready"],
    "post": ["ready", "published"],
    "fact-sheet": ["proposed", "approved"],
    "digest": [],
    "trend-scan": [],
}

RUBRICS = [
    "Devlog", "Design decision", "Gameplay moment", "Building with AI agents",
    "Ask the audience", "How-to", "Humor / Meme", "Bug of the week",
    "Before / After", "By the numbers", "Player challenge",
]

# Channels in iteration 1: a Topic's `channels` may name only these.
CHANNELS = ["x", "reddit", "linkedin"]

# Every Topic note body carries these `## ` sections (the Scout's Topic template).
TOPIC_SECTIONS = ["Angle", "Why now", "Source material", "Shot list"]

# A Digest's `trend_scan` may be at most this many days older than the Digest.
TREND_SCAN_MAX_AGE_DAYS = 14

# Draft: written by the Writer through six Passes, always in this order.
PASSES = ["angle", "hooks", "draft", "voice", "humanize", "channel-fit"]
# The Post text ends at the first callout (the Hook alternatives) or `## ` heading (Writer notes).
POST_TEXT_END = re.compile(r"^(> \[!|## )", re.MULTILINE)
# Editor loop: at most this many Editor rounds per Draft, then it goes to the Owner whatever the score.
MAX_EDITOR_ROUNDS = 2

# Owner edit: text between these Obsidian comment markers. `--seal <note>` records each block's
# fingerprint in the note's `owner_edits`; only the Owner (by hand or through /revise) seals.
OWNER_BLOCK = re.compile(r"%% owner %%(.*?)%% /owner %%", re.DOTALL)
OWNER_MARKER = re.compile(r"%% /?owner %%")

# Publish package: Attachment types whose files need alt text, and the folder each Post status
# lives in (the Owner moves a published Post to Posts/, the history of published Posts).
ALT_TEXT_TYPES = ["image", "gif"]
POST_FOLDERS = {"ready": "Publish packages", "published": "Posts"}

# The Project's GitHub repository is private: no note may link to it or its issues.
REPO_SLUGS = []  # filled by check_vault from each Projects/<project>.md `github` field

# Filled by check_vault: notes by (top folder, note name) for wiki-link lookups, and the
# frontmatter of each valid Channel rules note by `channel`.
VAULT_NOTES = {}
CHANNEL_RULES = {}
VAULT_ROOT = []  # filled by check_vault: Attachment paths are relative to it

FRONTMATTER = re.compile(r"\A---\r?\n(.*?)^---\s*$", re.DOTALL | re.MULTILINE)


def read_note(path):
    """Return {path, text, fm, error}: fm is the frontmatter dict, or None with an error."""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return {"path": path, "text": "", "fm": None, "error": "file is not UTF-8 text"}
    note = {"path": path, "text": text, "fm": None, "error": None}
    match = FRONTMATTER.match(text)
    if not match:
        return note | {"error": "no YAML frontmatter block"}
    try:
        fm = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        # ReaderError (a control character) has no `problem`; its text spans lines.
        problem = getattr(e, "problem", None) or str(e).splitlines()[0]
        return note | {"error": f"invalid YAML: {problem}"}
    if not isinstance(fm, dict):
        return note | {"error": "frontmatter is not a mapping"}
    return note | {"fm": fm}


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


def check_topic_channels(note):
    channels = note["fm"].get("channels") if kind_of(note) == "topic" else None
    if channels is None:
        return []  # a missing channels list is reported by required-fields
    if not isinstance(channels, list):
        return [f"channels {channels!r} must be a list of {', '.join(CHANNELS)}"]
    unknown = [c for c in channels if c not in CHANNELS]
    return [f"channels {unknown} are not among {', '.join(CHANNELS)}"] if unknown else []


def check_topic_sections(note):
    if kind_of(note) != "topic":
        return []
    missing = [h for h in TOPIC_SECTIONS if not re.search(rf"^## {re.escape(h)}[ \t]*$", note["text"], re.MULTILINE)]
    return [f"topic has no {', '.join(f'## {h}' for h in missing)} section"] if missing else []


def link_target(link):
    """The path a wiki link or embed points to: no `!`, brackets, alias or #heading."""
    return str(link).strip().lstrip("!").strip("[]").split("|")[0].split("#")[0]


def link_name(link):
    """The note name a wiki link points to: its target without the folder path."""
    return link_target(link).split("/")[-1]


def linked_note(folder, link):
    """The note `link` names anywhere under the Vault's `folder`, or None."""
    # shortcut: two notes of one name in different subfolders resolve to the last; Obsidian would ask.
    return VAULT_NOTES.get((folder, link_name(link)))


def digest_links(note):
    topics = note["fm"].get("topics")
    return topics if isinstance(topics, list) else []


def digest_topics(note):
    """Return (Topic frontmatters found, links with no Topic note) for a Digest note."""
    found, missing = [], []
    for link in digest_links(note):
        topic = linked_note("Topics", link)
        if topic and topic["fm"]:
            found.append(topic["fm"])
        else:
            missing.append(str(link))
    return found, missing


def check_digest_links(note):
    if kind_of(note) != "digest":
        return []
    topics = note["fm"].get("topics")
    if topics is not None and not isinstance(topics, list):
        return [f"topics {topics!r} must be a list of Topic links"]
    return [f"topic {link} has no note in Topics/" for link in digest_topics(note)[1]]


def check_digest_size(note):
    if kind_of(note) != "digest" or not isinstance(note["fm"].get("topics"), list):
        return []  # a missing or malformed list is reported by required-fields or digest-links
    count = len(note["fm"]["topics"])
    return [] if 5 <= count <= 8 else [f"digest holds {count} topics, expected 5 to 8"]


def check_digest_ranks(note):
    """Ranks run 1..N, best first, in the order of the Digest's `topics` list."""
    if kind_of(note) != "digest":
        return []
    found, missing = digest_topics(note)
    if missing or not found:
        return []  # a broken link is reported by digest-links
    ranks = [t.get("rank") for t in found]
    if ranks == list(range(1, len(found) + 1)):
        return []
    return [f"ranks {ranks} in topics order must run 1 to {len(found)}"]


def check_digest_rubrics(note):
    if kind_of(note) != "digest":
        return []
    rubrics = [t.get("rubric") for t in digest_topics(note)[0]]
    crowded = sorted({r for r in rubrics if isinstance(r, str) and rubrics.count(r) > 2})
    return [f"more than two topics of rubric {r!r}" for r in crowded]


def check_digest_promotional(note):
    if kind_of(note) != "digest":
        return []
    topics = digest_topics(note)[0]
    promo = sum(1 for t in topics if t.get("promotional") is True)
    if 3 * promo <= len(topics):
        return []
    return [f"{promo} of {len(topics)} topics are promotional, at most a third allowed"]


def as_date(value):
    """Return a date from YAML's date, datetime or ISO string, else None."""
    if isinstance(value, datetime.datetime):
        return value.date()
    if isinstance(value, datetime.date):
        return value
    try:
        return datetime.date.fromisoformat(str(value))
    except ValueError:
        return None


def check_trend_scan_date(note):
    value = note["fm"].get("date") if kind_of(note) == "trend-scan" else None
    if value is None or as_date(value):
        return []  # a missing date is reported by required-fields
    return [f"date {value!r} is not an ISO date (YYYY-MM-DD)"]


def check_digest_trend_scan(note):
    link = note["fm"].get("trend_scan") if kind_of(note) == "digest" else None
    if not link:
        return []  # a missing trend_scan is reported by required-fields
    scan = linked_note("Trend scans", link)
    if not scan or not scan["fm"]:
        return [f"trend_scan {link} has no note in Trend scans/"]
    digest_date, scan_date = as_date(note["fm"].get("date")), as_date(scan["fm"].get("date"))
    if not (digest_date and scan_date):
        return []  # an unreadable date is reported on its own note
    age = (digest_date - scan_date).days
    if age > TREND_SCAN_MAX_AGE_DAYS:
        return [f"trend_scan {link} is {age} days older than the digest, at most {TREND_SCAN_MAX_AGE_DAYS} allowed"]
    return []


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
    attachments = fm.get("attachments")
    if not isinstance(attachments, dict) or not attachments:
        problems.append("attachments must map each Attachment type to its limits")
    else:
        for name, limits in attachments.items():
            limits = limits if isinstance(limits, dict) else {}
            formats = limits.get("formats")
            size = limits.get("max_size_mb")
            if not is_count(limits.get("max_count")):
                problems.append(f"attachments.{name}.max_count must be a positive integer")
            if not (isinstance(formats, list) and formats and all(isinstance(f, str) for f in formats)):
                problems.append(f"attachments.{name}.formats must be a non-empty list")
            if isinstance(size, bool) or not isinstance(size, (int, float)) or size <= 0:
                problems.append(f"attachments.{name}.max_size_mb must be a positive number")
    hashtags = fm.get("hashtags")
    if not isinstance(hashtags, dict) or not is_count(hashtags.get("max"), minimum=0):
        problems.append("hashtags.max must be a non-negative integer")
    if fm.get("channel") == "reddit":
        subreddits = fm.get("subreddits")
        if not (isinstance(subreddits, list) and subreddits and all(isinstance(s, str) for s in subreddits)):
            problems.append("subreddits must be a non-empty list")
        if not isinstance(text, dict) or not is_count(text.get("max_title_length")):
            problems.append("text.max_title_length must be a positive integer")
    return problems


def load_channel_rules(vault):
    """Return ({channel: frontmatter} for each valid Channel rules note, violation lines,
    number of Channel rules notes read)."""
    rules, seen, violations = {}, {}, []
    paths = sorted((vault / CHANNEL_RULES_FOLDER).rglob("*.md"))
    for path in paths:
        note = read_note(path)
        problems = check_frontmatter(note) + check_channel_rules(note)
        channel = note["fm"].get("channel") if note["fm"] else None
        if isinstance(channel, str) and channel in seen:
            problems.append(f"channel {channel!r} is already defined in {seen[channel].relative_to(vault)}")
        elif isinstance(channel, str):
            seen[channel] = path
        violations += [f"{path.relative_to(vault)}: [channel-rules] {p}" for p in problems]
        if not problems:
            rules[channel] = note["fm"]
    return rules, violations, len(paths)


def check_draft_topic(note):
    topic = note["fm"].get("topic") if kind_of(note) == "draft" else None
    if not topic:
        return []  # a missing topic is reported by required-fields
    linked = linked_note("Topics", topic)
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


def is_ready_package(note):
    return kind_of(note) == "post" and note["fm"].get("status") == "ready"


def text_rules(note):
    """The Channel rules for a Draft or a ready Publish package, else None."""
    channel = note["fm"].get("channel") if kind_of(note) == "draft" or is_ready_package(note) else None
    # shortcut: a note whose Channel has no rules note goes unchecked; add a rule once every Channel has one.
    return CHANNEL_RULES.get(channel) if isinstance(channel, str) else None


def post_text(note):
    """The Post text of a Draft or Publish package: the body after the frontmatter, up to the Hook alternatives
    callout or the first `## ` heading, stripped."""
    body = OWNER_MARKER.sub("", FRONTMATTER.sub("", note["text"], count=1))  # markers are never posted
    return POST_TEXT_END.split(body, maxsplit=1)[0].strip()


def check_draft_length(note):
    rules = text_rules(note)
    if not rules:
        return []
    # URLs count as written: stricter than X, which counts each as 23 characters.
    length = len(post_text(note))
    limit = rules["text"]["max_length"]
    return [] if length <= limit else [f"post text is {length} characters, {rules['channel']} allows {limit}"]


# A hashtag starts a word and holds a letter first: not a URL fragment (page#top) or a number (issue #91).
HASHTAG = re.compile(r"(?<!\S)#[^\W\d_]\w*")


def check_hashtags(note):
    rules = text_rules(note)
    if not rules:
        return []
    count, limit = len(HASHTAG.findall(post_text(note))), rules["hashtags"]["max"]
    return [] if count <= limit else [f"post text has {count} hashtags, {rules['channel']} allows {limit}"]


def load_repo_slugs(vault):
    notes = (read_note(p) for p in sorted((vault / "Projects").glob("*.md")))
    return [n["fm"]["github"] for n in notes if n["fm"] and isinstance(n["fm"].get("github"), str) and n["fm"]["github"]]


def check_private_repo_link(note):
    if kind_of(note) not in ("topic", "draft", "post"):
        return []
    text = note["text"]
    # [/:] covers https and ssh remotes; the slug may end in .git, /issues/91, ) or end of line.
    return [
        f"links to the private repository {slug}"
        for slug in REPO_SLUGS
        if re.search(rf"github\.com[/:]{re.escape(slug)}(?![\w-])", text, re.IGNORECASE)
    ]


def check_editor_rounds(note):
    if kind_of(note) != "draft" or "editor_rounds" not in note["fm"]:
        return []
    rounds = note["fm"]["editor_rounds"]
    if is_count(rounds, minimum=0) and rounds <= MAX_EDITOR_ROUNDS:
        return []
    return [f"editor_rounds {rounds!r} must be a whole number from 0 to {MAX_EDITOR_ROUNDS}"]


def check_post_folder(note):
    status = note["fm"].get("status") if kind_of(note) == "post" else None
    folder = POST_FOLDERS.get(status) if isinstance(status, str) else None
    if not folder or note["path"].relative_to(VAULT_ROOT[0]).parts[0] == folder:
        return []
    return [f"{status} post belongs in {folder}/"]


def package_attachments(note):
    """The Attachment entries ({file, alt}) of a ready Publish package, else []. Published Posts
    are not checked: their video files stay out of git, so a fresh clone lacks them."""
    entries = note["fm"].get("attachments") if is_ready_package(note) else None
    return entries if isinstance(entries, list) else []


def attachment_path(entry):
    """The file a `file:` entry names: a path from the Vault root ("[[Attachments/x.png]]"), else
    a shortest-path link as Obsidian writes by default ("![[x.png]]"), found under Attachments/."""
    target = link_target(entry["file"])
    path = VAULT_ROOT[0] / target
    if path.is_file():
        return path
    # shortcut: two Attachments of one name in different subfolders resolve to the first found.
    return next((VAULT_ROOT[0] / "Attachments").rglob(target), path)


def typed_attachments(note):
    """Return (Channel rules, [(entry, Attachment type or None)]) for a ready Publish package whose
    Channel has rules; the type is the Channel's Attachment type whose formats hold the file's extension."""
    rules = text_rules(note)
    entries = [e for e in package_attachments(note) if isinstance(e, dict) and e.get("file")]
    if not rules or not entries:
        return rules, []
    typed = []
    for entry in entries:
        ext = attachment_path(entry).suffix.lower().lstrip(".")
        ext = {"jpeg": "jpg"}.get(ext, ext)
        typed.append((entry, next((t for t, lim in rules["attachments"].items() if ext in lim["formats"]), None)))
    return rules, typed


def check_attachment_files(note):
    entries = note["fm"].get("attachments") if is_ready_package(note) else None
    if entries is not None and not isinstance(entries, list):
        return [f"attachments {entries!r} must be a list of {{file, alt}} entries"]
    messages = []
    for entry in package_attachments(note):
        if not (isinstance(entry, dict) and entry.get("file")):
            messages.append(f"attachment {entry!r} has no file")
        elif not attachment_path(entry).is_file():
            messages.append(f"attachment {entry['file']} has no file on disk")
    return messages


def check_attachment_format(note):
    rules, typed = typed_attachments(note)
    return [f"attachment {e['file']} is not a format {rules['channel']} allows" for e, t in typed if t is None]


def check_attachment_count(note):
    rules, typed = typed_attachments(note)
    types = [t for _, t in typed if t]
    return [
        f"{types.count(t)} {t} attachments, {rules['channel']} allows {rules['attachments'][t]['max_count']}"
        for t in sorted(set(types))
        if types.count(t) > rules["attachments"][t]["max_count"]
    ]


def check_attachment_size(note):
    rules, typed = typed_attachments(note)
    messages = []
    for entry, attachment_type in typed:
        path = attachment_path(entry)
        if attachment_type and path.is_file():  # a missing file is reported by attachment-files
            size_mb, limit = path.stat().st_size / 1_000_000, rules["attachments"][attachment_type]["max_size_mb"]
            if size_mb > limit:
                messages.append(f"attachment {entry['file']} is {size_mb:.3f} MB, {rules['channel']} allows {limit} MB")
    return messages


def check_alt_text(note):
    _, typed = typed_attachments(note)
    return [
        f"attachment {e['file']} has no alt text"
        for e, t in typed
        if t in ALT_TEXT_TYPES and not (isinstance(e.get("alt"), str) and e["alt"].strip())
    ]


def check_mixed_attachments(note):
    rules, typed = typed_attachments(note)
    types = sorted({t for _, t in typed if t})
    if rules and rules.get("mixed_attachments") is False and len(types) > 1:
        return [f"attachments mix {', '.join(types)}; {rules['channel']} allows one Attachment type per Post"]
    return []


def check_topic_drafts(note):
    """An approved Topic has exactly one Draft per Channel it lists and none for a Channel it does
    not list; a Publish package or Post for the Channel stands in for a Draft already packaged.
    A missing Draft is reported only once /write has started the Topic and no Draft is `drafting`
    (/write first creates one `drafting` Draft per Channel)."""
    fm = note["fm"]
    if kind_of(note) != "topic" or fm.get("status") != "approved" or not isinstance(fm.get("channels"), list):
        return []
    linked = [
        n["fm"] for n in VAULT_NOTES.values()
        if kind_of(n) in ("draft", "post") and n["fm"].get("topic") and link_name(n["fm"]["topic"]) == note["path"].stem
    ]
    written = linked and not any(f.get("kind") == "draft" and f.get("status") == "drafting" for f in linked)
    messages = []
    for channel in fm["channels"]:
        drafts = sum(1 for f in linked if f.get("kind") == "draft" and f.get("channel") == channel)
        if drafts > 1:
            messages.append(f"approved topic has {drafts} drafts for {channel}, expected one")
        elif written and not any(f.get("channel") == channel for f in linked):
            messages.append(f"approved topic has no draft for {channel}")
    stale = sorted({str(f.get("channel")) for f in linked if f.get("channel") and f.get("channel") not in fm["channels"]})
    messages += [f"approved topic has a draft or post for {c}, which it does not list in channels" for c in stale]
    return messages


def reddit_draft_rules(note):
    """The Reddit Channel rules for a Reddit Draft or ready Publish package, else None."""
    rules = text_rules(note)
    return rules if rules and rules["channel"] == "reddit" else None


def check_reddit_subreddit(note):
    rules = reddit_draft_rules(note)
    if not rules:
        return []
    listed = rules["subreddits"]
    subreddit = note["fm"].get("subreddit")
    return [] if subreddit in listed else [f"subreddit {subreddit!r} is not one of {', '.join(map(str, listed))}"]


def check_reddit_title(note):
    rules = reddit_draft_rules(note)
    if not rules:
        return []
    title = note["fm"].get("title")
    if not isinstance(title, str) or not title.strip():
        return [f"reddit {kind_of(note)} has no title"]
    limit = rules["text"]["max_title_length"]
    if len(title) > limit:
        return [f"title is {len(title)} characters, reddit allows {limit}"]
    return []


def owner_fingerprints(text):
    """One fingerprint per Owner block in the note body. The `o` prefix keeps YAML from reading it as a number."""
    body = FRONTMATTER.sub("", text.replace("\r\n", "\n"), count=1)
    return ["o" + hashlib.sha256(block.strip().encode()).hexdigest()[:8] for block in OWNER_BLOCK.findall(body)]


def check_owner_edits(note):
    """A Role changed, removed or added an Owner block unless the fingerprints still match."""
    if kind_of(note) != "draft":
        return []
    # shortcut: deleting an Owner block together with its owner_edits entry passes; only git history shows it.
    sealed = note["fm"].get("owner_edits") or []
    if [str(s) for s in (sealed if isinstance(sealed, list) else [sealed])] == owner_fingerprints(note["text"]):
        return []
    return ["an Owner-edited part no longer matches owner_edits; if you changed it yourself, run scripts/vault_check.py --seal on this note"]


def seal(path):
    """Rewrite only the `owner_edits` key (flow or block list) of the note at `path`."""
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        raise SystemExit(f"{path}: no YAML frontmatter block")
    prints = owner_fingerprints(text)
    fm = re.sub(r"^owner_edits:.*\n(?:[ \t]+.*\n|- .*\n)*", "", match.group(1), flags=re.MULTILINE)
    path.write_text(text[: match.start(1)] + fm + f"owner_edits: [{', '.join(prints)}]\n" + text[match.end(1):], encoding="utf-8")
    return prints


RULES = [
    check_frontmatter, check_kind, check_required_fields, check_status, check_published_link,
    check_fact_sheet, check_rubric, check_rejection_reason, check_topic_channels, check_topic_sections,
    check_digest_links, check_digest_size, check_digest_ranks, check_digest_rubrics, check_digest_promotional,
    check_trend_scan_date, check_digest_trend_scan,
    check_draft_topic, check_draft_passes, check_draft_length, check_hashtags,
    check_private_repo_link, check_editor_rounds,
    check_topic_drafts, check_reddit_subreddit, check_reddit_title,
    check_post_folder, check_attachment_files, check_attachment_format, check_attachment_count,
    check_attachment_size, check_alt_text, check_mixed_attachments, check_owner_edits,
]


def check_vault(vault):
    """Return (notes checked, list of 'note: [rule] message' lines)."""
    REPO_SLUGS[:] = load_repo_slugs(vault)
    VAULT_ROOT[:] = [vault]
    channel_rules, channel_violations, channel_count = load_channel_rules(vault)
    CHANNEL_RULES.clear()
    CHANNEL_RULES.update(channel_rules)
    paths = sorted(p for folder in NOTE_FOLDERS for p in (vault / folder).rglob("*.md"))
    notes = [read_note(p) for p in paths]
    VAULT_NOTES.clear()
    VAULT_NOTES.update({(n["path"].relative_to(vault).parts[0], n["path"].stem): n for n in notes})
    violations = []
    for note in notes:
        for rule in RULES:
            name = rule.__name__.removeprefix("check_").replace("_", "-")
            for message in rule(note):
                violations.append(f"{note['path'].relative_to(vault)}: [{name}] {message}")
    return len(paths) + channel_count, violations + channel_violations


def main(argv):
    if len(argv) == 3 and argv[1] == "--seal":
        prints = seal(Path(argv[2]))
        print(f"Sealed {len(prints)} Owner edit(s) in {argv[2]}.")
        return 0
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
