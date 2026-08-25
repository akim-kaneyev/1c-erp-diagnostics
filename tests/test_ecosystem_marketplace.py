from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"

MARKETPLACE_ID = "one-c-erp-diagnostics-marketplace"
PLUGIN_VERSION = "0.3.2"
UNICA_COMMIT = "aefc880f9bab606a5c55ed11af563b740054a549"
POWERSHELL_COMMIT = "8cb7868145281d8e353831512cc1ffa72f1b5c89"
PYTHON_COMMIT = "c1f79f5ac9f31c620b8508f75464f8c42c559ae4"


class EcosystemMarketplaceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.marketplace = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
        self.plugins = {
            item["name"]: item for item in self.marketplace["plugins"]
        }

    def test_marketplace_identity_and_order(self) -> None:
        self.assertEqual(self.marketplace["name"], MARKETPLACE_ID)
        self.assertEqual(
            self.marketplace["interface"]["displayName"],
            "1C ERP Diagnostics Ecosystem",
        )
        self.assertEqual(
            [item["name"] for item in self.marketplace["plugins"]],
            ["one-c-erp-diagnostics", "unica", "1c-skills", "1c-skills-py"],
        )
        self.assertEqual(len(self.plugins), 4)

    def test_primary_plugin_is_local(self) -> None:
        source = self.plugins["one-c-erp-diagnostics"]["source"]
        self.assertEqual(
            source,
            {
                "source": "local",
                "path": "./plugins/one-c-erp-diagnostics",
            },
        )

    def test_unica_is_pinned_to_canonical_marketplace_commit(self) -> None:
        source = self.plugins["unica"]["source"]
        self.assertEqual(source["source"], "git-subdir")
        self.assertEqual(
            source["url"],
            "https://github.com/IngvarConsulting/unica-marketplace.git",
        )
        self.assertEqual(source["path"], "plugins/unica")
        self.assertEqual(source["sha"], UNICA_COMMIT)
        self.assertNotIn("ref", source)
        self.assertRegex(source["sha"], r"^[0-9a-f]{40}$")

    def test_1c_skills_are_pinned_to_immutable_generated_shas(self) -> None:
        expected = {
            "1c-skills": POWERSHELL_COMMIT,
            "1c-skills-py": PYTHON_COMMIT,
        }
        for name, sha in expected.items():
            source = self.plugins[name]["source"]
            self.assertEqual(source["source"], "url")
            self.assertEqual(
                source["url"],
                "https://github.com/Nikolay-Shirokov/cc-1c-skills.git",
            )
            self.assertEqual(source["sha"], sha)
            self.assertNotIn("ref", source)
            self.assertRegex(sha, r"^[0-9a-f]{40}$")

    def test_every_plugin_requires_explicit_installation(self) -> None:
        for item in self.marketplace["plugins"]:
            policy = item["policy"]
            self.assertEqual(policy["installation"], "AVAILABLE")
            self.assertEqual(policy["authentication"], "ON_INSTALL")
            self.assertNotEqual(policy["installation"], "INSTALLED_BY_DEFAULT")

    def test_documented_provenance_and_terms_exist(self) -> None:
        ecosystem = (ROOT / "docs" / "ECOSYSTEM_MARKETPLACE.md").read_text(
            encoding="utf-8"
        )
        integrations = (ROOT / "docs" / "OPEN_SOURCE_INTEGRATIONS.md").read_text(
            encoding="utf-8"
        )
        release_notes = (
            ROOT / "docs" / f"RELEASE_NOTES_v{PLUGIN_VERSION}.md"
        ).read_text(encoding="utf-8")
        audit = (
            ROOT / "docs" / f"PLUGIN_AUDIT_v{PLUGIN_VERSION}.md"
        ).read_text(encoding="utf-8")
        terms = (ROOT / "TERMS.md").read_text(encoding="utf-8")
        companion = (
            ROOT
            / "plugins"
            / "one-c-erp-diagnostics"
            / "skills"
            / "one-c-erp-companion-plugins"
            / "SKILL.md"
        ).read_text(encoding="utf-8")

        for token in (UNICA_COMMIT, POWERSHELL_COMMIT, PYTHON_COMMIT):
            self.assertIn(token, ecosystem)
            self.assertIn(token, integrations)
            self.assertIn(token, release_notes)
            self.assertIn(token, companion)

        self.assertIn(PLUGIN_VERSION, audit)
        self.assertIn(MARKETPLACE_ID, ecosystem)
        self.assertIn("v0.12.0", ecosystem)
        self.assertIn("v0.12.0", integrations)
        self.assertIn("third-party", terms.lower())
        self.assertIn("permissions", ecosystem.lower())


if __name__ == "__main__":
    unittest.main()
