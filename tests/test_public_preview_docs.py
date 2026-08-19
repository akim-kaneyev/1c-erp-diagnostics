from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PublicPreviewDocumentationTests(unittest.TestCase):
    def test_readme_declares_current_public_preview(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("v0.2.2 Public Preview is live", readme)
        self.assertIn("status-public%20preview", readme)
        self.assertNotIn("Repository publication and global Plugin Directory submission remain", readme)

    def test_privacy_scope_matches_current_ecosystem(self) -> None:
        privacy = (ROOT / "PRIVACY.md").read_text(encoding="utf-8")
        self.assertIn("v0.2.2", privacy)
        self.assertIn("Unica and 1C Skills", privacy)
        self.assertNotIn("v0.1.x", privacy)

    def test_public_preview_audit_and_release_notes_exist(self) -> None:
        audit = ROOT / "docs" / "PLUGIN_AUDIT_v0.2.2.md"
        release_notes = ROOT / "docs" / "RELEASE_NOTES_v0.2.2.md"
        checklist = ROOT / "docs" / "PUBLIC_RELEASE_CHECKLIST.md"

        self.assertTrue(audit.is_file())
        self.assertTrue(release_notes.is_file())
        self.assertTrue(checklist.is_file())

        self.assertIn("No critical control is `FAIL`", audit.read_text(encoding="utf-8"))
        self.assertIn("Public Preview", release_notes.read_text(encoding="utf-8"))
        self.assertIn("Repository visibility is Public", checklist.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
