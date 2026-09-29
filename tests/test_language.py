import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from normalize_ipa import normalize  # noqa: E402
from read_number import read_number  # noqa: E402
from read_datetime import read_date, read_time  # noqa: E402
from generate_dictionary_candidates import arpabet_to_ipa  # noqa: E402


class PhonologyTests(unittest.TestCase):
    def test_direct_core_words(self):
        self.assertEqual(normalize("/mi/"), ("mi", "mi"))
        self.assertEqual(normalize("/ju/"), ("yu", "yu"))
        self.assertEqual(normalize("/hæv/"), ("hav", "ha-v"))
        self.assertEqual(normalize("/pliz/"), ("piliz", "pi-li-z"))
        self.assertEqual(normalize("/θɪŋ/"), ("tin", "ti-n"))
        self.assertEqual(normalize("/ˈɛni/"), ("heni", "he-ni"))
        self.assertEqual(normalize("/itʃ/"), ("hic", "hi-c"))
        self.assertEqual(normalize("/boʊθ/"), ("bot", "bo-t"))
        self.assertEqual(normalize("/seɪm/"), ("sem", "se-m"))
        self.assertEqual(normalize("/gɪv/"), ("giv", "gi-v"))

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


class LexicalGeneratorTests(unittest.TestCase):
    def test_arpabet_to_ipa(self):
        self.assertEqual(arpabet_to_ipa(["P", "L", "IY1", "Z"]), "pliz")
        self.assertEqual(arpabet_to_ipa(["DH", "EH1", "R"]), "ðɛɹ")
        self.assertEqual(arpabet_to_ipa(["AH0", "DH", "ER0"]), "əðɚ")

    def test_arpabet_output_normalizes_to_string(self):
        ipa = arpabet_to_ipa(["P", "L", "IY1", "Z"])
        self.assertEqual(normalize("/" + ipa + "/"), ("piliz", "pi-li-z"))


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


class DateTimeTests(unittest.TestCase):
    def test_date_reading(self):
        self.assertEqual(
            read_date("2026-09-29"),
            "det tun ziro tun sikas, ziro nayan, tun nayan",
        )

    def test_time_reading(self):
        self.assertEqual(read_time("14:30"), "tam wan foro, tiri ziro")
        self.assertEqual(
            read_time("08:05:09"),
            "tam ziro het, ziro fav, ziro nayan",
        )

    def test_invalid_calendar_values_are_rejected(self):
        with self.assertRaises(ValueError):
            read_date("2026-02-30")
        with self.assertRaises(ValueError):
            read_time("25:00")


if __name__ == "__main__":
    unittest.main()
