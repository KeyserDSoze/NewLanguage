import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from normalize_ipa import normalize  # noqa: E402
from read_number import read_number  # noqa: E402


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


class NumberTests(unittest.TestCase):
    def test_integer_reading(self):
        self.assertEqual(read_number("2026"), "tun ziro tun sikas")

    def test_leading_zeroes(self):
        self.assertEqual(read_number("007"), "ziro ziro sevan")

    def test_decimal_and_negative(self):
        self.assertEqual(read_number("-3.14"), "manas tiri dot wan foro")

    def test_grouping_separator_is_ignored(self):
        self.assertEqual(read_number("1,000"), "wan ziro ziro ziro")

    def test_invalid_number_is_rejected(self):
        with self.assertRaises(ValueError):
            read_number("12x")


if __name__ == "__main__":
    unittest.main()
