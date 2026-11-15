from __future__ import annotations

import importlib.util
import io
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("viewer_publication", ROOT / "tools/validate_publication_history.py")
scanner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scanner)
public_spec = importlib.util.spec_from_file_location("viewer_public_release", ROOT / "tools/validate_public_release.py")
public = importlib.util.module_from_spec(public_spec)
public_spec.loader.exec_module(public)


class ViewerPublicationTests(unittest.TestCase):
    def test_complete_react_boolean_input_support_map_is_not_a_credential(self):
        key = "pass" + "word"
        mapping = ("{color:!0,date:!0,datetime:!0,\"datetime-local\":!0,email:!0,"
                   f"month:!0,number:!0,{key}:!0,range:!0,search:!0,tel:!0,text:!0,time:!0,url:!0,week:!0}}")
        self.assertEqual(scanner.text_findings("const flags=" + mapping + ";"), (False, False))
        self.assertEqual(scanner.stream_text_findings(io.BytesIO(mapping.encode())), (False, False, False))
        self.assertTrue(scanner.text_findings(mapping + f';const config={{{key}:"synthetic"}}')[0])
        self.assertEqual(public.text_findings(mapping), (False, False))
        self.assertTrue(public.text_findings(mapping + f';const config={{{key}:"synthetic"}}')[0])

    def test_no_general_boolean_or_path_exemption_is_introduced(self):
        key = "pass" + "word"
        for content in (f'{{{key}:!0}}', f'{{"{key}":true}}', f'{{{key}:"synthetic"}}', f'{key}=!0'):
            self.assertTrue(scanner.text_findings(content)[0])
            self.assertTrue(public.text_findings(content)[0])
        self.assertIsNotNone(scanner.unsafe_path("cache/example" + ".dt"))


if __name__ == "__main__":
    unittest.main()
