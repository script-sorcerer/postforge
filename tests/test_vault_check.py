"""Feed fixture Vaults to the Vault check and assert its verdicts."""

import datetime
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
    "channel-rules-shorts": ("Channel rules/Shorts.md", "channel-rules"),
    "shorts-script": ("Drafts/Queue at the junction - shorts.md", "shorts-script"),
    "shorts-script-beat": ("Drafts/Queue at the junction - shorts.md", "shorts-script"),
    "shorts-script-footage": ("Drafts/Queue at the junction - shorts.md", "shorts-script"),
    "shorts-script-one-beat": ("Drafts/Queue at the junction - shorts.md", "shorts-script"),
    "shorts-duration": ("Drafts/Queue at the junction - shorts.md", "shorts-duration"),
    "shorts-duration-limit": ("Drafts/Queue at the junction - shorts.md", "shorts-duration"),
    "shorts-on-screen-text": ("Drafts/Queue at the junction - shorts.md", "shorts-on-screen-text"),
    "shorts-title": ("Drafts/Queue at the junction - shorts.md", "shorts-title"),
    "shorts-video": ("Publish packages/Queue at the junction - shorts.md", "shorts-video"),
    "shorts-package-count": ("Publish packages/Queue at the junction - shorts.md", "attachment-count"),
    "shorts-package-format": ("Publish packages/Queue at the junction - shorts.md", "attachment-format"),
    "shorts-package-size": ("Publish packages/Queue at the junction - shorts.md", "attachment-size"),
    "shorts-package-title": ("Publish packages/Queue at the junction - shorts.md", "shorts-title"),
    "channel-rules-reddit": ("Channel rules/Reddit.md", "channel-rules"),
    "publish-on": ("Publish packages/Lane change bug - x.md", "publish-on"),
    "publish-on-format": ("Publish packages/Lane change bug - x.md", "publish-on"),
    "schedule": ("Schedule/traffic_jam.md", "schedule"),
    "schedule-duplicate": ("Schedule/traffic_jam.md", "schedule"),
    "schedule-slot": ("Publish packages/Lane change bug - x.md", "schedule-slot"),
    "schedule-collision": ("Publish packages/Lane change bug again - x.md", "schedule-collision"),
    "topic-phase": ("Topics/Lane change bug.md", "topic-phase"),
    "phase-date": ("Publish packages/Lane change bug - x.md", "phase-date"),
    "phase-date-undated": ("Publish packages/Lane change bug - x.md", "phase-date"),
    "channel-rules-destination": ("Channel rules/X.md", "channel-rules"),
    "pinned-comment": ("Publish packages/Lane change bug - x.md", "pinned-comment"),
    "fact-sheet-public-links": ("Fact sheets/traffic_jam.md", "fact-sheet"),
    "private-repo-link-pinned-comment": ("Publish packages/Lane change bug - x.md", "private-repo-link"),
    "metrics": ("Posts/Queue at the junction - shorts.md", "metrics"),
}


def test_phase_without_a_date_blocks_scheduling_and_says_so():
    """A Phase with an empty `starts` takes Topics and Drafts (the valid Vault holds one) but no scheduled package."""
    violations = run_check(FIXTURES / "phase-date-undated")[1]
    assert any("Phase 'Reveal' has no date yet" in v for v in violations), violations


def edited_valid_vault(tmp_path, note, old, new):
    """A copy of the valid Vault with `old` replaced by `new` in `note`."""
    vault = tmp_path / "vault"
    shutil.copytree(FIXTURES / "valid", vault)
    path = vault / note
    assert old in path.read_text()
    path.write_text(path.read_text().replace(old, new, 1))
    return vault


def test_list_phase_is_reported_not_crashed_on(tmp_path):
    vault = edited_valid_vault(tmp_path, "Topics/Lane change bug.md", "phase: Pre-reveal", "phase: [Pre-reveal]")
    result = subprocess.run([sys.executable, str(SCRIPT), str(vault)], capture_output=True, text=True)
    assert "Traceback" not in result.stderr
    assert run_check(vault) == (1, ["Topics/Lane change bug.md: [topic-phase] phase ['Pre-reveal'] is not one of the Fact sheet's Phases: Pre-reveal, Reveal"])


@pytest.mark.parametrize("value", ["20261019", "2026-W43-1", "2026-10-19T10:00:00"])
def test_publish_on_accepts_only_yyyy_mm_dd(tmp_path, value):
    vault = edited_valid_vault(tmp_path, "Publish packages/Lane change bug - x.md", "publish_on: 2026-10-19", f"publish_on: {value}")
    code, violations = run_check(vault)
    assert code == 1 and len(violations) == 1 and "[publish-on] " in violations[0], violations


def test_dated_phases_out_of_order_fail_fact_sheet(tmp_path):
    vault = edited_valid_vault(tmp_path, "Fact sheets/traffic_jam.md", "  - name: Reveal\n    starts:\n", "  - name: Reveal\n    starts: 2026-09-01\n")
    assert run_check(vault) == (1, ["Fact sheets/traffic_jam.md: [fact-sheet] Phase 2 starts 2026-09-01, before an earlier Phase starts on 2026-10-01"])


def test_profile_link_channel_needs_no_pinned_comment():
    """Reddit's destination is the profile link, set once by the Owner: its ready package carries no pinned_comment."""
    package = FIXTURES / "valid" / "Publish packages" / "Road capacity explained - reddit.md"
    assert "pinned_comment" not in package.read_text()
    assert "kind: profile_link" in (FIXTURES / "valid" / "Channel rules" / "Reddit.md").read_text()
    assert run_check(FIXTURES / "valid") == (0, [])


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


def test_missing_draft_for_channel_with_unapproved_rules_passes_until_approved(tmp_path):
    """The Writer skips a Channel whose rules are not approved; its missing Draft is reported only once they are."""
    assert run_check(FIXTURES / "topic-drafts-unapproved-rules") == (0, [])
    vault = tmp_path / "vault"
    shutil.copytree(FIXTURES / "topic-drafts-unapproved-rules", vault)
    rules = vault / "Channel rules" / "Shorts.md"
    rules.write_text(rules.read_text().replace("status: proposed", "status: approved", 1))
    code, violations = run_check(vault)
    assert code == 1 and len(violations) == 1 and "[topic-drafts] approved topic has no draft for shorts" in violations[0]


def test_schedule_gap_is_a_warning_until_the_next_cadence_day_is_packaged(tmp_path):
    """A ready Draft waits unpackaged while x's next cadence day is empty: warned, exit 0. A package of that
    Channel on the next cadence day (today, with a daily cadence) fills the gap."""
    vault = tmp_path / "vault"
    shutil.copytree(FIXTURES / "schedule-gap", vault)
    draft = vault / "Drafts" / "Rush hour in one tap - x.md"
    (vault / "Drafts" / "Rush hour in one tap - x2.md").write_text(draft.read_text())  # a second waiting Draft
    code, lines = run_check(vault)
    assert code == 0 and len(lines) == 1, lines
    assert lines[0].startswith("warning: Drafts/Rush hour in one tap - x.md: [schedule-gap] ")
    schedule = vault / "Schedule" / "traffic_jam.md"
    every_day = "[Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]"
    schedule.write_text(schedule.read_text().replace("[Monday, Thursday]", every_day))
    package = vault / "Publish packages" / "Lane change bug - x.md"
    package.write_text(package.read_text().replace("2026-10-19", datetime.date.today().isoformat()))
    assert run_check(vault) == (0, [])


def test_post_metrics_is_a_warning_on_an_old_post_without_7d():
    assert run_check(FIXTURES / "post-metrics") == (0, [
        "warning: Posts/Road capacity explained - x.md: [post-metrics] published 2026-10-01, more than seven days ago, "
        "and has no 7d metrics entry; record the numbers or set metrics: skipped"
    ])


def test_skipped_metrics_stop_the_reminder(tmp_path):
    vault = tmp_path / "vault"
    shutil.copytree(FIXTURES / "post-metrics", vault)
    post = vault / "Posts" / "Road capacity explained - x.md"
    text = post.read_text()
    post.write_text(text[: text.index("metrics:")] + "metrics: skipped\n---\n\nFinal text.\n")
    assert run_check(vault) == (0, [])


def test_post_metrics_waits_seven_days(tmp_path):
    """Published three days ago with only a 2d entry: no reminder yet."""
    vault = tmp_path / "vault"
    shutil.copytree(FIXTURES / "post-metrics", vault)
    post = vault / "Posts" / "Road capacity explained - x.md"
    recent = (datetime.date.today() - datetime.timedelta(days=3)).isoformat()
    post.write_text(post.read_text().replace("published_on: 2026-10-01", f"published_on: {recent}"))
    assert run_check(vault) == (0, [])


@pytest.mark.parametrize("old, new, message", [
    ("    platform: tiktok", "    platform: x", "platform must be youtube or tiktok"),
    ("    likes: 80", "    likes: true", "likes must be a whole number"),
    ("  - at: 7d\n    platform: tiktok", "  - at: 30d\n    platform: tiktok", "at must be one of 2d, 7d"),
    ("    hook: gap", "    hook: curiosity", "hook must be one of gap, prediction, scene, payoff, weight"),
    ("    retention: 71.5", "    retention: 140", "retention must be a percent from 0 to 100"),
])
def test_malformed_metrics_entry_fails(tmp_path, old, new, message):
    vault = tmp_path / "vault"
    shutil.copytree(FIXTURES / "metrics", vault)
    post = vault / "Posts" / "Queue at the junction - shorts.md"
    text = post.read_text().replace("    views: 1k", "    views: 1000")
    assert old in text
    post.write_text(text.replace(old, new, 1))
    code, violations = run_check(vault)
    assert code == 1 and len(violations) == 1 and "[metrics] " in violations[0] and message in violations[0], violations


def test_metrics_not_a_list_is_reported_not_crashed_on(tmp_path):
    vault = tmp_path / "vault"
    shutil.copytree(FIXTURES / "post-metrics", vault)
    post = vault / "Posts" / "Road capacity explained - x.md"
    text = post.read_text()
    post.write_text(text[: text.index("metrics:")] + "metrics: 5\n---\n\nFinal text.\n")
    result = subprocess.run([sys.executable, str(SCRIPT), str(vault)], capture_output=True, text=True)
    assert "Traceback" not in result.stderr and result.returncode == 1 and "[metrics] metrics 5 must be" in result.stdout
