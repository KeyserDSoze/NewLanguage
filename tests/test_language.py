import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from normalize_ipa import normalize  # noqa: E402


class PhonologyTests(unittest.TestCase):
    def test_direct_core_words(self):
        self.assertEqual(normalize("/mi/"), ("mi", "mi"))
        self.assertEqual(normalize("/ju/"), ("yu", "yu"))
        self.assertEqual(normalize("/hæv/"), ("hav", "ha-v"))

    def test_diphthong_collapse(self):
        self.assertEqual(normalize("/goʊ/"), ("go", "go"))
        self.assertEqual(normalize("/ðeɪ/"), ("de", "de"))

    def test_cluster_repair(self):
        self.assertEqual(normalize("/strɪŋ/"), ("sitirin", "si-ti-ri-n"))
        self.assertEqual(normalize("/wɝk/"), ("werak", "we-ra-k"))

    def test_vowel_initial_repair(self):
        self.assertEqual(normalize("/æpəl/"), ("hapal", "ha-pa-l"))

    def test_dictionary_forms_match_pattern(self):
        spec = json.loads((ROOT / "spec" / "phonology.json").read_text(encoding="utf-8"))
        pattern = re.compile(spec["orthography"]["word_pattern"])
        for raw in (ROOT / "dictionary" / "entries.jsonl").read_text(encoding="utf-8").splitlines():
            if not raw.strip():
                continue
            item = json.loads(raw)
            if item.get("status") == "accepted":
                self.assertRegex(item["string"], pattern)


if __name__ == "__main__":
    unittest.main()
