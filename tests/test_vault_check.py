"""Feed fixture Vaults to the Vault check and assert its verdicts."""

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "vault_check.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def run_check(vault):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(vault)], capture_output=True, text=True
    )
    violations = [line for line in result.stdout.splitlines() if ": [" in line]
    return result.returncode, violations


# The real Vault is checked by running the script directly, not here: Owner edits must not fail the code tests.
def test_clean_vault_passes():
    assert run_check(FIXTURES / "valid") == (0, [])


# fixture folder -> (note, rule it must be reported under)
BROKEN = {
    "frontmatter": ("Topics/No frontmatter.md", "frontmatter"),
    "kind": ("Topics/Unknown kind.md", "kind"),
    "required-fields-topic": ("Topics/No rubric.md", "required-fields"),
    "required-fields-draft": ("Drafts/No topic link.md", "required-fields"),
    "required-fields-post": ("Publish packages/No channel.md", "required-fields"),
    "required-fields-scout-rank": ("Topics/Scout topic without rank.md", "required-fields"),
    "topic-origin": ("Topics/Unknown origin.md", "topic-origin"),
    "status-topic": ("Topics/Wrong status.md", "status"),
    "status-draft": ("Drafts/Wrong status.md", "status"),
    "status-post": ("Posts/Wrong status.md", "status"),
    "published-link": ("Posts/No link.md", "published-link"),
    "status-fact-sheet": ("Fact sheets/Wrong status.md", "status"),
    "fact-sheet": ("Fact sheets/No public name.md", "fact-sheet"),
    "rubric": ("Topics/Bad rubric.md", "rubric"),
    "rejection-reason": ("Topics/No reason.md", "rejection-reason"),
    "digest-links": ("Digests/2026-10-22 traffic_jam.md", "digest-links"),
    "digest-size": ("Digests/2026-10-22 traffic_jam.md", "digest-size"),
    "digest-rubrics": ("Digests/2026-10-22 traffic_jam.md", "digest-rubrics"),
    "digest-promotional": ("Digests/2026-10-22 traffic_jam.md", "digest-promotional"),
    "channel-rules": ("Channel rules/X.md", "channel-rules"),
    "draft-topic": ("Drafts/Missing topic.md", "draft-topic"),
    "draft-passes": ("Drafts/Passes out of order.md", "draft-passes"),
    "draft-length": ("Drafts/Too long.md", "draft-length"),
    "private-repo-link": ("Topics/Event factory.md", "private-repo-link"),
    "editor-rounds": ("Drafts/Three rounds.md", "editor-rounds"),
    "required-fields-trend-scan": ("Trend scans/No date.md", "required-fields"),
    "trend-scan-date": ("Trend scans/Undated.md", "trend-scan-date"),
    "digest-trend-scan": ("Digests/2026-10-22 traffic_jam.md", "digest-trend-scan"),
    "required-fields-digest": ("Digests/2026-10-22 traffic_jam.md", "required-fields"),
    "frontmatter-reader-error": ("Topics/Control character.md", "frontmatter"),
    "frontmatter-encoding": ("Topics/Latin-1.md", "frontmatter"),
    "digest-topics-list": ("Digests/2026-10-22 traffic_jam.md", "digest-links"),
    "digest-ranks": ("Digests/2026-10-22 traffic_jam.md", "digest-ranks"),
    "topic-sections": ("Topics/No shot list.md", "topic-sections"),
    "topic-channels": ("Topics/Unknown channel.md", "topic-channels"),
    "channel-rules-duplicate": ("Channel rules/X.md", "channel-rules"),
    "attachment-files": ("Publish packages/Missing file.md", "attachment-files"),
    "attachment-count": ("Publish packages/Five images.md", "attachment-count"),
    "attachment-format": ("Publish packages/Bitmap.md", "attachment-format"),
    "attachment-size": ("Publish packages/Large image.md", "attachment-size"),
    "alt-text": ("Publish packages/No alt text.md", "alt-text"),
    "mixed-attachments": ("Publish packages/Image and GIF.md", "mixed-attachments"),
    "post-folder": ("Publish packages/Published.md", "post-folder"),
    "topic-drafts-missing": ("Topics/Road capacity explained.md", "topic-drafts"),
    "topic-drafts-duplicate": ("Topics/Road capacity explained.md", "topic-drafts"),
    "reddit-subreddit": ("Drafts/Road capacity explained - reddit.md", "reddit-subreddit"),
    "reddit-title": ("Drafts/Road capacity explained - reddit.md", "reddit-title"),
    "owner-edits": ("Drafts/Road capacity explained - x.md", "owner-edits"),
    "topic-drafts-stale": ("Topics/Road capacity explained.md", "topic-drafts"),
    "hashtags": ("Drafts/Two hashtags.md", "hashtags"),
    "draft-length-package": ("Publish packages/Too long.md", "draft-length"),
    "reddit-title-package": ("Publish packages/Road capacity explained - reddit.md", "reddit-title"),
    "channel-rules-reddit": ("Channel rules/Reddit.md", "channel-rules"),
}


# owner_edits as Obsidian's Properties panel writes it (block list), unindented, or a flow list over two lines.
@pytest.mark.parametrize("sealed", ["owner_edits:\n  - o71d89536\n", "owner_edits:\n- o71d89536\n", "owner_edits: [o71d89536,\n  o12345678]\n"])
def test_seal_records_owner_edits_and_leaves_other_frontmatter(tmp_path, sealed):
    """The owner_edits key is replaced whatever its layout; nothing else moves."""
    vault = tmp_path / "vault"
    shutil.copytree(FIXTURES / "owner-edits", vault)
    draft = vault / "Drafts" / "Road capacity explained - x.md"
    others = [line for line in draft.read_text().splitlines() if "owner_edits" not in line]
    draft.write_text(draft.read_text().replace("owner_edits: [o71d89536]\n", sealed))
    assert run_check(vault)[0] == 1
    subprocess.run([sys.executable, str(SCRIPT), "--seal", str(draft)], check=True, capture_output=True)
    assert run_check(vault) == (0, [])
    assert [line for line in draft.read_text().splitlines() if "owner_edits" not in line] == others


@pytest.mark.parametrize("fixture", BROKEN)
def test_broken_vault_fails_naming_note_and_rule(fixture):
    note, rule = BROKEN[fixture]
    code, violations = run_check(FIXTURES / fixture)
    assert code == 1
    assert len(violations) == 1, violations
    assert violations[0].startswith(f"{note}: [{rule}] ")


def test_list_rubrics_are_reported_not_crashed_on():
    """Three Topics share the list rubric [Devlog]: digest-rubrics must skip it, not crash."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(FIXTURES / "digest-rubric-list")], capture_output=True, text=True
    )
    violations = [line for line in result.stdout.splitlines() if ": [" in line]
    assert "Traceback" not in result.stderr
    assert result.returncode == 1
    assert len(violations) == 3 and all(": [rubric] " in v for v in violations), violations


def test_non_text_channel_and_status_are_reported_not_crashed_on():
    """A Draft with channel [x] and a Post with status [ready] must not crash any rule."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(FIXTURES / "non-string-keys")], capture_output=True, text=True
    )
    assert "Traceback" not in result.stderr
    assert result.returncode == 1
