from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.3.2"


class PublicPreviewDocumentationTests(unittest.TestCase):
    def test_readme_declares_current_public_preview(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(f"v{VERSION} Public Preview release candidate", readme)
        self.assertIn(f"version-{VERSION}", readme)
        self.assertIn("status-public%20preview", readme)
        self.assertIn("Velis", readme)
        self.assertNotIn("v0.2.3 Public Preview is live", readme)

    def test_privacy_scope_matches_current_ecosystem(self) -> None:
        privacy = (ROOT / "PRIVACY.md").read_text(encoding="utf-8")
        self.assertIn(f"v{VERSION}", privacy)
        self.assertIn("Unica and 1C Skills", privacy)
        self.assertIn("push protection", privacy)
        self.assertNotIn("v0.1.x", privacy)

    def test_current_audit_release_notes_and_checklist_exist(self) -> None:
        audit = ROOT / "docs" / f"PLUGIN_AUDIT_v{VERSION}.md"
        release_notes = ROOT / "docs" / f"RELEASE_NOTES_v{VERSION}.md"
        checklist = ROOT / "docs" / "PUBLIC_RELEASE_CHECKLIST.md"

        self.assertTrue(audit.is_file())
        self.assertTrue(release_notes.is_file())
        self.assertTrue(checklist.is_file())

        audit_text = audit.read_text(encoding="utf-8")
        release_text = release_notes.read_text(encoding="utf-8")
        checklist_text = checklist.read_text(encoding="utf-8")

        self.assertIn("No known critical control", audit_text)
        self.assertIn("Velis", release_text)
        self.assertIn("CodeQL", release_text)
        self.assertIn(f"Public release checklist — v{VERSION}", checklist_text)
        self.assertIn("Repository visibility is Public", checklist_text)
        self.assertIn("Private vulnerability reporting is enabled", checklist_text)


if __name__ == "__main__":
    unittest.main()
