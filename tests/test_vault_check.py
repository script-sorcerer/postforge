"""Feed fixture Vaults to the Vault check and assert its verdicts."""

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


@pytest.mark.parametrize("vault", [FIXTURES / "valid", ROOT], ids=["valid-fixture", "real-vault"])
def test_clean_vault_passes(vault):
    assert run_check(vault) == (0, [])


# fixture folder -> (note, rule it must be reported under)
BROKEN = {
    "frontmatter": ("Topics/No frontmatter.md", "frontmatter"),
    "kind": ("Topics/Unknown kind.md", "kind"),
    "required-fields-topic": ("Topics/No rubric.md", "required-fields"),
    "required-fields-draft": ("Drafts/No topic link.md", "required-fields"),
    "required-fields-post": ("Publish packages/No channel.md", "required-fields"),
    "status-topic": ("Topics/Wrong status.md", "status"),
    "status-draft": ("Drafts/Wrong status.md", "status"),
    "status-post": ("Posts/Wrong status.md", "status"),
    "published-link": ("Posts/No link.md", "published-link"),
}


@pytest.mark.parametrize("fixture", BROKEN)
def test_broken_vault_fails_naming_note_and_rule(fixture):
    note, rule = BROKEN[fixture]
    code, violations = run_check(FIXTURES / fixture)
    assert code == 1
    assert len(violations) == 1, violations
    assert violations[0].startswith(f"{note}: [{rule}] ")
